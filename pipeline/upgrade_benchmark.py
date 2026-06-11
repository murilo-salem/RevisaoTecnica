"""
Benchmark dedicado para comparar o pipeline atual com a baseline sem as melhorias do dia.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from datetime import datetime
from statistics import mean
from typing import Any, Callable, Dict, List, Sequence

from models.patent import PatentEvaluation
from pipeline.features import PipelineFeatures
from pipeline.frozen_benchmark import (
    build_frozen_scrapers_from_fixture,
    build_frozen_scrapers_from_run_state,
)
from pipeline.orchestrator import run_agent


ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
STRUCTURAL_FIELDS = (
    "co2_role",
    "storage_role",
    "system_boundary",
    "cycle_type",
    "heat_source_sink",
    "claim_focus",
    "exclusion_category",
)
TODAY_CHANGELOG = (
    {
        "title": "Pivot do modelo padrão para gemma3:27b",
        "why": "Aumentar profundidade técnica na triagem e na síntese sem migrar para API externa.",
        "files": ["config.py", "main.py", "README.md"],
    },
    {
        "title": "Resolução de alias e detecção robusta do modelo ativo",
        "why": "Evitar falsos negativos quando o Ollama expõe variantes compatíveis do mesmo modelo.",
        "files": ["evaluator/llm_evaluator.py"],
    },
    {
        "title": "Ampliação do corpus comparativo para include + review + adjacentes",
        "why": "Whitespace real aparece na borda técnica, não apenas no núcleo incluído.",
        "files": ["evaluator/llm_evaluator.py", "pipeline/orchestrator.py", "analysis_utils.py"],
    },
    {
        "title": "Schema técnico estruturado de papéis do CO2 e do armazenamento",
        "why": "Separar working fluid, meio armazenado, refrigeração e integração de processo com menos ambiguidade.",
        "files": ["models/patent.py", "evaluator/llm_evaluator.py", "report/generator.py"],
    },
    {
        "title": "Rerank para zona cinzenta de triagem",
        "why": "Forçar um segundo passe nos casos limítrofes antes do roteamento final.",
        "files": ["config.py", "evaluator/llm_evaluator.py", "pipeline/orchestrator.py"],
    },
    {
        "title": "Whitespace estruturado em JSON e persistência de artefato",
        "why": "Transformar hipótese de whitespace em matriz de cobertura auditável e reutilizável.",
        "files": ["evaluator/llm_evaluator.py", "pipeline/state.py", "pipeline/orchestrator.py", "report/generator.py"],
    },
    {
        "title": "Cobertura de regressão para os novos mecanismos",
        "why": "Evitar regressão silenciosa no schema técnico, rerank e artefatos do benchmark.",
        "files": ["tests/test_architecture.py", "tests/test_frozen_pipeline.py", "pipeline/frozen_benchmark.py"],
    },
)


@dataclass(frozen=True)
class UpgradeVariant:
    """Variante comparável para o benchmark das melhorias do dia."""

    name: str
    description: str
    features: PipelineFeatures


DEFAULT_VARIANTS: Sequence[UpgradeVariant] = (
    UpgradeVariant(
        name="pre_today_baseline",
        description="Desliga papéis estruturados, rerank de triagem e whitespace estruturado.",
        features=PipelineFeatures(
            enable_structural_roles=False,
            enable_screening_rerank=False,
            enable_whitespace_analysis=False,
        ),
    ),
    UpgradeVariant(
        name="today_updates",
        description="Mantém ativas as melhorias técnicas implementadas hoje.",
        features=PipelineFeatures(),
    ),
)


def _absolute_path(path: str) -> str:
    return os.path.abspath(os.path.join(ROOT_DIR, path))


def _average_relevance(evaluations: List[PatentEvaluation]) -> float:
    scored = [
        evaluation.relevance_score
        for evaluation in evaluations
        if evaluation.screening_decision != "exclude" and not evaluation.llm_error
    ]
    return round(mean(scored), 2) if scored else 0.0


def _structural_summary(evaluations: List[PatentEvaluation]) -> Dict[str, Any]:
    if not evaluations:
        return {
            "filled_fields": 0,
            "total_fields": 0,
            "fill_ratio": 0.0,
            "by_field": {field: 0 for field in STRUCTURAL_FIELDS},
        }

    by_field = {
        field: sum(1 for evaluation in evaluations if getattr(evaluation, field, ""))
        for field in STRUCTURAL_FIELDS
    }
    total_fields = len(evaluations) * len(STRUCTURAL_FIELDS)
    filled_fields = sum(by_field.values())
    return {
        "filled_fields": filled_fields,
        "total_fields": total_fields,
        "fill_ratio": round(filled_fields / total_fields, 3) if total_fields else 0.0,
        "by_field": by_field,
    }


def _top_patent(evaluations: List[PatentEvaluation]) -> str:
    eligible = [
        evaluation for evaluation in evaluations
        if evaluation.screening_decision in {"include", "review"} and not evaluation.llm_error
    ]
    if not eligible:
        return ""
    best = max(
        eligible,
        key=lambda item: (item.relevance_score, item.screening_score, item.confidence),
    )
    return best.patent_id


def _decision_map(evaluations: List[PatentEvaluation]) -> Dict[str, Dict[str, Any]]:
    payload: Dict[str, Dict[str, Any]] = {}
    for evaluation in evaluations:
        patent_id = evaluation.patent_id or evaluation.record_id
        payload[patent_id] = {
            "decision": evaluation.screening_decision,
            "screening_score": round(float(evaluation.screening_score or 0.0), 1),
            "relevance_score": round(float(evaluation.relevance_score or 0.0), 1),
            "co2_role": evaluation.co2_role,
            "storage_role": evaluation.storage_role,
            "claim_focus": evaluation.claim_focus,
            "exclusion_category": evaluation.exclusion_category,
            "rerank_applied": bool(evaluation.rerank_applied),
            "rerank_reason": evaluation.rerank_reason,
        }
    return payload


def _summarize_state(state) -> Dict[str, Any]:
    coverage = state.coverage_metrics or {}
    reranked_items = sum(1 for item in state.evaluations if item.rerank_applied)
    rerank_changed = sum(
        1
        for item in state.evaluations
        if item.rerank_reason and item.rerank_reason != "reranked:decision_confirmed"
    )
    whitespace_candidates = len(state.whitespace_analysis.get("whitespace_candidates", []))

    return {
        "run_id": state.run_id,
        "status": state.status,
        "model": state.model,
        "feature_flags": state.feature_flags,
        "coverage_metrics": coverage,
        "average_relevance": _average_relevance(state.evaluations),
        "total_duration_seconds": round(float(state.total_duration_seconds or 0.0), 3),
        "evaluation_duration_seconds": round(float(state.evaluation_duration_seconds or 0.0), 3),
        "comparative_analysis_duration_seconds": round(float(state.comparative_analysis_duration_seconds or 0.0), 3),
        "rerank_duration_seconds": round(float(state.rerank_duration_seconds or 0.0), 3),
        "reranked_items": reranked_items,
        "rerank_decision_changes": rerank_changed,
        "structural_summary": _structural_summary(state.evaluations),
        "whitespace_status": state.whitespace_analysis.get("status", ""),
        "whitespace_candidates": whitespace_candidates,
        "top_patent": _top_patent(state.evaluations),
        "decision_map": _decision_map(state.evaluations),
        "output_paths": state.output_paths,
    }


def _build_delta(summary: Dict[str, Any]) -> Dict[str, Any]:
    results_by_name = {
        item["variant"]["name"]: item["summary"]
        for item in summary.get("results", [])
    }
    baseline = results_by_name.get("pre_today_baseline")
    updated = results_by_name.get("today_updates")
    if not baseline or not updated:
        return {}

    baseline_coverage = baseline.get("coverage_metrics", {})
    updated_coverage = updated.get("coverage_metrics", {})
    patent_ids = sorted(
        set(baseline.get("decision_map", {}).keys()) | set(updated.get("decision_map", {}).keys())
    )
    decision_changes: List[Dict[str, Any]] = []
    for patent_id in patent_ids:
        before = baseline.get("decision_map", {}).get(patent_id, {})
        after = updated.get("decision_map", {}).get(patent_id, {})
        decision_changes.append(
            {
                "patent_id": patent_id,
                "baseline_decision": before.get("decision", ""),
                "updated_decision": after.get("decision", ""),
                "baseline_screening_score": before.get("screening_score", 0.0),
                "updated_screening_score": after.get("screening_score", 0.0),
                "baseline_relevance_score": before.get("relevance_score", 0.0),
                "updated_relevance_score": after.get("relevance_score", 0.0),
                "rerank_applied": after.get("rerank_applied", False),
                "co2_role": after.get("co2_role", ""),
                "storage_role": after.get("storage_role", ""),
                "claim_focus": after.get("claim_focus", ""),
                "exclusion_category": after.get("exclusion_category", ""),
            }
        )

    return {
        "average_relevance_delta": round(
            float(updated.get("average_relevance", 0.0)) - float(baseline.get("average_relevance", 0.0)),
            2,
        ),
        "included_delta": int(updated_coverage.get("included", 0) or 0) - int(baseline_coverage.get("included", 0) or 0),
        "review_delta": int(updated_coverage.get("review", 0) or 0) - int(baseline_coverage.get("review", 0) or 0),
        "excluded_delta": int(updated_coverage.get("excluded", 0) or 0) - int(baseline_coverage.get("excluded", 0) or 0),
        "manual_review_delta": int(updated_coverage.get("manual_review_required", 0) or 0) - int(baseline_coverage.get("manual_review_required", 0) or 0),
        "total_duration_delta_seconds": round(
            float(updated.get("total_duration_seconds", 0.0)) - float(baseline.get("total_duration_seconds", 0.0)),
            3,
        ),
        "rerank_items_delta": int(updated.get("reranked_items", 0) or 0) - int(baseline.get("reranked_items", 0) or 0),
        "structural_fill_ratio_delta": round(
            float(updated.get("structural_summary", {}).get("fill_ratio", 0.0))
            - float(baseline.get("structural_summary", {}).get("fill_ratio", 0.0)),
            3,
        ),
        "whitespace_candidates_delta": int(updated.get("whitespace_candidates", 0) or 0) - int(baseline.get("whitespace_candidates", 0) or 0),
        "decision_changes": decision_changes,
    }


def _load_optional_json(path: str) -> Dict[str, Any]:
    if not path:
        return {}
    absolute = os.path.abspath(path)
    if not os.path.exists(absolute):
        return {}
    with open(absolute, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data if isinstance(data, dict) else {}


def _build_model_recommendation(
    default_model: str,
    model_comparison: Dict[str, Any],
) -> Dict[str, Any]:
    recommendation = {
        "recommended_model": default_model,
        "keep_current_default": True,
        "rationale": "Sem comparativo externo adicional; manter o modelo configurado.",
        "evidence": {},
    }
    if not model_comparison:
        return recommendation

    results = {
        item.get("model", ""): item
        for item in model_comparison.get("results", [])
        if isinstance(item, dict)
    }
    gemma = results.get("gemma3:27b")
    qwen = results.get("qwen2.5:32b")
    if not gemma or not qwen:
        recommendation["rationale"] = "Comparativo externo sem os dois modelos esperados; manter o default atual."
        recommendation["evidence"] = {"comparison_file": model_comparison.get("summary_paths", {}) or model_comparison.get("query", "")}
        return recommendation

    same_routing = (
        gemma.get("included") == qwen.get("included")
        and gemma.get("review") == qwen.get("review")
        and gemma.get("excluded") == qwen.get("excluded")
        and gemma.get("manual_review_required") == qwen.get("manual_review_required")
        and gemma.get("top_patent") == qwen.get("top_patent")
    )
    gemma_time = float(gemma.get("total_duration_seconds", 0.0) or 0.0)
    qwen_time = float(qwen.get("total_duration_seconds", 0.0) or 0.0)
    recommendation["evidence"] = {
        "gemma3:27b_total_duration_seconds": round(gemma_time, 3),
        "qwen2.5:32b_total_duration_seconds": round(qwen_time, 3),
        "same_routing": same_routing,
        "gemma_top_patent": gemma.get("top_patent", ""),
        "qwen_top_patent": qwen.get("top_patent", ""),
    }
    if same_routing and gemma_time and qwen_time and gemma_time < qwen_time:
        recommendation["recommended_model"] = "gemma3:27b"
        recommendation["keep_current_default"] = default_model == "gemma3:27b"
        recommendation["rationale"] = (
            "Manter gemma3:27b como default. No corpus comparado, ele entregou o mesmo roteamento agregado "
            "e o mesmo top patent do qwen2.5:32b, mas com menor tempo total."
        )
        return recommendation

    recommendation["recommended_model"] = default_model
    recommendation["keep_current_default"] = True
    recommendation["rationale"] = (
        "O comparativo externo não mostrou vantagem operacional suficiente para trocar o default atual."
    )
    return recommendation


def _build_markdown_report(summary: Dict[str, Any]) -> str:
    delta = summary.get("delta", {})
    model_rec = summary.get("model_recommendation", {})
    lines = [
        "# Relatório das Atualizações Técnicas de Hoje",
        "",
        f"- **Gerado em:** {summary.get('generated_at', 'N/A')}",
        f"- **Query:** {summary.get('query', 'N/A')}",
        f"- **Modelo avaliado:** {summary.get('model', 'N/A')}",
        f"- **Corpus congelado:** {summary.get('corpus_run_state', 'N/A') or summary.get('corpus_fixture', 'N/A') or 'N/A'}",
        "",
        "## Escopo do Benchmark",
        "",
        "Este benchmark isola as mudanças técnicas ligadas a papéis estruturados, rerank de triagem e whitespace estruturado.",
        "Mudanças de infraestrutura, como a resolução de alias do modelo e o pivot do default para `gemma3:27b`, entram no relatório qualitativo abaixo, mas não são desligadas no A/B.",
        "",
        "## O Que Fizemos Hoje",
        "",
    ]

    for item in TODAY_CHANGELOG:
        lines.extend([
            f"### {item['title']}",
            "",
            f"- **Por que:** {item['why']}",
            "- **Arquivos:**",
        ])
        for rel_path in item["files"]:
            abs_path = _absolute_path(rel_path)
            lines.append(f"  - [{rel_path}]({abs_path})")
        lines.append("")

    lines.extend([
        "## Resultado A/B no Mesmo Corpus",
        "",
        "| Variante | Score médio | Tempo total | Incluídas | Review | Excluídas | Rerank | Fill estrutural | Whitespaces |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ])

    for item in summary.get("results", []):
        variant = item.get("variant", {})
        result = item.get("summary", {})
        coverage = result.get("coverage_metrics", {})
        lines.append(
            f"| {variant.get('name', 'N/A')} | {result.get('average_relevance', 0):.2f} | "
            f"{result.get('total_duration_seconds', 0):.2f}s | "
            f"{coverage.get('included', 0)} | {coverage.get('review', 0)} | {coverage.get('excluded', 0)} | "
            f"{result.get('reranked_items', 0)} | {result.get('structural_summary', {}).get('fill_ratio', 0):.3f} | "
            f"{result.get('whitespace_candidates', 0)} |"
        )
    lines.append("")

    lines.extend([
        "## Leitura das Melhorias",
        "",
        f"- **Delta de score médio:** {delta.get('average_relevance_delta', 0):+.2f}",
        f"- **Delta de tempo total:** {delta.get('total_duration_delta_seconds', 0):+.2f}s",
        f"- **Delta de itens rerankeados:** {delta.get('rerank_items_delta', 0):+d}",
        f"- **Delta de cobertura estrutural:** {delta.get('structural_fill_ratio_delta', 0):+.3f}",
        f"- **Delta de candidatos de whitespace:** {delta.get('whitespace_candidates_delta', 0):+d}",
        "",
        "## Diferenças por Patente",
        "",
        "| Patente | Baseline | Atual | Score triagem | Relevância | Rerank | CO2 role | Storage role | Claim focus |",
        "|---|---|---|---:|---:|---|---|---|---|",
    ])

    for row in delta.get("decision_changes", []):
        lines.append(
            f"| {row.get('patent_id', 'N/A')} | {row.get('baseline_decision', '')} | {row.get('updated_decision', '')} | "
            f"{row.get('baseline_screening_score', 0):.1f} -> {row.get('updated_screening_score', 0):.1f} | "
            f"{row.get('baseline_relevance_score', 0):.1f} -> {row.get('updated_relevance_score', 0):.1f} | "
            f"{'sim' if row.get('rerank_applied') else 'não'} | "
            f"{row.get('co2_role', '') or 'N/A'} | "
            f"{row.get('storage_role', '') or 'N/A'} | "
            f"{row.get('claim_focus', '') or 'N/A'} |"
        )
    lines.append("")

    lines.extend([
        "## Recomendação de Modelo",
        "",
        f"- **Modelo recomendado:** {model_rec.get('recommended_model', 'N/A')}",
        f"- **Manter default atual:** {'sim' if model_rec.get('keep_current_default') else 'não'}",
        f"- **Justificativa:** {model_rec.get('rationale', '')}",
    ])
    evidence = model_rec.get("evidence", {})
    if evidence:
        lines.extend([
            f"- **Tempo gemma3:27b:** {evidence.get('gemma3:27b_total_duration_seconds', 'N/A')}",
            f"- **Tempo qwen2.5:32b:** {evidence.get('qwen2.5:32b_total_duration_seconds', 'N/A')}",
            f"- **Mesmo roteamento agregado:** {evidence.get('same_routing', 'N/A')}",
        ])
    lines.append("")

    return "\n".join(lines)


def run_today_upgrade_benchmark(
    query: str,
    max_results: int,
    model: str,
    output_dir: str,
    corpus_run_state: str = "",
    corpus_fixture: str = "",
    model_comparison_summary: str = "",
    variants: Sequence[UpgradeVariant] = DEFAULT_VARIANTS,
    scrapers=None,
    evaluator_factory: Callable[..., Any] | None = None,
) -> Dict[str, Any]:
    """Executa benchmark A/B entre baseline sem melhorias do dia e pipeline atual."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    suite_root = os.path.join(output_dir, f"today_upgrade_{timestamp}")
    os.makedirs(suite_root, exist_ok=True)

    if scrapers is None:
        if corpus_run_state:
            scrapers = build_frozen_scrapers_from_run_state(corpus_run_state)
        elif corpus_fixture:
            scrapers = build_frozen_scrapers_from_fixture(corpus_fixture)
        else:
            raise ValueError("Informe corpus_run_state ou corpus_fixture para congelar o corpus do benchmark.")

    suite_results: List[Dict[str, Any]] = []
    for variant in variants:
        variant_dir = os.path.join(suite_root, variant.name)
        os.makedirs(variant_dir, exist_ok=True)
        state = run_agent(
            query=query,
            max_results=max_results,
            model=model,
            output_dir=variant_dir,
            features=variant.features,
            scrapers=scrapers,
            evaluator_factory=evaluator_factory,
        )
        suite_results.append(
            {
                "variant": {
                    "name": variant.name,
                    "description": variant.description,
                    "features": variant.features.to_dict(),
                },
                "summary": _summarize_state(state),
            }
        )

    model_comparison = _load_optional_json(model_comparison_summary)
    summary = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "query": query,
        "max_results": max_results,
        "model": model,
        "suite_root": os.path.abspath(suite_root),
        "corpus_run_state": os.path.abspath(corpus_run_state) if corpus_run_state else "",
        "corpus_fixture": os.path.abspath(corpus_fixture) if corpus_fixture else "",
        "variants": [
            {
                "name": variant.name,
                "description": variant.description,
                "features": variant.features.to_dict(),
            }
            for variant in variants
        ],
        "today_changes": [
            {
                "title": item["title"],
                "why": item["why"],
                "files": [_absolute_path(rel_path) for rel_path in item["files"]],
            }
            for item in TODAY_CHANGELOG
        ],
        "results": suite_results,
        "model_comparison_summary": os.path.abspath(model_comparison_summary) if model_comparison_summary else "",
    }
    summary["delta"] = _build_delta(summary)
    summary["model_recommendation"] = _build_model_recommendation(model, model_comparison)

    summary_path = os.path.join(suite_root, "today_upgrade_summary.json")
    report_path = os.path.join(suite_root, "today_upgrade_report.md")
    summary["summary_paths"] = {
        "json": os.path.abspath(summary_path),
        "markdown": os.path.abspath(report_path),
    }

    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(_build_markdown_report(summary))

    return summary
