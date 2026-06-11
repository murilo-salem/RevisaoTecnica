"""
Gerador de relatórios de análise de patentes.

Gera relatórios em Markdown e JSON com os resultados
da busca e avaliação de patentes.
"""

import json
import logging
import os
from datetime import datetime
from typing import List, Tuple

from analysis_utils import has_substantive_comparative_analysis
import config
from logging_utils import log_event
from models.patent import Patent, PatentEvaluation

logger = logging.getLogger(__name__)


def _entity_key(record_id: str, patent_id: str) -> str:
    return record_id or patent_id or ""


def _display_patent_id(patent: Patent) -> str:
    return patent.patent_id or patent.record_id or "N/A"


def _evaluation_map(evaluations: List[PatentEvaluation]) -> dict:
    return {
        _entity_key(evaluation.record_id, evaluation.patent_id): evaluation
        for evaluation in evaluations
        if _entity_key(evaluation.record_id, evaluation.patent_id)
    }


def _pair_patents_with_evaluations(
    patents: List[Patent],
    evaluations: List[PatentEvaluation],
) -> List[Tuple[Patent, PatentEvaluation]]:
    eval_map = _evaluation_map(evaluations)
    pairs = []
    for patent in patents:
        evaluation = eval_map.get(_entity_key(patent.record_id, patent.patent_id))
        if evaluation is not None:
            pairs.append((patent, evaluation))
    return pairs


