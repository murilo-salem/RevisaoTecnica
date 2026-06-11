"""
Harness de ablation para comparar variantes do pipeline.
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from datetime import datetime
from statistics import mean
from typing import Dict, List, Sequence

from pipeline.features import PipelineFeatures
from pipeline.frozen_benchmark import build_frozen_components
from pipeline.orchestrator import run_agent


@dataclass(frozen=True)
class AblationVariant:
    """Variante comparável do pipeline."""

    name: str
    description: str
    features: PipelineFeatures


DEFAULT_VARIANTS: Sequence[AblationVariant] = (
    AblationVariant(
        name="baseline",
        description="Pipeline completo com todas as features habilitadas.",
        features=PipelineFeatures(),
    ),
    AblationVariant(
        name="no_evidence",
        description="Remove a exigência de evidência textual.",
        features=PipelineFeatures(require_evidence=False),
    ),
    AblationVariant(
        name="no_clusters",
        description="Desliga a síntese temática por cluster.",
        features=PipelineFeatures(enable_thematic_clusters=False),
    ),
    AblationVariant(
        name="no_prisma",
        description="Desliga os artefatos PRISMA-like.",
        features=PipelineFeatures(enable_prisma=False),
    ),
    AblationVariant(
        name="no_snapshot",
        description="Desliga o snapshot versionado da execução.",
        features=PipelineFeatures(enable_snapshot=False),
    ),
    AblationVariant(
        name="no_comparative_analysis",
        description="Desliga a análise comparativa gerada pelo LLM.",
        features=PipelineFeatures(enable_comparative_analysis=False),
    ),
    AblationVariant(
        name="no_manual_review",
        description="Desliga a fila de revisão manual.",
        features=PipelineFeatures(enable_manual_review_queue=False),
    ),
)


def _slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    return value.strip("_") or "benchmark"


def _load_cases(benchmark_file: str, fallback_query: str, fallback_max_results: int) -> List[Dict[str, object]]:
    if benchmark_file and os.path.exists(benchmark_file):
        with open(benchmark_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        cases = data.get("cases", [])
        if isinstance(cases, list) and cases:
            normalized: List[Dict[str, object]] = []
            for case in cases:
                if not isinstance(case, dict):
                    continue
                query = str(case.get("query", "")).strip()
                if not query:
                    continue
                normalized.append({
                    "name": case.get("name") or query,
                    "query": query,
                    "max_results": int(case.get("max_results", fallback_max_results) or fallback_max_results),
                    "model": case.get("model", ""),
                    "fixture_file": case.get("fixture_file", ""),
                })
            if normalized:
                return normalized

    return [
        {
            "name": fallback_query,
            "query": fallback_query,
            "max_results": fallback_max_results,
            "model": "",
            "fixture_file": "",
        }
    ]


def _summarize_state(state) -> Dict[str, object]:
    coverage = state.coverage_metrics or {}
    scored = [
        evaluation
        for evaluation in state.evaluations
        if evaluation.screening_decision != "exclude" and not evaluation.llm_error
    ]
    avg_relevance = mean([item.relevance_score for item in scored]) if scored else 0.0

    return {
        "run_id": state.run_id,
        "status": state.status,
        "query": state.query,
        "model": state.model,
        "snapshot_hash": state.snapshot_hash,
        "feature_flags": state.feature_flags,
        "coverage_metrics": coverage,
        "average_relevance": round(avg_relevance, 2),
        "total_duration_seconds": state.total_duration_seconds,
        "evaluation_duration_seconds": state.evaluation_duration_seconds,
        "comparative_analysis_duration_seconds": state.comparative_analysis_duration_seconds,
        "output_paths": state.output_paths,
        "errors": state.errors,
        "manual_review_queue_size": len(state.manual_review_queue),
        "clusters": state.thematic_clusters.get("total_clusters", 0) if isinstance(state.thematic_clusters, dict) else 0,
        "stage_metrics_count": len(state.stage_metrics),
        "llm_cache_stats": state.llm_cache_stats,
    }


def _build_comparison(summary: Dict[str, object]) -> Dict[str, object]:
    """Agrupa resultados por variante e calcula deltas contra baseline."""
    grouped: Dict[str, Dict[str, List[float]]] = {}

    for item in summary.get("results", []):
        variant = item.get("variant", {})
        result = item.get("summary", {})
        name = variant.get("name", "unknown")
        bucket = grouped.setdefault(name, {
            "average_relevance": [],
            "total_duration_seconds": [],
            "evaluation_duration_seconds": [],
            "included": [],
            "manual_review_required": [],
            "clusters": [],
            "full_extractions": [],
        })

        coverage = result.get("coverage_metrics", {})
        bucket["average_relevance"].append(float(result.get("average_relevance", 0) or 0))
        bucket["total_duration_seconds"].append(float(result.get("total_duration_seconds", 0) or 0))
        bucket["evaluation_duration_seconds"].append(float(result.get("evaluation_duration_seconds", 0) or 0))
        bucket["included"].append(float(coverage.get("included", 0) or 0))
        bucket["manual_review_required"].append(float(coverage.get("manual_review_required", 0) or 0))
        bucket["clusters"].append(float(result.get("clusters", 0) or 0))
        bucket["full_extractions"].append(float(coverage.get("full_extractions", 0) or 0))

    comparison_rows: List[Dict[str, object]] = []
    baseline = grouped.get("baseline", {})

    def _avg(values: List[float]) -> float:
        return round(mean(values), 2) if values else 0.0

    baseline_avg_relevance = _avg(baseline.get("average_relevance", []))
    baseline_avg_time = _avg(baseline.get("total_duration_seconds", []))
    baseline_avg_eval_time = _avg(baseline.get("evaluation_duration_seconds", []))

    for variant_name, bucket in grouped.items():
        avg_relevance = _avg(bucket.get("average_relevance", []))
        avg_time = _avg(bucket.get("total_duration_seconds", []))
        avg_eval_time = _avg(bucket.get("evaluation_duration_seconds", []))
        avg_included = _avg(bucket.get("included", []))
        avg_manual_review = _avg(bucket.get("manual_review_required", []))
        avg_clusters = _avg(bucket.get("clusters", []))
        avg_full_extractions = _avg(bucket.get("full_extractions", []))

        comparison_rows.append({
            "variant": variant_name,
            "cases": len(bucket.get("average_relevance", [])),
            "avg_relevance": avg_relevance,
            "avg_total_time": avg_time,
            "avg_eval_time": avg_eval_time,
            "avg_included": avg_included,
            "avg_manual_review": avg_manual_review,
            "avg_clusters": avg_clusters,
            "avg_full_extractions": avg_full_extractions,
            "delta_relevance_vs_baseline": round(avg_relevance - baseline_avg_relevance, 2) if baseline else 0.0,
            "delta_total_time_vs_baseline": round(avg_time - baseline_avg_time, 2) if baseline else 0.0,
            "delta_eval_time_vs_baseline": round(avg_eval_time - baseline_avg_eval_time, 2) if baseline else 0.0,
        })

    comparison_rows.sort(
        key=lambda item: (item["avg_relevance"], -item["avg_total_time"]),
        reverse=True,
    )

    return {
        "baseline": {
            "avg_relevance": baseline_avg_relevance,
            "avg_total_time": baseline_avg_time,
            "avg_eval_time": baseline_avg_eval_time,
        },
        "rows": comparison_rows,
        "best_quality": comparison_rows[0]["variant"] if comparison_rows else "",
        "fastest": min(comparison_rows, key=lambda item: item["avg_total_time"])["variant"] if comparison_rows else "",
    }


def run_ablation_suite(
    query: str,
    max_results: int,
    model: str,
    output_dir: str,
    benchmark_file: str = "",
    variants: Sequence[AblationVariant] = DEFAULT_VARIANTS,
) -> Dict[str, object]:
    """Executa um conjunto fixo de variantes sobre um benchmark de consultas."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    suite_root = os.path.join(output_dir, f"ablation_{timestamp}")
    os.makedirs(suite_root, exist_ok=True)

    cases = _load_cases(benchmark_file, query, max_results)
    suite_results: List[Dict[str, object]] = []

    for case in cases:
        case_name = _slugify(str(case["name"]))
        case_dir = os.path.join(suite_root, case_name)
        os.makedirs(case_dir, exist_ok=True)

        for variant in variants:
            variant_dir = os.path.join(case_dir, variant.name)
            os.makedirs(variant_dir, exist_ok=True)

            scrapers = None
            evaluator_factory = None
            fixture_file = str(case.get("fixture_file") or "")
            if fixture_file:
                fixture_path = os.path.abspath(fixture_file)
                scrapers, evaluator_factory = build_frozen_components(fixture_path)

            state = run_agent(
                query=str(case["query"]),
                max_results=int(case["max_results"]),
                model=str(case.get("model") or model),
                output_dir=variant_dir,
                features=variant.features,
                scrapers=scrapers,
                evaluator_factory=evaluator_factory,
            )

            suite_results.append({
                "case": case,
                "variant": {
                    "name": variant.name,
                    "description": variant.description,
                    "features": variant.features.to_dict(),
                },
                "summary": _summarize_state(state),
            })

    summary = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "benchmark_file": os.path.abspath(benchmark_file) if benchmark_file else "",
        "suite_root": os.path.abspath(suite_root),
        "cases": cases,
        "variants": [
            {
                "name": variant.name,
                "description": variant.description,
                "features": variant.features.to_dict(),
            }
            for variant in variants
        ],
        "results": suite_results,
    }
    summary["comparison"] = _build_comparison(summary)

    summary_path = os.path.join(suite_root, "ablation_summary.json")
    markdown_path = os.path.join(suite_root, "ablation_summary.md")
    summary["summary_paths"] = {
        "json": os.path.abspath(summary_path),
        "markdown": os.path.abspath(markdown_path),
    }

    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    with open(markdown_path, "w", encoding="utf-8") as f:
        f.write(_build_markdown_summary(summary))

    return summary


