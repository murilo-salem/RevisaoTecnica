"""
Motor de confronto: reivindicações do artigo vs. extração das patentes.
Identifica whitespace (gaps não cobertos por patentes existentes).
"""

import logging
import time
from typing import List, Optional

from logging_utils import log_event
from models.article import (
    ArticleAnalysis,
    ArticleWhitespaceReport,
    ClaimCoverage,
    PatentExtraction,
)

logger = logging.getLogger(__name__)

_NARRATIVE_PROMPT = """\
Você é especialista em propriedade intelectual e análise de patentes.
Com base nos dados abaixo, escreva uma narrativa clara e objetiva sobre o whitespace encontrado.

INOVAÇÃO DO ARTIGO:
Título: {article_title}
Inovação central: {core_innovation}
Hipótese de novidade: {novelty_hypothesis}

REIVINDICAÇÕES E COBERTURA POR PATENTES EXISTENTES:
{coverage_summary}

ESTATÍSTICAS:
- Total de reivindicações analisadas: {total_claims}
- Whitespace real (sem cobertura em patentes): {whitespace_count} reivindicações ({whitespace_pct:.0f}%)
- Cobertura parcial (potencial whitespace): {partial_count} reivindicações
- Totalmente cobertas por patentes: {covered_count} reivindicações

Escreva uma narrativa em português (3-5 parágrafos) que:
1. Descreva o que a inovação propõe de novo
2. Identifique o que já existe em patentes (reivindicações cobertas)
3. Destaque claramente os whitespaces reais (reivindicações sem cobertura)
4. Avalie o potencial de patenteamento com base nos gaps encontrados

Escreva diretamente a narrativa, sem JSON, sem bullet points, sem títulos de seção.
"""


def build_whitespace_report(
    article_analysis: ArticleAnalysis,
    extractions: List[PatentExtraction],
    evaluator=None,  # OllamaEvaluator opcional para gerar narrativa
) -> ArticleWhitespaceReport:
    """Confronta reivindicações do artigo com extrações das patentes e monta o relatório."""
    coverage_map: dict = {}
    for claim in article_analysis.claims:
        coverage_map[claim.id] = ClaimCoverage(
            claim_id=claim.id,
            claim_text=claim.text,
            status="whitespace",
            covering_patents=[],
            partial_patents=[],
        )

    for extraction in extractions:
        patent_id = extraction.patent_id or extraction.record_id

        for claim_id in extraction.covers_claims:
            if claim_id in coverage_map:
                cov = coverage_map[claim_id]
                if patent_id not in cov.covering_patents:
                    cov.covering_patents.append(patent_id)
                cov.status = "covered"

        for partial in extraction.partial_coverage:
            claim_id = partial.get("claim_id")
            aspect = partial.get("aspect", "")
            if claim_id in coverage_map:
                cov = coverage_map[claim_id]
                if cov.status != "covered":
                    cov.status = "partial"
                cov.partial_patents.append({"patent_id": patent_id, "aspect": aspect})

    coverage_list = list(coverage_map.values())
    whitespace_ids = [c.claim_id for c in coverage_list if c.status == "whitespace"]
    partial_ids = [c.claim_id for c in coverage_list if c.status == "partial"]
    covered_ids = [c.claim_id for c in coverage_list if c.status == "covered"]
    total = len(coverage_list) or 1
    whitespace_score = len(whitespace_ids) / total

    narrative = ""
    if evaluator is not None and coverage_list:
        coverage_lines = []
        for cov in coverage_list:
            badge = {"covered": "COBERTO", "partial": "PARCIAL", "whitespace": "WHITESPACE"}[cov.status]
            coverage_lines.append(f"[{badge}] Reivindicação {cov.claim_id}: {cov.claim_text[:120]}")
            if cov.covering_patents:
                coverage_lines.append(f"  → Coberto por: {', '.join(cov.covering_patents[:3])}")
            if cov.partial_patents:
                parts = [
                    f"{p['patent_id']} ({p['aspect'][:60]})"
                    for p in cov.partial_patents[:2]
                ]
                coverage_lines.append(f"  → Parcialmente por: {'; '.join(parts)}")

        prompt = _NARRATIVE_PROMPT.format(
            article_title=article_analysis.article_title,
            core_innovation=article_analysis.core_innovation,
            novelty_hypothesis=article_analysis.novelty_hypothesis,
            coverage_summary="\n".join(coverage_lines),
            total_claims=total,
            whitespace_count=len(whitespace_ids),
            whitespace_pct=whitespace_score * 100,
            partial_count=len(partial_ids),
            covered_count=len(covered_ids),
        )
        started = time.perf_counter()
        narrative = evaluator._call_ollama(
            prompt,
            response_format=None,
            num_predict=2048,
            operation="whitespace_narrative",
        )
        log_event(
            logger,
            logging.INFO,
            "whitespace_narrative_generated",
            duration=round(time.perf_counter() - started, 2),
            chars=len(narrative),
        )

    recommended_queries = []
    whitespace_claim_objects = [
        claim for claim in article_analysis.claims if claim.id in whitespace_ids
    ]
    for claim in whitespace_claim_objects[:3]:
        words = claim.text.split()[:8]
        recommended_queries.append(" ".join(words))

    log_event(
        logger,
        logging.INFO,
        "whitespace_report_built",
        total_claims=total,
        whitespace=len(whitespace_ids),
        partial=len(partial_ids),
        covered=len(covered_ids),
        whitespace_score=round(whitespace_score, 3),
    )
    return ArticleWhitespaceReport(
        status="ok",
        claim_coverage=coverage_list,
        whitespace_claims=whitespace_ids,
        partial_claims=partial_ids,
        covered_claims=covered_ids,
        whitespace_score=round(whitespace_score, 3),
        narrative=narrative,
        recommended_queries=recommended_queries,
    )
