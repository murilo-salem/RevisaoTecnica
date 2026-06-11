"""
Orquestrador do pipeline de análise de artigo → whitespace.

Fluxo:
  1. LLM forte analisa artigo → claims + queries de busca
  2. Scrapers buscam patentes por cada query gerada
  3. LLM médio extrai pontos técnicos de cada patente
  4. Motor de whitespace confronta reivindicações vs. patentes
"""

import logging
import time
from datetime import datetime
from typing import Callable, List, Optional

import config
from evaluator.article_analyzer import ArticleAnalyzer
from evaluator.llm_evaluator import OllamaEvaluator
from evaluator.patent_extractor import PatentExtractor
from logging_utils import log_event
from models.article_state import ArticleRunState
from models.patent import Patent
from pipeline.orchestrator import _dedupe_patents
from pipeline.whitespace_engine import build_whitespace_report
from scraper.epo import EPOScraper
from scraper.google_patents import GooglePatentsScraper
from scraper.patentscope import PatentscopeScraper

logger = logging.getLogger(__name__)


def _record_stage(
    state: ArticleRunState,
    stage: str,
    start: float,
    end: float,
    status: str,
    items: int = 0,
    detail: str = "",
) -> None:
    metric = {
        "stage": stage,
        "status": status,
        "duration_seconds": round(end - start, 3),
        "items_processed": items,
        "detail": detail,
    }
    state.stage_metrics.append(metric)
    log_event(logger, logging.INFO, "article_stage_metric", **metric)