def _build_markdown_summary(summary: Dict[str, object]) -> str:
    lines = [
        "# Ablation Summary",
        "",
        f"- **Gerado em:** {summary.get('generated_at', 'N/A')}",
        f"- **Pasta raiz:** {summary.get('suite_root', 'N/A')}",
        f"- **Benchmark:** {summary.get('benchmark_file', 'N/A') or 'N/A'}",
        "",
        "## Variantes",
        "",
    ]

    for variant in summary.get("variants", []):
        lines.extend([
            f"### {variant.get('name', 'N/A')}",
            "",
            f"- {variant.get('description', '')}",
            "",
        ])

    lines.extend(["## Resultados", ""])

    comparison = summary.get("comparison", {})
    rows = comparison.get("rows", [])
    if rows:
        lines.extend([
            "## Comparação Geral",
            "",
            "| Variante | Casos | Score médio | Δ Score | Tempo total | Δ Tempo | Inclusões | Revisão manual | Clusters |",
            "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
        ])
        for row in rows:
            lines.append(
                f"| {row.get('variant', 'N/A')} | {row.get('cases', 0)} | "
                f"{row.get('avg_relevance', 0):.2f} | {row.get('delta_relevance_vs_baseline', 0):+.2f} | "
                f"{row.get('avg_total_time', 0):.2f}s | {row.get('delta_total_time_vs_baseline', 0):+.2f}s | "
                f"{row.get('avg_included', 0):.2f} | {row.get('avg_manual_review', 0):.2f} | "
                f"{row.get('avg_clusters', 0):.2f} |"
            )
        lines.append("")

        if comparison.get("best_quality") or comparison.get("fastest"):
            lines.extend([
                f"- **Melhor qualidade média:** {comparison.get('best_quality', 'N/A')}",
                f"- **Mais rápido:** {comparison.get('fastest', 'N/A')}",
                "",
            ])

    for item in summary.get("results", []):
        case = item.get("case", {})
        variant = item.get("variant", {})
        result = item.get("summary", {})
        lines.extend([
            f"### {case.get('name', 'N/A')} / {variant.get('name', 'N/A')}",
            "",
            f"- **Query:** {case.get('query', 'N/A')}",
            f"- **Score médio:** {result.get('average_relevance', 0):.2f}",
            f"- **Tempo total:** {result.get('total_duration_seconds', 0):.2f}s",
            f"- **Incluídas:** {result.get('coverage_metrics', {}).get('included', 0)}",
            f"- **Revisão manual:** {result.get('coverage_metrics', {}).get('manual_review_required', 0)}",
            f"- **Clusters:** {result.get('clusters', 0)}",
            f"- **Métricas de etapa:** {result.get('stage_metrics_count', 0)}",
            f"- **Cache LLM:** hits={result.get('llm_cache_stats', {}).get('hits', 0)}, misses={result.get('llm_cache_stats', {}).get('misses', 0)}",
            "",
        ])

    return "\n".join(lines)