class ReportGenerator:
    """Gerador de relatórios de análise de patentes."""

    def __init__(self, output_dir: str = None):
        self.output_dir = output_dir or config.OUTPUT_DIR
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_report(
        self,
        query: str,
        patents: List[Patent],
        evaluations: List[PatentEvaluation],
        comparative_analysis: str = "",
        run_metadata: dict = None,
    ) -> Tuple[str, str]:
        """
        Gera relatórios completos em Markdown e JSON.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_query = "".join(c if c.isalnum() or c in " -_" else "" for c in query)
        safe_query = safe_query.replace(" ", "_")[:50]

        md_path = os.path.join(self.output_dir, f"patentes_{safe_query}_{timestamp}.md")
        json_path = os.path.join(self.output_dir, f"patentes_{safe_query}_{timestamp}.json")

        return self.write_report_files(
            md_path,
            json_path,
            query,
            patents,
            evaluations,
            comparative_analysis,
            run_metadata=run_metadata,
        )

    def write_report_files(
        self,
        md_path: str,
        json_path: str,
        query: str,
        patents: List[Patent],
        evaluations: List[PatentEvaluation],
        comparative_analysis: str = "",
        run_metadata: dict = None,
    ) -> Tuple[str, str]:
        """Escreve ou reescreve os relatórios em caminhos fixos."""

        md_content = self._generate_markdown(
            query,
            patents,
            evaluations,
            comparative_analysis,
            run_metadata=run_metadata,
        )
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(md_content)

        json_content = self._generate_json(
            query,
            patents,
            evaluations,
            comparative_analysis,
            run_metadata=run_metadata,
        )
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(json_content, f, ensure_ascii=False, indent=2)

        log_event(
            logger,
            logging.INFO,
            "report_file_written",
            format="markdown",
            path=md_path,
            query=query,
            patents=len(patents),
            evaluations=len(evaluations),
        )
        log_event(
            logger,
            logging.INFO,
            "report_file_written",
            format="json",
            path=json_path,
            query=query,
            patents=len(patents),
            evaluations=len(evaluations),
        )

        return md_path, json_path

    def _generate_markdown(
        self,
        query: str,
        patents: List[Patent],
        evaluations: List[PatentEvaluation],
        comparative_analysis: str,
        run_metadata: dict = None,
    ) -> str:
        """Gera relatório em formato Markdown."""
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        model_name = (
            run_metadata.get("model", config.OLLAMA_MODEL)
            if run_metadata
            else config.OLLAMA_MODEL
        )
        protocol = run_metadata.get("protocol", {}) if run_metadata else {}
        coverage = run_metadata.get("coverage_metrics", {}) if run_metadata else {}
        manual_review_queue = run_metadata.get("manual_review_queue", []) if run_metadata else []
        prisma_flow = run_metadata.get("prisma_flow", {}) if run_metadata else {}
        thematic_clusters = run_metadata.get("thematic_clusters", {}) if run_metadata else {}
        scraper_diagnostics = run_metadata.get("scraper_diagnostics", {}) if run_metadata else {}
        config_snapshot = run_metadata.get("config_snapshot", {}) if run_metadata else {}
        snapshot_hash = run_metadata.get("snapshot_hash", "") if run_metadata else ""
        feature_flags = run_metadata.get("feature_flags", {}) if run_metadata else {}
        writing_context = run_metadata.get("writing_context", {}) if run_metadata else {}
        stage_metrics = run_metadata.get("stage_metrics", []) if run_metadata else []
        llm_cache_stats = run_metadata.get("llm_cache_stats", {}) if run_metadata else {}
        llm_telemetry = run_metadata.get("llm_telemetry", {}) if run_metadata else {}
        observability_metrics = run_metadata.get("observability_metrics", {}) if run_metadata else {}
        draft_status = self._draft_status(patents, evaluations, comparative_analysis)

        lines = [
            "# 📋 Relatório de Análise de Patentes",
            "",
            f"**Data:** {timestamp}",
            f"**Busca:** `{query}`",
            f"**Total de patentes encontradas:** {len(patents)}",
            f"**Modelo de avaliação:** {model_name}",
            "",
            "---",
            "",
            "## 🧭 Protocolo Metodológico",
            "",
        ]

        if protocol:
            thresholds = protocol.get("thresholds", {})
            criteria = protocol.get("criteria", {})
            lines.extend([
                f"- **Versão:** {protocol.get('version', 'N/A')}",
                f"- **Fontes:** {', '.join(protocol.get('sources', [])) or 'N/A'}",
                f"- **Etapas:** {', '.join(protocol.get('stages', [])) or 'N/A'}",
                f"- **Threshold inclusão:** {thresholds.get('include_score', 'N/A')}",
                f"- **Threshold revisão:** {thresholds.get('review_score', 'N/A')}",
                f"- **Máximo em revisão manual:** {thresholds.get('max_items_for_manual_review', 'N/A')}",
                "",
            ])
            if criteria:
                lines.extend([
                    "**Critérios de inclusão**",
                ])
                for item in criteria.get("include", []):
                    lines.append(f"- {item}")
                lines.append("")
                lines.append("**Critérios de exclusão**")
                for item in criteria.get("exclude", []):
                    lines.append(f"- {item}")
                lines.append("")
        else:
            lines.extend(["Protocolo não disponível.", ""])

        if coverage:
            lines.extend([
                "## 📐 Cobertura e Seleção",
                "",
                f"- **Total bruto coletado:** {coverage.get('raw_scraped', 0)}",
                f"- **Patentes únicas:** {coverage.get('unique_patents', 0)}",
                f"- **Duplicatas removidas:** {coverage.get('duplicates_removed', 0)}",
                f"- **Triadas:** {coverage.get('screened', 0)}",
                f"- **Incluídas:** {coverage.get('included', 0)}",
                f"- **Em revisão manual:** {coverage.get('review', 0)}",
                f"- **Excluídas:** {coverage.get('excluded', 0)}",
                f"- **Extrações completas:** {coverage.get('full_extractions', 0)}",
                f"- **Sem abstract/snippet:** {coverage.get('missing_abstract', 0)}",
                f"- **Sem ID:** {coverage.get('missing_id', 0)}",
                f"- **Identidade por conteúdo:** {coverage.get('records_with_content_identity', 0)}",
                f"- **Identidade fallback:** {coverage.get('records_with_fallback_identity', 0)}",
                f"- **Duplicatas por família removidas:** {coverage.get('family_duplicates_removed', 0)}",
                f"- **Falhas de triagem LLM:** {coverage.get('llm_screening_failures', 0)}",
                f"- **Falhas totais LLM:** {coverage.get('llm_total_failures', 0)}",
                "",
            ])

        if prisma_flow:
            flow = prisma_flow.get("flow", {})
            lines.extend([
                "## 🧭 Fluxo PRISMA-Like",
                "",
                f"- **Identificação:** {flow.get('identification', {}).get('raw_records', 0)} bruto(s), {flow.get('identification', {}).get('unique_records', 0)} único(s), {flow.get('identification', {}).get('duplicates_removed', 0)} duplicata(s) removida(s)",
                f"- **Triagem:** {flow.get('screening', {}).get('screened', 0)} triado(s), {flow.get('screening', {}).get('included', 0)} incluído(s), {flow.get('screening', {}).get('review', 0)} em revisão, {flow.get('screening', {}).get('excluded', 0)} excluído(s)",
                f"- **Elegibilidade:** {flow.get('eligibility', {}).get('full_extractions', 0)} extração(ões) completa(s), {flow.get('eligibility', {}).get('manual_review_required', 0)} revisão(ões) manual(is), {flow.get('eligibility', {}).get('manual_review_deferred', 0)} adiada(s)",
                f"- **Cobertura:** {flow.get('coverage', {}).get('missing_abstract', 0)} sem abstract/snippet, {flow.get('coverage', {}).get('missing_id', 0)} sem ID",
                f"- **Síntese:** {flow.get('synthesis', {}).get('analyzed_records', 0)} registro(s) analisado(s)",
                "",
            ])

        if thematic_clusters and thematic_clusters.get("clusters"):
            lines.extend([
                "## 🧩 Síntese Temática",
                "",
            ])
            for cluster in thematic_clusters["clusters"]:
                lines.extend([
                    f"### {cluster['cluster']}",
                    "",
                    f"- **Patentes:** {cluster['count']}",
                    f"- **Score médio:** {cluster['average_score']:.2f}/10",
                    f"- **Confiança média:** {cluster['average_confidence']:.2f}",
                    f"- **Evidências citadas:** {cluster['evidence_count']}",
                    f"- **IDs:** {', '.join(cluster['patent_ids']) or 'N/A'}",
                    "",
                ])

        if writing_context:
            lines.extend([
                "## 🧠 Contexto Compartilhado",
                "",
                f"- **Top patentes no contexto:** {len(writing_context.get('top_patents', []))}",
                f"- **Clusters no contexto:** {writing_context.get('thematic_clusters', {}).get('total_clusters', 0)}",
                f"- **Roteamento agregado:** {len(writing_context.get('route_summary', {}))} rota(s)",
                f"- **Slots ativos:** {', '.join(writing_context.get('slot_policy', {}).get('slots', [])) or 'N/A'}",
                "",
            ])

        if stage_metrics:
            lines.extend([
                "## ⏱️ Métricas por Etapa",
                "",
                "| Etapa | Status | Duração | Itens | Detalhes |",
                "|---|---|---:|---:|---|",
            ])
            for metric in stage_metrics:
                lines.append(
                    f"| {metric.get('stage', 'N/A')} | {metric.get('status', 'N/A')} | "
                    f"{float(metric.get('duration_seconds', 0) or 0):.2f}s | "
                    f"{metric.get('items_processed', 0)} | "
                    f"{metric.get('detail', '')} |"
                )
            lines.append("")

        if scraper_diagnostics:
            lines.extend([
                "## 🌐 Diagnósticos de Coleta",
                "",
            ])
            for source_name, items in scraper_diagnostics.items():
                lines.append(f"### {source_name}")
                lines.append("")
                if items:
                    for item in items:
                        lines.append(
                            f"- **{item.get('kind', 'signal')}**: {item.get('detail', '')}"
                        )
                else:
                    lines.append("- Nenhum sinal relevante detectado.")
                lines.append("")

        if llm_telemetry:
            lines.extend([
                "## 📡 Telemetria do LLM",
                "",
                f"- **Degradado:** {'sim' if llm_telemetry.get('degraded') else 'não'}",
                f"- **Falhas totais:** {llm_telemetry.get('total_failures', 0)}",
                f"- **Falhas consecutivas:** {llm_telemetry.get('consecutive_failures', 0)}",
                "",
            ])
            for operation, metric in llm_telemetry.get("operations", {}).items():
                lines.extend([
                    f"### {operation}",
                    "",
                    f"- **Chamadas:** {metric.get('calls', 0)}",
                    f"- **Sucessos:** {metric.get('successes', 0)}",
                    f"- **Falhas:** {metric.get('failures', 0)}",
                    f"- **Retries:** {metric.get('retries', 0)}",
                    f"- **Cache hits:** {metric.get('cache_hits', 0)}",
                    f"- **Pulos por degradação:** {metric.get('degraded_skips', 0)}",
                    f"- **Latência média:** {metric.get('average_duration_seconds', 0)}s",
                    f"- **Latência máxima:** {metric.get('max_duration_seconds', 0)}s",
                    "",
                ])

        if observability_metrics:
            route_metrics = observability_metrics.get("routes", {})
            source_metrics = observability_metrics.get("sources", {})
            failure_metrics = observability_metrics.get("failures", {})
            lines.extend([
                "## 🔎 Observabilidade Estruturada",
                "",
            ])
            if route_metrics:
                lines.extend([
                    "### Rotas",
                    "",
                ])
                for route_name, metric in route_metrics.items():
                    lines.append(
                        f"- **{route_name}**: total={metric.get('count', 0)}, "
                        f"include={metric.get('include', 0)}, review={metric.get('review', 0)}, "
                        f"exclude={metric.get('exclude', 0)}, llm_errors={metric.get('llm_errors', 0)}"
                    )
                lines.append("")

            if source_metrics:
                lines.extend([
                    "### Fontes",
                    "",
                ])
                for source_name, metric in source_metrics.items():
                    diagnostic_counts = metric.get("diagnostic_counts", {})
                    diagnostic_text = ", ".join(
                        f"{kind}={count}" for kind, count in sorted(diagnostic_counts.items())
                    ) or "nenhum"
                    lines.append(
                        f"- **{source_name}**: bruto={metric.get('raw_results', 0)}, "
                        f"duração={float(metric.get('duration_seconds', 0) or 0):.2f}s, "
                        f"diagnósticos={diagnostic_text}"
                    )
                lines.append("")

            if failure_metrics:
                lines.extend([
                    "### Falhas",
                    "",
                    f"- **Erros de execução:** {failure_metrics.get('run_errors', 0)}",
                    f"- **Registros com erro de LLM:** {failure_metrics.get('records_with_llm_error', 0)}",
                    f"- **Falhas totais do LLM:** {failure_metrics.get('llm_total_failures', 0)}",
                ])
                llm_by_operation = failure_metrics.get("llm_by_operation", {})
                if llm_by_operation:
                    operation_text = ", ".join(
                        f"{operation}(falhas={metric.get('failures', 0)}, retries={metric.get('retries', 0)}, skips={metric.get('degraded_skips', 0)})"
                        for operation, metric in sorted(llm_by_operation.items())
                    )
                    lines.append(f"- **LLM por operação:** {operation_text}")
                scraper_failures = failure_metrics.get("scraper_diagnostics_by_kind", {})
                if scraper_failures:
                    scraper_text = ", ".join(
                        f"{kind}={count}" for kind, count in sorted(scraper_failures.items())
                    )
                    lines.append(f"- **Scraper por tipo de sinal:** {scraper_text}")
                lines.append("")

        lines.extend([
            "## 📊 Resumo Executivo",
            "",
        ])

        if patents and evaluations:
            paired = _pair_patents_with_evaluations(patents, evaluations)
            paired.sort(key=lambda x: x[1].relevance_score, reverse=True)

            scored = [
                e for e in evaluations
                if e.screening_decision == "include" and not e.llm_error
            ]
            avg_score = sum(e.relevance_score for e in scored) / len(scored) if scored else 0
            lines.append(f"**Score médio de relevância:** {avg_score:.1f}/10\n")

            lines.extend([
                "| # | Patente | Score | Inovação | Domínio |",
                "|---|---------|-------|----------|---------|",
            ])

            for i, (patent, evaluation) in enumerate(paired, 1):
                score_emoji = "🟢" if evaluation.relevance_score >= 7 else (
                    "🟡" if evaluation.relevance_score >= 4 else "🔴"
                )
                status = evaluation.screening_decision or "N/A"
                lines.append(
                    f"| {i} | [{_display_patent_id(patent)}]({patent.url}) — "
                    f"{patent.title[:60]}{'...' if len(patent.title) > 60 else ''} | "
                    f"{score_emoji} {evaluation.relevance_score:.1f} ({status}) | "
                    f"{evaluation.innovation_level or 'N/A'} | "
                    f"{evaluation.technical_domain or 'N/A'} |"
                )

            lines.extend(["", "---", ""])

        lines.extend([
            "## 🔍 Análise Detalhada das Patentes",
            "",
        ])

        eval_map = _evaluation_map(evaluations)
        patent_map = {
            patent.record_id: patent
            for patent in patents
        }

        for i, patent in enumerate(patents, 1):
            evaluation = eval_map.get(
                _entity_key(patent.record_id, patent.patent_id),
                PatentEvaluation(record_id=patent.record_id, patent_id=patent.patent_id),
            )
            inventors_str = ", ".join(patent.inventors) if patent.inventors else "N/A"
            evidence = evaluation.evidence_snippets or []

            lines.extend([
                f"### {i}. {patent.title}",
                "",
                "| Campo | Valor |",
                "|-------|-------|",
                f"| **Record ID** | `{patent.record_id or 'N/A'}` |",
                f"| **Family ID** | `{patent.family_id or 'N/A'}` |",
                f"| **ID** | `{patent.patent_id}` |",
                f"| **Inventores** | {inventors_str} |",
                f"| **Titular** | {patent.assignee or 'N/A'} |",
                f"| **Data** | {patent.publication_date or patent.filing_date or 'N/A'} |",
                f"| **Fonte** | {patent.source} |",
                f"| **URL** | [{_display_patent_id(patent)}]({patent.url}) |",
                f"| **Triagem** | {evaluation.screening_decision or 'N/A'} |",
                f"| **Rota** | {evaluation.analysis_route or 'N/A'} |",
                f"| **Motivo da rota** | {evaluation.route_reason or 'N/A'} |",
                f"| **Score de Triagem** | {evaluation.screening_score:.1f}/10 |",
                f"| **Score de Relevância** | {evaluation.relevance_score:.1f}/10 |",
                f"| **Nível de Inovação** | {evaluation.innovation_level or 'N/A'} |",
                f"| **Domínio Técnico** | {evaluation.technical_domain or 'N/A'} |",
                f"| **Cluster Temático** | {evaluation.thematic_cluster or 'N/A'} |",
                f"| **Papel do CO2** | {evaluation.co2_role or 'N/A'} |",
                f"| **Papel do Armazenamento** | {evaluation.storage_role or 'N/A'} |",
                f"| **Limite Sistêmico** | {evaluation.system_boundary or 'N/A'} |",
                f"| **Tipo de Ciclo** | {evaluation.cycle_type or 'N/A'} |",
                f"| **Fonte/Sumidouro Térmico** | {evaluation.heat_source_sink or 'N/A'} |",
                f"| **Foco das Claims** | {evaluation.claim_focus or 'N/A'} |",
                f"| **Categoria de Exclusão** | {evaluation.exclusion_category or 'N/A'} |",
                f"| **Confiança** | {evaluation.confidence:.2f} |",
                f"| **Rerank Aplicado** | {'Sim' if evaluation.rerank_applied else 'Não'} |",
                f"| **Motivo do Rerank** | {evaluation.rerank_reason or 'N/A'} |",
                f"| **Revisão Manual** | {'Sim' if evaluation.manual_review_required else 'Não'} |",
                f"| **Erro LLM** | {evaluation.llm_error or 'N/A'} |",
                "",
            ])

            if patent.abstract or patent.snippet:
                lines.extend([
                    "**Abstract:**",
                    f"> {patent.abstract or patent.snippet}",
                    "",
                ])

            if evaluation.summary:
                lines.extend([
                    "**Avaliação do LLM:**",
                    evaluation.summary,
                    "",
                ])

            if evaluation.problem_statement or evaluation.solution_summary:
                lines.extend([
                    "**Extração Estruturada:**",
                    f"- **Problema:** {evaluation.problem_statement or 'N/A'}",
                    f"- **Solução:** {evaluation.solution_summary or 'N/A'}",
                    f"- **Maturidade:** {evaluation.maturity_level or 'N/A'}",
                    "",
                ])

            if evaluation.key_findings:
                lines.append("**Achados-chave:**")
                for finding in evaluation.key_findings:
                    lines.append(f"- {finding}")
                lines.append("")

            if evaluation.claimed_advantages:
                lines.append("**Vantagens alegadas:**")
                for advantage in evaluation.claimed_advantages:
                    lines.append(f"- {advantage}")
                lines.append("")

            if evaluation.limitations:
                lines.append("**Limitações:**")
                for limitation in evaluation.limitations:
                    lines.append(f"- {limitation}")
                lines.append("")

            if evaluation.potential_applications:
                lines.append("**Aplicações potenciais:**")
                for app in evaluation.potential_applications:
                    lines.append(f"- {app}")
                lines.append("")

            if evidence:
                lines.append("**Evidências citadas:**")
                for snippet in evidence:
                    lines.append(f"> {snippet}")
                lines.append("")

            lines.extend(["---", ""])

        if manual_review_queue:
            lines.extend([
                "## 🧾 Fila de Revisão Manual",
                "",
            ])
            for item in manual_review_queue:
                record_id = item.get("record_id", "")
                patent = patent_map.get(record_id)
                if patent:
                    lines.append(
                        f"- {record_id} ({_display_patent_id(patent)}) | "
                        f"rota={item.get('route', 'N/A')} | "
                        f"motivo={item.get('reason', 'N/A')} | "
                        f"erro_llm={item.get('llm_error', 'N/A') or 'N/A'}"
                    )
                else:
                    lines.append(
                        f"- {record_id} | rota={item.get('route', 'N/A')} | "
                        f"motivo={item.get('reason', 'N/A')}"
                    )
            lines.extend(["", "---", ""])

        if comparative_analysis:
            lines.extend([
                "## 🔬 Análise Comparativa",
                "",
                comparative_analysis,
                "",
                "---",
                "",
            ])

        whitespace_analysis = run_metadata.get("whitespace_analysis", {}) if run_metadata else {}
        if whitespace_analysis and whitespace_analysis.get("status") == "ok":
            lines.extend([
                "## 🧭 Matriz de Whitespaces",
                "",
            ])
            summary = whitespace_analysis.get("corpus_summary", {})
            lines.extend([
                f"- **Patentes selecionadas:** {summary.get('selected_patents', 0)}",
                f"- **Núcleo:** {summary.get('core', 0)}",
                f"- **Fronteira:** {summary.get('frontier', 0)}",
                f"- **Adjacência:** {summary.get('adjacent', 0)}",
                "",
            ])
            for candidate in whitespace_analysis.get("whitespace_candidates", []):
                lines.append(
                    f"- **{candidate.get('opportunity', 'N/A')}**: {candidate.get('rationale', 'N/A')} "
                    f"[core={', '.join(candidate.get('core_ids', [])) or 'N/A'} | "
                    f"frontier={', '.join(candidate.get('frontier_ids', [])) or 'N/A'} | "
                    f"adjacent={', '.join(candidate.get('adjacent_ids', [])) or 'N/A'}]"
                )
            lines.extend(["", "---", ""])

        lines.extend([
            "## ℹ️ Informações do Sistema",
            "",
            f"- **Gerado por:** Agente de Web Scraping de Patentes",
            f"- **Modelo LLM:** {model_name}",
            f"- **Data de geração:** {timestamp}",
            f"- **Query de busca:** `{query}`",
        ])

        if run_metadata:
            lines.extend([
                f"- **Status da execução:** {run_metadata.get('status', 'N/A')}",
                f"- **Tempo total:** {run_metadata.get('total_duration_seconds', 0):.1f}s",
                f"- **LLM disponível:** {'sim' if run_metadata.get('llm_available') else 'não'}",
            ])

            errors = run_metadata.get("errors") or []
            if errors:
                lines.append(f"- **Erros registrados:** {len(errors)}")

            if manual_review_queue:
                lines.append(f"- **Fila de revisão manual:** {len(manual_review_queue)} itens")

            if snapshot_hash:
                lines.append(f"- **Snapshot hash:** `{snapshot_hash}`")

            if feature_flags:
                enabled = ", ".join(
                    key
                    for key, value in feature_flags.items()
                    if value
                ) or "nenhum"
                disabled = ", ".join(
                    key
                    for key, value in feature_flags.items()
                    if not value
                ) or "nenhum"
                lines.append(f"- **Features habilitadas:** {enabled}")
                lines.append(f"- **Features desabilitadas:** {disabled}")

            if config_snapshot:
                lines.append(
                    f"- **Versão do pipeline:** {config_snapshot.get('pipeline_version', 'N/A')}"
                )
                thresholds = config_snapshot.get("thresholds", {})
                if thresholds:
                    lines.append(
                        f"- **Thresholds snapshot:** include={thresholds.get('include', 'N/A')}, review={thresholds.get('review', 'N/A')}"
                    )
            if llm_cache_stats:
                lines.append(
                    f"- **Cache LLM:** {llm_cache_stats.get('hits', 0)} hits, {llm_cache_stats.get('misses', 0)} misses, {llm_cache_stats.get('entries', 0)} entradas"
                )

            lines.append(f"- **Status do rascunho:** {draft_status['status']}")
            if draft_status.get("warnings"):
                lines.append(f"- **Avisos do rascunho:** {len(draft_status['warnings'])}")

        return "\n".join(lines)

    def _generate_json(
        self,
        query: str,
        patents: List[Patent],
        evaluations: List[PatentEvaluation],
        comparative_analysis: str,
        run_metadata: dict = None,
    ) -> dict:
        """Gera relatório em formato JSON."""
        eval_map = _evaluation_map(evaluations)
        scored = [
            e for e in evaluations
            if e.screening_decision == "include" and not e.llm_error
        ]
        prisma_flow = run_metadata.get("prisma_flow", {}) if run_metadata else {}
        thematic_clusters = run_metadata.get("thematic_clusters", {}) if run_metadata else {}
        config_snapshot = run_metadata.get("config_snapshot", {}) if run_metadata else {}
        snapshot_hash = run_metadata.get("snapshot_hash", "") if run_metadata else ""
        writing_context = run_metadata.get("writing_context", {}) if run_metadata else {}
        stage_metrics = run_metadata.get("stage_metrics", []) if run_metadata else []
        llm_cache_stats = run_metadata.get("llm_cache_stats", {}) if run_metadata else {}
        llm_telemetry = run_metadata.get("llm_telemetry", {}) if run_metadata else {}
        scraper_diagnostics = run_metadata.get("scraper_diagnostics", {}) if run_metadata else {}
        observability_metrics = run_metadata.get("observability_metrics", {}) if run_metadata else {}
        whitespace_analysis = run_metadata.get("whitespace_analysis", {}) if run_metadata else {}
        draft_status = self._draft_status(patents, evaluations, comparative_analysis)

        results = []
        for patent in patents:
            evaluation = eval_map.get(
                _entity_key(patent.record_id, patent.patent_id),
                PatentEvaluation(record_id=patent.record_id, patent_id=patent.patent_id),
            )
            results.append({
                "patent": patent.to_dict(),
                "evaluation": evaluation.to_dict(),
            })

        results.sort(
            key=lambda x: x["evaluation"]["relevance_score"],
            reverse=True,
        )

        return {
            "metadata": {
                "query": query,
                "timestamp": datetime.now().isoformat(),
                "total_patents": len(patents),
                "model": run_metadata.get("model", config.OLLAMA_MODEL) if run_metadata else config.OLLAMA_MODEL,
                "average_relevance": (
                    sum(e.relevance_score for e in scored) / len(scored)
                    if scored
                    else 0
                ),
                "run_state": run_metadata or {},
                "feature_flags": run_metadata.get("feature_flags", {}) if run_metadata else {},
                "writing_context": writing_context,
                "stage_metrics": stage_metrics,
                "llm_cache_stats": llm_cache_stats,
                "llm_telemetry": llm_telemetry,
                "observability_metrics": observability_metrics,
                "whitespace_analysis": whitespace_analysis,
                "scraper_diagnostics": scraper_diagnostics,
                "prisma_flow": prisma_flow,
                "thematic_clusters": thematic_clusters,
                "config_snapshot": config_snapshot,
                "snapshot_hash": snapshot_hash,
                "draft_status": draft_status,
            },
            "results": results,
            "comparative_analysis": comparative_analysis,
            "whitespace_analysis": whitespace_analysis,
        }

    def _draft_status(
        self,
        patents: List[Patent],
        evaluations: List[PatentEvaluation],
        comparative_analysis: str,
    ) -> dict:
        """Garante que o relatório não seja considerado pronto sem substância."""
        substantive_evaluations = [
            evaluation for evaluation in evaluations
            if evaluation.screening_decision == "include"
            and not evaluation.llm_error
            and (
                evaluation.summary
                or evaluation.evidence_snippets
                or evaluation.problem_statement
                or evaluation.solution_summary
                or evaluation.key_findings
            )
        ]
        warnings = []
        comparative_ready = has_substantive_comparative_analysis(comparative_analysis)
        if not patents:
            warnings.append("Nenhuma patente encontrada.")
        if not substantive_evaluations and not comparative_ready:
            warnings.append("Conteúdo insuficiente para um rascunho completo.")

        status = "ready" if substantive_evaluations or comparative_ready else "blocked"
        return {
            "status": status,
            "warnings": warnings,
            "substantive_patents": len(substantive_evaluations),
        }