def run_article_analysis(
    article_text: str,
    innovation_description: str,
    analysis_model: str = None,
    extraction_model: str = None,
    max_results_per_query: int = 5,
    max_queries: int = 4,
    state_sink: Callable | None = None,
    user_queries: Optional[List[str]] | None = None,
) -> ArticleRunState:
    """Executa o pipeline completo de análise de artigo."""
    analysis_model = analysis_model or config.OLLAMA_MODEL
    extraction_model = extraction_model or config.OLLAMA_EXTRACTION_MODEL
    run_start = time.perf_counter()
    max_queries = min(max_queries, config.ARTICLE_MAX_SEARCH_QUERIES)

    state = ArticleRunState(
        innovation_description=innovation_description,
        analysis_model=analysis_model,
        extraction_model=extraction_model,
        status="running",
    )
    if state_sink is not None:
        state_sink(state)

    # ── Estágio 1: Análise do artigo (LLM forte) ──
    state.current_stage = "article_analysis"
    log_event(logger, logging.INFO, "article_stage_start", stage="article_analysis", model=analysis_model)
    stage_start = time.perf_counter()
    try:
        analyzer = ArticleAnalyzer(model=analysis_model)
        if user_queries:
            analysis = analyzer.analyze_innovation(
                innovation_description=innovation_description,
                max_queries=max_queries,
            )
        else:
            analysis = analyzer.analyze(
                article_text=article_text,
                innovation_description=innovation_description,
                max_queries=max_queries,
            )
        if analysis is None:
            state.errors.append("Falha na análise do artigo: LLM retornou resposta vazia.")
            state.status = "error"
            state.finished_at = datetime.now().isoformat(timespec="seconds")
            state.total_duration_seconds = round(time.perf_counter() - run_start, 3)
            _record_stage(state, "article_analysis", stage_start, time.perf_counter(), "error",
                          detail="LLM returned empty")
            return state

        state.article_analysis = analysis
        state.article_title = analysis.article_title
        queries = user_queries if user_queries else analysis.search_queries[:max_queries]
        _record_stage(
            state, "article_analysis", stage_start, time.perf_counter(), "ok",
            items=len(analysis.claims),
            detail=f"{len(analysis.claims)} claims, {len(queries)} queries",
        )
    except Exception as exc:
        msg = f"Erro na análise do artigo: {exc}"
        state.errors.append(msg)
        state.status = "error"
        state.finished_at = datetime.now().isoformat(timespec="seconds")
        state.total_duration_seconds = round(time.perf_counter() - run_start, 3)
        _record_stage(state, "article_analysis", stage_start, time.perf_counter(), "error", detail=str(exc))
        logger.exception(msg)
        return state

    # ── Estágio 2: Busca de patentes ──
    state.current_stage = "search"
    log_event(logger, logging.INFO, "article_stage_start", stage="search", queries=queries)
    stage_start = time.perf_counter()

    scrapers = [GooglePatentsScraper(), PatentscopeScraper(), EPOScraper()]
    all_raw: List[Patent] = []

    for query in queries:
        state.patents_by_query[query] = []
        for scraper in scrapers:
            source_name = scraper.__class__.__name__.replace("Scraper", "")
            try:
                results = scraper.search(query, max_results=max_results_per_query)
                state.patents_by_source[source_name] = (
                    state.patents_by_source.get(source_name, 0) + len(results)
                )
                all_raw.extend(results)
                log_event(
                    logger, logging.INFO, "article_search_result",
                    source=source_name, query=query[:60], count=len(results),
                )
            except Exception as exc:
                msg = f"Erro no scraper {source_name} para '{query[:40]}': {exc}"
                state.errors.append(msg)
                logger.exception(msg)

    deduped, _ = _dedupe_patents(all_raw)
    state.patents = deduped

    for query in queries:
        state.patents_by_query[query] = [p.record_id for p in deduped][:max_results_per_query]

    _record_stage(
        state, "search", stage_start, time.perf_counter(),
        "ok" if deduped else "empty",
        items=len(deduped),
        detail=f"{len(all_raw)} raw → {len(deduped)} únicos",
    )

    if not deduped:
        # Sem patentes = whitespace total — não é erro, é resultado válido
        log_event(logger, logging.INFO, "article_search_no_results", queries=queries)
        state.current_stage = "whitespace"
        stage_start_ws = time.perf_counter()
        try:
            narrative_evaluator = OllamaEvaluator(model=analysis_model)
            report = build_whitespace_report(
                article_analysis=state.article_analysis,
                extractions=[],
                evaluator=narrative_evaluator,
            )
            state.whitespace_report = report
            _record_stage(
                state, "whitespace", stage_start_ws, time.perf_counter(), "ok",
                items=len(report.whitespace_claims),
                detail=f"score=1.00 — nenhuma patente encontrada (whitespace total)",
            )
        except Exception as exc:
            state.errors.append(f"Erro na análise de whitespace: {exc}")
            logger.exception(str(exc))
        state.status = "completed"
        state.current_stage = "done"
        state.finished_at = datetime.now().isoformat(timespec="seconds")
        state.total_duration_seconds = round(time.perf_counter() - run_start, 3)
        return state

    # ── Estágio 3: Extração (LLM médio) ──
    state.current_stage = "extraction"
    log_event(
        logger, logging.INFO, "article_stage_start", stage="extraction",
        model=extraction_model, patents=len(deduped),
    )
    stage_start = time.perf_counter()
    extractor = PatentExtractor(model=extraction_model)
    claims = state.article_analysis.claims

    for patent in deduped:
        try:
            extraction = extractor.extract(patent=patent, claims=claims)
            state.patent_extractions.append(extraction)
        except Exception as exc:
            msg = f"Erro na extração da patente {patent.patent_id or patent.record_id}: {exc}"
            state.errors.append(msg)
            logger.exception(msg)
        state.extracted_count += 1

    _record_stage(
        state, "extraction", stage_start, time.perf_counter(), "ok",
        items=state.extracted_count,
        detail=f"{state.extracted_count} patentes processadas",
    )

    # ── Estágio 4: Whitespace (confronto + narrativa LLM forte) ──
    state.current_stage = "whitespace"
    log_event(logger, logging.INFO, "article_stage_start", stage="whitespace")
    stage_start = time.perf_counter()

    narrative_evaluator = OllamaEvaluator(model=analysis_model)
    try:
        report = build_whitespace_report(
            article_analysis=state.article_analysis,
            extractions=state.patent_extractions,
            evaluator=narrative_evaluator,
        )
        state.whitespace_report = report
        _record_stage(
            state, "whitespace", stage_start, time.perf_counter(), "ok",
            items=len(report.whitespace_claims),
            detail=f"score={report.whitespace_score:.2f}, {len(report.whitespace_claims)} gaps",
        )
    except Exception as exc:
        msg = f"Erro na análise de whitespace: {exc}"
        state.errors.append(msg)
        logger.exception(msg)
        _record_stage(state, "whitespace", stage_start, time.perf_counter(), "error", detail=str(exc))

    state.status = "completed"
    state.current_stage = "done"
    state.finished_at = datetime.now().isoformat(timespec="seconds")
    state.total_duration_seconds = round(time.perf_counter() - run_start, 3)
    log_event(
        logger,
        logging.INFO,
        "article_run_completed",
        run_id=state.run_id,
        duration=state.total_duration_seconds,
        patents=len(deduped),
        whitespace_score=(
            state.whitespace_report.whitespace_score if state.whitespace_report else None
        ),
    )
    return state
