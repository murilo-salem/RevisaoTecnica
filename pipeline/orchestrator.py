"""
Orquestrador do fluxo de busca, avaliação e relatório.
"""

import json
import hashlib
import logging
import os
import re
import time
from datetime import datetime
from typing import Callable, Dict, List, Tuple

from analysis_utils import (
    COMPARATIVE_ANALYSIS_NO_INPUT,
    has_substantive_comparative_analysis,
)
import config
from evaluator.llm_evaluator import OllamaEvaluator
from logging_utils import log_event
from models.patent import Patent, PatentEvaluation
from pipeline.features import PipelineFeatures
from pipeline.memory import MemorySidecar
from pipeline.router import ThemeRouter
from pipeline.state import RunState
from pipeline.protocol import build_review_protocol
from report.generator import ReportGenerator
from scraper.base import BaseScraper
from scraper.google_patents import GooglePatentsScraper
from scraper.patentscope import PatentscopeScraper

logger = logging.getLogger(__name__)


class RunStateStore:
    """Persiste o estado incremental da execução em disco."""

    def __init__(self, output_dir: str, run_id: str):
        self.output_dir = output_dir
        self.state_path = os.path.join(output_dir, f"run_state_{run_id}.json")
        self.latest_path = os.path.join(output_dir, "run_state_latest.json")
        os.makedirs(self.output_dir, exist_ok=True)

    def save(self, state: RunState) -> None:
        """Escreve a versão atual do estado em arquivos JSON."""
        payload = state.to_dict()

        for path in (self.state_path, self.latest_path):
            with open(path, "w", encoding="utf-8") as f:
                json.dump(payload, f, ensure_ascii=False, indent=2)

    def save_artifact(self, filename: str, payload: dict) -> str:
        """Salva um artefato JSON auxiliar."""
        path = os.path.join(self.output_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        return path


def print_banner() -> None:
    """Emite evento de inicialização do agente."""
    log_event(
        logger,
        logging.INFO,
        "agent_startup",
        component="patent-agent",
        description="Agente de Web Scraping de Patentes",
    )


def print_progress(step: str, current: int = 0, total: int = 0) -> None:
    """Emite progresso como log estruturado."""
    if total > 0:
        percent = round((current / total) * 100, 1) if total else 0.0
        log_event(
            logger,
            logging.INFO if current == total else logging.DEBUG,
            "progress",
            step=step,
            current=current,
            total=total,
            percent=percent,
        )
    else:
        log_event(
            logger,
            logging.INFO,
            "progress",
            step=step,
        )


def _log_stage(stage: str, title: str, level: int = logging.INFO, **fields: object) -> None:
    """Emite transições de etapa do pipeline."""
    log_event(
        logger,
        level,
        "stage_transition",
        stage=stage,
        title=title,
        **fields,
    )


def _normalize_text(value: str) -> str:
    """Normaliza texto para deduplicação."""
    return re.sub(r"\s+", " ", (value or "").strip()).lower()


def _normalize_patent_id(value: str) -> str:
    """Normaliza identificadores de patente e números de publicação."""
    return re.sub(r"[^A-Z0-9]", "", (value or "").upper())


def _record_id_from_key(key: str) -> str:
    """Gera identificador interno estável para a execução."""
    digest = hashlib.sha1((key or "record").encode("utf-8")).hexdigest()[:12]
    return f"rec_{digest}"


def _display_patent_id(patent: Patent) -> str:
    """Retorna o melhor identificador legível para humanos."""
    return patent.patent_id or patent.record_id or "N/A"


def _identity_key(patent: Patent) -> Tuple[str, str]:
    """Gera uma chave estável de identidade e informa sua base."""
    pid = _normalize_patent_id(patent.patent_id)
    if pid:
        return f"id:{pid}", "patent_id"

    if patent.url:
        url = patent.url.split("#", 1)[0].split("?", 1)[0].strip().lower()
        if url:
            return f"url:{url}", "url"

    title = _normalize_text(patent.title)
    if title:
        return f"title:{title}", "title"

    content_seed = {
        "abstract": _normalize_text(patent.abstract),
        "snippet": _normalize_text(patent.snippet),
        "assignee": _normalize_text(patent.assignee),
        "publication_date": _normalize_text(patent.publication_date),
        "filing_date": _normalize_text(patent.filing_date),
    }
    if any(content_seed.values()):
        encoded = json.dumps(content_seed, sort_keys=True, ensure_ascii=False).encode("utf-8")
        return f"content:{hashlib.sha1(encoded).hexdigest()}", "content"

    fallback_seed = {
        "source": _normalize_text(patent.source),
        "inventors": [_normalize_text(item) for item in patent.inventors],
        "url": patent.url.strip().lower(),
    }
    encoded = json.dumps(fallback_seed, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return f"fallback:{hashlib.sha1(encoded).hexdigest()}", "fallback"


def _family_key(patent: Patent) -> str:
    """Gera uma assinatura conservadora de família para dedupe inter-publicação."""
    title = _normalize_text(patent.title)
    assignee = _normalize_text(patent.assignee)
    inventor = _normalize_text(patent.inventors[0]) if patent.inventors else ""
    year_match = re.search(r"(19|20)\d{2}", patent.filing_date or patent.publication_date or "")
    year = year_match.group(0) if year_match else ""

    if title and ((assignee and year) or (inventor and year) or (assignee and inventor)):
        payload = {
            "title": title,
            "assignee": assignee,
            "inventor": inventor,
            "year": year,
        }
        encoded = json.dumps(payload, sort_keys=True, ensure_ascii=False).encode("utf-8")
        return f"family:{hashlib.sha1(encoded).hexdigest()}"
    return ""


def _entity_key(record_id: str, patent_id: str) -> str:
    """Resolve a chave interna preferencial de patente/avaliação."""
    return record_id or _normalize_patent_id(patent_id) or patent_id or ""


def _evaluation_map(evaluations: List[PatentEvaluation]) -> Dict[str, PatentEvaluation]:
    """Indexa avaliações pela chave interna estável."""
    return {
        _entity_key(evaluation.record_id, evaluation.patent_id): evaluation
        for evaluation in evaluations
        if _entity_key(evaluation.record_id, evaluation.patent_id)
    }


def _pair_patents_with_evaluations(
    patents: List[Patent],
    evaluations: List[PatentEvaluation],
) -> List[Tuple[Patent, PatentEvaluation]]:
    """Relaciona patentes e avaliações por record_id, não pela ordem da lista."""
    eval_map = _evaluation_map(evaluations)
    pairs: List[Tuple[Patent, PatentEvaluation]] = []
    for patent in patents:
        key = _entity_key(patent.record_id, patent.patent_id)
        evaluation = eval_map.get(key)
        if evaluation is not None:
            pairs.append((patent, evaluation))
    return pairs


def _build_config_snapshot(
    query: str,
    max_results: int,
    model: str,
    output_dir: str,
    features: PipelineFeatures,
) -> Dict[str, object]:
    """Monta um snapshot estável da configuração da execução."""
    return {
        "pipeline_version": "1.1",
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "query": query,
        "max_results": max_results,
        "model": model,
        "output_dir": output_dir,
        "feature_flags": features.to_dict(),
        "thresholds": {
            "include": config.SCREEN_INCLUDE_THRESHOLD,
            "review": config.SCREEN_REVIEW_THRESHOLD,
            "manual_review_limit": config.SCREEN_MAX_ITEMS_FOR_REVIEW,
        },
        "runtime": {
            "ollama_base_url": config.OLLAMA_BASE_URL,
            "ollama_timeout": config.OLLAMA_TIMEOUT,
        },
        "sources": [
            "Google Patents",
            "Patentscope",
        ],
    }


def _hash_snapshot(snapshot: Dict[str, object]) -> str:
    """Calcula hash estável do snapshot."""
    encoded = json.dumps(snapshot, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _merge_patents(base: Patent, incoming: Patent) -> Patent:
    """Combina campos não vazios de duas versões da mesma patente."""
    if not base.record_id and incoming.record_id:
        base.record_id = incoming.record_id
    if not base.family_id and incoming.family_id:
        base.family_id = incoming.family_id
    if not base.title and incoming.title:
        base.title = incoming.title
    if not base.abstract and incoming.abstract:
        base.abstract = incoming.abstract
    if not base.assignee and incoming.assignee:
        base.assignee = incoming.assignee
    if not base.filing_date and incoming.filing_date:
        base.filing_date = incoming.filing_date
    if not base.publication_date and incoming.publication_date:
        base.publication_date = incoming.publication_date
    if not base.url and incoming.url:
        base.url = incoming.url
    if not base.snippet and incoming.snippet:
        base.snippet = incoming.snippet
    if incoming.source:
        if not base.source:
            base.source = incoming.source
        elif incoming.source not in base.source:
            base.source = f"{base.source}; {incoming.source}"

    for inventor in incoming.inventors:
        if inventor not in base.inventors:
            base.inventors.append(inventor)

    return base


def _dedupe_patents(patents: List[Patent]) -> Tuple[List[Patent], Dict[str, int]]:
    """Remove duplicatas mantendo a melhor versão de cada patente."""
    deduped: Dict[str, Patent] = {}
    stats = {
        "records_with_content_identity": 0,
        "records_with_fallback_identity": 0,
        "family_duplicates_removed": 0,
    }

    for patent in patents:
        key, basis = _identity_key(patent)
        patent.record_id = _record_id_from_key(key)

        if key in deduped:
            deduped[key] = _merge_patents(deduped[key], patent)
        else:
            deduped[key] = patent
            if basis == "content":
                stats["records_with_content_identity"] += 1
            elif basis == "fallback":
                stats["records_with_fallback_identity"] += 1

    family_deduped: Dict[str, Patent] = {}
    for patent in deduped.values():
        family_key = _family_key(patent)
        if family_key:
            patent.family_id = family_key
            patent.record_id = _record_id_from_key(family_key)
        else:
            patent.family_id = ""

        merge_key = family_key or f"record:{patent.record_id}"
        if merge_key in family_deduped:
            family_deduped[merge_key] = _merge_patents(family_deduped[merge_key], patent)
            if family_key:
                stats["family_duplicates_removed"] += 1
        else:
            family_deduped[merge_key] = patent

    return list(family_deduped.values()), stats


def _build_manual_review_queue(
    patents: List[Patent],
    evaluations: List[PatentEvaluation],
    limit: int,
) -> Tuple[List[Dict[str, object]], int]:
    """Constrói um contrato explícito para a fila de revisão manual."""
    queue_candidates: List[Dict[str, object]] = []
    for patent, evaluation in _pair_patents_with_evaluations(patents, evaluations):
        if not (evaluation.manual_review_required or evaluation.screening_decision == "review" or evaluation.llm_error):
            continue
        queue_candidates.append({
            "record_id": patent.record_id,
            "patent_id": patent.patent_id,
            "family_id": patent.family_id,
            "title": patent.title,
            "reason": evaluation.route_reason or evaluation.screening_reason,
            "route": evaluation.analysis_route,
            "screening_score": evaluation.screening_score,
            "screening_decision": evaluation.screening_decision,
            "llm_error": evaluation.llm_error,
        })

    queue_candidates.sort(
        key=lambda item: (
            0 if item.get("llm_error") else 1,
            -(item.get("screening_score") or 0),
            item.get("title") or "",
        )
    )
    limited = queue_candidates[:limit]
    deferred = max(len(queue_candidates) - len(limited), 0)
    return limited, deferred


def _cluster_label(patent: Patent, evaluation: PatentEvaluation) -> str:
    """Atribui um cluster temático determinístico."""
    text = " ".join([
        patent.title,
        patent.abstract,
        patent.snippet,
        evaluation.summary,
        evaluation.technical_domain,
    ]).lower()

    rules = [
        ("CO2 Cycle Configurations", ["cycle", "transcritical", "ejector", "economizer", "compressor", "cop"]),
        ("CO2 Phase Properties", ["phase", "triple point", "critical point", "property"]),
        ("Cryogenic Energy Systems", ["cryogenic", "liquid air", "laes", "cold storage", "boil-off"]),
        ("Phase Change Materials", ["pcm", "phase change", "latent heat", "encapsulat"]),
        ("Thermal Transfer Mechanisms", ["boiling", "condensation", "heat transfer", "nucleate"]),
        ("Economic Optimization", ["economic", "cost", "tariff", "optimization", "arbitrage"]),
        ("Solid CO2 Storage", ["solid co2", "dry ice", "sublim"]),
    ]

    for label, keywords in rules:
        if any(keyword in text for keyword in keywords):
            return label

    if evaluation.technical_domain:
        return evaluation.technical_domain
    return "General / Other"


def _prisma_stage_artifact(state: RunState, counts: Dict[str, int]) -> Dict[str, object]:
    """Monta um artefato PRISMA-like para o relatório e o estado."""
    return {
        "flow": {
            "identification": {
                "raw_records": counts.get("raw_scraped", 0),
                "unique_records": counts.get("unique_patents", 0),
                "duplicates_removed": counts.get("duplicates_removed", 0),
            },
            "screening": {
                "screened": counts.get("screened", 0),
                "included": counts.get("included", 0),
                "review": counts.get("review", 0),
                "excluded": counts.get("excluded", 0),
            },
            "eligibility": {
                "full_extractions": counts.get("full_extractions", 0),
                "manual_review_required": counts.get("manual_review_required", 0),
                "manual_review_deferred": counts.get("manual_review_deferred", 0),
            },
            "coverage": {
                "missing_abstract": counts.get("missing_abstract", 0),
                "missing_id": counts.get("missing_id", 0),
            },
            "synthesis": {
                "analyzed_records": counts.get("full_extractions", 0),
                "comparative_analysis_generated": has_substantive_comparative_analysis(
                    state.comparative_analysis
                ),
            },
        },
        "criteria": state.protocol.get("criteria", {}),
        "thresholds": state.protocol.get("thresholds", {}),
        "version": state.protocol.get("version", ""),
    }


def _build_top_patents(patents: List[Patent], evaluations: List[PatentEvaluation], limit: int = 5) -> List[Dict[str, object]]:
    """Seleciona as patentes mais relevantes para o contexto compartilhado."""
    paired = [
        (patent, evaluation)
        for patent, evaluation in _pair_patents_with_evaluations(patents, evaluations)
        if evaluation.screening_decision == "include" and not evaluation.llm_error
    ]
    paired.sort(key=lambda item: item[1].relevance_score, reverse=True)
    top = []
    for patent, evaluation in paired[:limit]:
        top.append({
            "record_id": patent.record_id,
            "family_id": patent.family_id,
            "patent_id": patent.patent_id,
            "title": patent.title,
            "score": evaluation.relevance_score,
            "screening_decision": evaluation.screening_decision,
            "thematic_cluster": evaluation.thematic_cluster,
            "route": evaluation.analysis_route,
            "evidence_snippets": evaluation.evidence_snippets[:2],
        })
    return top


def _build_route_summary(evaluations: List[PatentEvaluation]) -> Dict[str, int]:
    """Agrega estatísticas de roteamento por tipo de análise."""
    summary: Dict[str, int] = {}
    for evaluation in evaluations:
        route = evaluation.analysis_route or "unrouted"
        summary[route] = summary.get(route, 0) + 1
    return summary


def _count_diagnostic_kinds(items: List[Dict[str, object]]) -> Dict[str, int]:
    """Conta diagnósticos por tipo."""
    counts: Dict[str, int] = {}
    for item in items:
        kind = item.get("kind", "unknown") or "unknown"
        counts[kind] = counts.get(kind, 0) + 1
    return counts


def _build_observability_metrics(state: RunState) -> Dict[str, object]:
    """Expande métricas de observabilidade por rota, fonte e falha."""
    route_metrics: Dict[str, Dict[str, object]] = {}
    for evaluation in state.evaluations:
        route = evaluation.analysis_route or "unrouted"
        bucket = route_metrics.setdefault(route, {
            "count": 0,
            "include": 0,
            "review": 0,
            "exclude": 0,
            "llm_errors": 0,
        })
        bucket["count"] += 1
        decision = (evaluation.screening_decision or "unknown").lower()
        if decision in {"include", "review", "exclude"}:
            bucket[decision] += 1
        if evaluation.llm_error:
            bucket["llm_errors"] += 1

    source_metrics: Dict[str, Dict[str, object]] = {}
    for source_name, raw_results in state.patents_by_source.items():
        diagnostics = state.scraper_diagnostics.get(source_name, [])
        source_metrics[source_name] = {
            "raw_results": raw_results,
            "duration_seconds": round(float(state.scraper_durations.get(source_name, 0) or 0), 3),
            "diagnostic_counts": _count_diagnostic_kinds(diagnostics),
        }

    llm_by_operation: Dict[str, Dict[str, int]] = {}
    for operation, metric in state.llm_telemetry.get("operations", {}).items():
        llm_by_operation[operation] = {
            "calls": int(metric.get("calls", 0) or 0),
            "failures": int(metric.get("failures", 0) or 0),
            "retries": int(metric.get("retries", 0) or 0),
            "degraded_skips": int(metric.get("degraded_skips", 0) or 0),
        }

    scraper_failure_counts: Dict[str, int] = {}
    for items in state.scraper_diagnostics.values():
        for kind, count in _count_diagnostic_kinds(items).items():
            scraper_failure_counts[kind] = scraper_failure_counts.get(kind, 0) + count

    failure_metrics = {
        "run_errors": len(state.errors),
        "records_with_llm_error": sum(1 for evaluation in state.evaluations if evaluation.llm_error),
        "llm_total_failures": int(state.llm_telemetry.get("total_failures", 0) or 0),
        "llm_by_operation": llm_by_operation,
        "scraper_diagnostics_by_kind": scraper_failure_counts,
    }

    return {
        "routes": dict(sorted(route_metrics.items(), key=lambda item: (-item[1]["count"], item[0]))),
        "sources": dict(sorted(source_metrics.items())),
        "failures": failure_metrics,
    }


def _build_writing_context(state: RunState) -> Dict[str, object]:
    """Compacta o estado para consumo do writer/relatório."""
    return {
        "protocol": state.protocol,
        "coverage_metrics": state.coverage_metrics,
        "top_patents": _build_top_patents(state.patents, state.evaluations),
        "thematic_clusters": state.thematic_clusters,
        "route_summary": _build_route_summary(state.evaluations),
        "feature_flags": state.feature_flags,
        "snapshot_hash": state.snapshot_hash,
    }


def _record_stage_metric(
    state: RunState,
    stage: str,
    start_time: float,
    end_time: float,
    status: str,
    items_processed: int = 0,
    detail: str = "",
) -> None:
    """Registra métricas estruturadas de etapa e loga a transição."""
    metric = {
        "stage": stage,
        "status": status,
        "duration_seconds": round(end_time - start_time, 3),
        "items_processed": items_processed,
        "detail": detail,
    }
    state.stage_metrics.append(metric)
    log_event(
        logger,
        logging.INFO,
        "stage_metric",
        stage=stage,
        status=status,
        duration_seconds=metric["duration_seconds"],
        items_processed=items_processed,
        detail=detail,
    )


def _build_thematic_clusters(
    patents: List[Patent],
    evaluations: List[PatentEvaluation],
) -> Dict[str, object]:
    """Agrupa patentes em clusters temáticos para síntese."""
    clusters: Dict[str, Dict[str, object]] = {}

    for patent, evaluation in _pair_patents_with_evaluations(patents, evaluations):
        if evaluation.screening_decision != "include" or evaluation.llm_error:
            continue

        label = _cluster_label(patent, evaluation)
        evaluation.thematic_cluster = label

        cluster = clusters.setdefault(label, {
            "cluster": label,
            "count": 0,
            "patent_ids": [],
            "titles": [],
            "average_score": 0.0,
            "average_confidence": 0.0,
            "evidence_count": 0,
            "top_patents": [],
            "summary": "",
        })
        cluster["count"] += 1
        cluster.setdefault("record_ids", []).append(patent.record_id)
        cluster["patent_ids"].append(patent.patent_id)
        cluster["titles"].append(patent.title)
        cluster["average_score"] += evaluation.relevance_score
        cluster["average_confidence"] += evaluation.confidence
        cluster["evidence_count"] += len(evaluation.evidence_snippets)

    for cluster in clusters.values():
        count = cluster["count"] or 1
        cluster["average_score"] = round(cluster["average_score"] / count, 2)
        cluster["average_confidence"] = round(cluster["average_confidence"] / count, 2)

    return {
        "clusters": sorted(
            clusters.values(),
            key=lambda item: (item["count"], item["average_score"]),
            reverse=True,
        ),
        "total_clusters": len(clusters),
    }


def run_agent(
    query: str,
    max_results: int,
    model: str,
    output_dir: str,
    features: PipelineFeatures | None = None,
    scrapers: List[BaseScraper] | None = None,
    evaluator_factory: Callable[..., OllamaEvaluator] | None = None,
) -> RunState:
    """Executa o fluxo completo do agente com estado persistido."""
    start_time = time.perf_counter()
    pipeline_features = features or PipelineFeatures()
    config_snapshot = (
        _build_config_snapshot(query, max_results, model, output_dir, pipeline_features)
        if pipeline_features.enable_snapshot
        else {}
    )
    state = RunState(
        query=query,
        max_results=max_results,
        model=model,
        output_dir=output_dir,
        feature_flags=pipeline_features.to_dict(),
        config_snapshot=config_snapshot,
        snapshot_hash=_hash_snapshot(config_snapshot) if config_snapshot else "",
        protocol=build_review_protocol(query, max_results, model),
    )
    store = RunStateStore(output_dir=output_dir, run_id=state.run_id)
    memory = MemorySidecar(run_id=state.run_id)
    router = ThemeRouter()

    _log_stage("setup", "Verificando conexão com Ollama", model=state.model)

    setup_start = time.perf_counter()
    if evaluator_factory is None:
        evaluator = OllamaEvaluator(model=state.model, cache_dir=output_dir)
    else:
        evaluator = evaluator_factory(model=state.model, output_dir=output_dir)
    state.llm_available = evaluator.check_connection()
    memory.append(
        "setup",
        "llm_check",
        "Verificação de disponibilidade do Ollama concluída.",
        {"llm_available": state.llm_available, "model": state.model},
    )
    _record_stage_metric(
        state,
        "setup",
        setup_start,
        time.perf_counter(),
        "ok" if state.llm_available else "degraded",
        items_processed=1,
        detail="Verificação do modelo Ollama",
    )
    if not state.llm_available:
        log_event(
            logger,
            logging.WARNING,
            "llm_unavailable",
            model=state.model,
            recommended_command=f"ollama pull {state.model}",
            fallback_mode="manual_review_only",
        )
    else:
        log_event(
            logger,
            logging.INFO,
            "llm_available",
            model=state.model,
        )

    _log_stage(
        "search",
        "Buscando patentes",
        query=query,
        max_results=max_results,
    )

    search_start = time.perf_counter()
    scrapers = scrapers or [
        GooglePatentsScraper(),
        PatentscopeScraper(),
    ]

    patents: List[Patent] = []
    dedupe_stats = {
        "records_with_content_identity": 0,
        "records_with_fallback_identity": 0,
        "family_duplicates_removed": 0,
    }
    raw_total = 0
    for scraper in scrapers:
        source_name = scraper.__class__.__name__.replace("Scraper", "")
        print_progress(f"Iniciando scraping no {source_name}")
        scraper_start = time.perf_counter()
        try:
            results = scraper.search(query, max_results=max_results)
            raw_total += len(results)
            state.patents_by_source[source_name] = len(results)
            patents.extend(results)
            state.patents, dedupe_stats = _dedupe_patents(patents)
            state.scraper_diagnostics[source_name] = scraper.get_diagnostics()
            memory.append(
                "identification",
                "scrape_completed",
                f"{source_name} retornou patentes.",
                {
                    "source": source_name,
                    "count": len(results),
                    "diagnostics": scraper.get_diagnostics(),
                },
            )
            log_event(
                logger,
                logging.INFO,
                "scrape_completed",
                source=source_name,
                raw_results=len(results),
                unique_patents=len(state.patents),
                diagnostics_count=len(scraper.get_diagnostics()),
            )
        except Exception as e:
            message = f"Erro no scraper {source_name}: {e}"
            logger.exception(message)
            state.errors.append(message)
        finally:
            if source_name not in state.scraper_diagnostics:
                state.scraper_diagnostics[source_name] = scraper.get_diagnostics()
            state.scraper_durations[source_name] = round(
                time.perf_counter() - scraper_start,
                3,
            )
            store.save(state)

    _record_stage_metric(
        state,
        "search",
        search_start,
        time.perf_counter(),
        "ok" if state.patents else "empty",
        items_processed=raw_total,
        detail=f"{len(state.patents)} patentes únicas após dedupe",
    )

    if not state.patents:
        log_event(
            logger,
            logging.WARNING,
            "no_results",
            query=query,
            max_results=max_results,
            recommendation="Tente termos diferentes ou mais genéricos.",
        )
        state.status = "no_results"
        state.finished_at = datetime.now().isoformat(timespec="seconds")
        state.coverage_metrics = {
            "raw_scraped": raw_total,
            "unique_patents": 0,
            "duplicates_removed": raw_total,
            "screened": 0,
            "included": 0,
            "review": 0,
            "excluded": 0,
            "manual_review_required": 0,
            "manual_review_deferred": 0,
            "full_extractions": 0,
            "missing_abstract": 0,
            "missing_id": 0,
            "records_with_content_identity": dedupe_stats.get("records_with_content_identity", 0),
            "records_with_fallback_identity": dedupe_stats.get("records_with_fallback_identity", 0),
            "family_duplicates_removed": dedupe_stats.get("family_duplicates_removed", 0),
            "llm_screening_failures": 0,
            "llm_total_failures": 0,
        }
        state.total_duration_seconds = round(time.perf_counter() - start_time, 3)
        state.prisma_flow = (
            _prisma_stage_artifact(state, state.coverage_metrics)
            if pipeline_features.enable_prisma
            else {}
        )
        memory.append(
            "synthesis",
            "no_results",
            "Execução encerrada sem patentes encontradas.",
            state.coverage_metrics,
        )
        state.memory_sidecar = memory.to_dict()
        state.memory_journal = [entry.to_dict() for entry in memory.journal]
        state.llm_cache_stats = evaluator.cache_stats()
        state.llm_telemetry = evaluator.telemetry_stats()
        state.rerank_duration_seconds = round(
            state.llm_telemetry.get("operations", {}).get("rerank", {}).get("total_duration_seconds", 0.0),
            3,
        )
        state.observability_metrics = _build_observability_metrics(state)
        journal_path = store.save_artifact(f"memory_journal_{state.run_id}.json", state.memory_journal)
        sidecar_path = store.save_artifact(f"memory_sidecar_{state.run_id}.json", state.memory_sidecar)
        state.output_paths = {
            "state": os.path.abspath(store.state_path),
            "memory_journal": os.path.abspath(journal_path),
            "memory_sidecar": os.path.abspath(sidecar_path),
        }
        _record_stage_metric(
            state,
            "finalization",
            start_time,
            time.perf_counter(),
            "empty",
            items_processed=0,
            detail="Execução encerrada sem resultados",
        )
        log_event(
            logger,
            logging.INFO,
            "run_completed",
            status=state.status,
            total_duration_seconds=round(state.total_duration_seconds, 1),
            output_paths=state.output_paths,
        )
        store.save(state)
        return state

    missing_abstract = sum(1 for patent in state.patents if not (patent.abstract or patent.snippet))
    missing_id = sum(1 for patent in state.patents if not patent.patent_id)
    duplicates_removed = max(raw_total - len(state.patents), 0)

    log_event(
        logger,
        logging.INFO,
        "search_results_ready",
        patents_found=len(state.patents),
        duplicates_removed=duplicates_removed,
        missing_abstract=missing_abstract,
        missing_id=missing_id,
    )

    for i, patent in enumerate(state.patents, 1):
        log_event(
            logger,
            logging.INFO,
            "patent_discovered",
            index=i,
            patent_id=_display_patent_id(patent),
            title=patent.title[:80],
            assignee=patent.assignee or "",
            source=patent.source or "",
        )

    screenings: List[PatentEvaluation] = []
    llm_screening_failures = 0
    llm_circuit_open_logged = False
    screening_start = time.perf_counter()
    if state.llm_available:
        _log_stage(
            "screening",
            "Triagem e extração estruturada",
            model=state.model,
            include_threshold=config.SCREEN_INCLUDE_THRESHOLD,
            review_threshold=config.SCREEN_REVIEW_THRESHOLD,
        )

        for i, patent in enumerate(state.patents, 1):
            print_progress(
                f"Triando: {_display_patent_id(patent)} — {patent.title[:40]}...",
                i,
                len(state.patents),
            )
            if evaluator.is_degraded():
                screening = evaluator._llm_failure_evaluation(
                    patent,
                    "Circuit breaker global do LLM ativo; revisão manual necessária.",
                )
            else:
                screening = evaluator.screen_patent(
                    patent,
                    query,
                    require_evidence=pipeline_features.require_evidence,
                    enable_thematic_clusters=pipeline_features.enable_thematic_clusters,
                    enable_structural_roles=pipeline_features.enable_structural_roles,
                    enable_screening_rerank=pipeline_features.enable_screening_rerank,
                )
                if screening.llm_error:
                    llm_screening_failures += 1
            if evaluator.is_degraded() and not llm_circuit_open_logged:
                message = (
                    "Circuit breaker global do Ollama acionado após "
                    f"{evaluator.total_failures} falha(s) na execução."
                )
                state.errors.append(message)
                memory.append(
                    "policy",
                    "llm_circuit_open",
                    message,
                    {"failures": evaluator.total_failures},
                )
                llm_circuit_open_logged = True
            route = router.route(patent, screening)
            screening.analysis_route = route.route
            screening.route_reason = route.reason
            screenings.append(screening)
            memory.append(
                "screening",
                "screening_completed",
                f"{_display_patent_id(patent)} roteada para {route.route}.",
                {
                    "record_id": patent.record_id,
                    "patent_id": patent.patent_id,
                    "decision": screening.screening_decision,
                    "score": screening.screening_score,
                    "route": route.to_dict(),
                    "llm_error": screening.llm_error,
                },
            )
            memory.set_slot(
                route.slot,
                {
                    "record_id": patent.record_id,
                    "patent_id": patent.patent_id,
                    "title": patent.title,
                    "route": route.route,
                    "score": screening.screening_score,
                },
            )

            log_event(
                logger,
                logging.INFO,
                "screening_result",
                index=i,
                patent_id=_display_patent_id(patent),
                decision=screening.screening_decision,
                screening_score=screening.screening_score,
                technical_domain=screening.technical_domain or "N/A",
                route=screening.analysis_route,
                llm_error=screening.llm_error or "",
            )

        included = [
            item for item in screenings
            if item.screening_decision == "include"
        ]
        review = [
            item for item in screenings
            if item.screening_decision == "review"
        ]
        excluded = [
            item for item in screenings
            if item.screening_decision == "exclude"
        ]

        review.sort(key=lambda item: item.screening_score, reverse=True)
        review_limit = config.SCREEN_MAX_ITEMS_FOR_REVIEW
        review_to_process = (
            review[:review_limit]
            if pipeline_features.enable_manual_review_queue
            else []
        )
        if not pipeline_features.enable_manual_review_queue:
            memory.append(
                "policy",
                "manual_review_disabled",
                "Fila de revisão manual desativada por feature flag.",
            )

        screening_map = _evaluation_map(screenings)
        review_ids = {item.record_id for item in review_to_process}
        included_ids = {item.record_id for item in included}

        eval_start = time.perf_counter()
        evaluations: List[PatentEvaluation] = []
        for patent in state.patents:
            screening = screening_map.get(_entity_key(patent.record_id, patent.patent_id))
            if screening is None:
                continue

            if screening.record_id in included_ids or screening.record_id in review_ids:
                if evaluator.is_degraded():
                    detailed = screening
                    detailed.screening_decision = "review"
                    detailed.manual_review_required = True
                    detailed.llm_error = (
                        detailed.llm_error
                        or "Circuit breaker global do LLM ativo antes da extração detalhada."
                    )
                else:
                    detailed = evaluator.evaluate_patent(
                        patent,
                        query,
                        screening=screening,
                        require_evidence=pipeline_features.require_evidence,
                        enable_thematic_clusters=pipeline_features.enable_thematic_clusters,
                        enable_structural_roles=pipeline_features.enable_structural_roles,
                        enable_screening_rerank=pipeline_features.enable_screening_rerank,
                    )
                detailed.manual_review_required = screening.screening_decision == "review"
                if detailed.llm_error:
                    detailed.screening_decision = "review"
                    detailed.manual_review_required = True
                detailed.analysis_route = screening.analysis_route
                detailed.route_reason = screening.route_reason
                evaluations.append(detailed)
                memory.append(
                    "extraction",
                    "detailed_evaluation_completed",
                    f"{_display_patent_id(patent)} recebeu extração detalhada.",
                    {
                        "record_id": patent.record_id,
                        "patent_id": patent.patent_id,
                        "route": detailed.analysis_route,
                        "confidence": detailed.confidence,
                    },
                )
            else:
                evaluations.append(screening)
                memory.append(
                    "extraction",
                    "screening_only",
                    f"{_display_patent_id(patent)} permaneceu apenas na triagem.",
                    {
                        "record_id": patent.record_id,
                        "patent_id": patent.patent_id,
                        "route": screening.analysis_route,
                    },
                )

        state.evaluation_duration_seconds = round(time.perf_counter() - eval_start, 3)
        state.evaluations = evaluations
        state.manual_review_queue, review_deferred_count = _build_manual_review_queue(
            state.patents,
            state.evaluations,
            review_limit if pipeline_features.enable_manual_review_queue else 0,
        )
        state.thematic_clusters = (
            _build_thematic_clusters(state.patents, state.evaluations)
            if pipeline_features.enable_thematic_clusters
            else {"clusters": [], "total_clusters": 0}
        )
        state.coverage_metrics = {
            "raw_scraped": raw_total,
            "unique_patents": len(state.patents),
            "duplicates_removed": duplicates_removed,
            "screened": len(screenings),
            "included": len(included),
            "review": len(review),
            "excluded": len(excluded),
            "manual_review_required": len(state.manual_review_queue),
            "manual_review_deferred": review_deferred_count,
            "full_extractions": len(included) + len(review_to_process),
            "missing_abstract": missing_abstract,
            "missing_id": missing_id,
            "records_with_content_identity": dedupe_stats.get("records_with_content_identity", 0),
            "records_with_fallback_identity": dedupe_stats.get("records_with_fallback_identity", 0),
            "family_duplicates_removed": dedupe_stats.get("family_duplicates_removed", 0),
            "llm_screening_failures": llm_screening_failures,
            "llm_total_failures": evaluator.total_failures,
        }
        memory.append(
            "synthesis",
            "coverage_computed",
            "Cobertura e seleção consolidadas após triagem.",
            state.coverage_metrics,
        )

        log_event(
            logger,
            logging.INFO,
            "screening_completed",
            screened=len(screenings),
            included=len(included),
            review=len(review),
            excluded=len(excluded),
            manual_review_queue=len(state.manual_review_queue),
        )
        _record_stage_metric(
            state,
            "screening",
            screening_start,
            time.perf_counter(),
            "degraded" if llm_screening_failures or evaluator.is_degraded() else "ok",
            items_processed=len(screenings),
            detail=f"{len(included)} incluídas, {len(state.manual_review_queue)} revisão",
        )
    else:
        log_event(
            logger,
            logging.WARNING,
            "screening_skipped",
            reason="LLM indisponível",
            patents=len(state.patents),
        )
        review_limit = config.SCREEN_MAX_ITEMS_FOR_REVIEW
        state.evaluations = [
            PatentEvaluation(
                record_id=patent.record_id,
                patent_id=patent.patent_id,
                screening_score=0.0,
                screening_decision="review",
                screening_reason="LLM indisponível.",
                manual_review_required=True,
                llm_error="LLM indisponível.",
            )
            for patent in state.patents
        ]
        state.manual_review_queue, review_deferred_count = _build_manual_review_queue(
            state.patents,
            state.evaluations,
            review_limit if pipeline_features.enable_manual_review_queue else 0,
        )
        state.coverage_metrics = {
            "raw_scraped": raw_total,
            "unique_patents": len(state.patents),
            "duplicates_removed": duplicates_removed,
            "screened": 0,
            "included": 0,
            "review": len(state.patents),
            "excluded": 0,
            "manual_review_required": len(state.manual_review_queue),
            "manual_review_deferred": review_deferred_count,
            "full_extractions": 0,
            "missing_abstract": missing_abstract,
            "missing_id": missing_id,
            "records_with_content_identity": dedupe_stats.get("records_with_content_identity", 0),
            "records_with_fallback_identity": dedupe_stats.get("records_with_fallback_identity", 0),
            "family_duplicates_removed": dedupe_stats.get("family_duplicates_removed", 0),
            "llm_screening_failures": len(state.patents),
            "llm_total_failures": 0,
        }

        state.thematic_clusters = {"clusters": [], "total_clusters": 0}
        memory.append(
            "synthesis",
            "llm_unavailable",
            "Síntese temática desativada porque o LLM não está disponível.",
        )
        _record_stage_metric(
            state,
            "screening",
            screening_start,
            time.perf_counter(),
            "skipped",
            items_processed=len(state.patents),
            detail="LLM indisponível",
        )

    state.prisma_flow = (
        _prisma_stage_artifact(state, state.coverage_metrics)
        if pipeline_features.enable_prisma
        else {}
    )
    state.memory_sidecar = memory.to_dict()
    state.memory_journal = [entry.to_dict() for entry in memory.journal]
    state.llm_cache_stats = evaluator.cache_stats()
    state.llm_telemetry = evaluator.telemetry_stats()
    state.rerank_duration_seconds = round(
        state.llm_telemetry.get("operations", {}).get("rerank", {}).get("total_duration_seconds", 0.0),
        3,
    )
    store.save(state)

    synthesis_start = time.perf_counter()
    comparative_status = "disabled_or_skipped"
    comparative_detail = "Síntese comparativa"
    if (
        state.llm_available
        and len(state.patents) > 1
        and pipeline_features.enable_comparative_analysis
        and not evaluator.is_degraded()
    ):
        _log_stage(
            "comparative_analysis",
            "Gerando análise comparativa",
            eligible_patents=len(state.evaluations),
        )

        comp_start = time.perf_counter()
        print_progress("Gerando análise comparativa com IA")
        analysis_eval_map = _evaluation_map(state.evaluations)
        analysis_patents = [
            patent for patent in state.patents
            if (
                _entity_key(patent.record_id, patent.patent_id) in analysis_eval_map
                and not analysis_eval_map[_entity_key(patent.record_id, patent.patent_id)].llm_error
            )
        ]
        analysis_evaluations = [
            analysis_eval_map[_entity_key(patent.record_id, patent.patent_id)]
            for patent in analysis_patents
            if _entity_key(patent.record_id, patent.patent_id) in analysis_eval_map
        ]
        if len(analysis_patents) > 1 and len(analysis_evaluations) > 1:
            state.comparative_analysis = evaluator.generate_comparative_analysis(
                analysis_patents,
                analysis_evaluations,
                query,
            )
            if state.comparative_analysis == COMPARATIVE_ANALYSIS_NO_INPUT:
                comparative_status = "skipped"
                comparative_detail = "Nenhuma patente elegível para síntese comparativa"
                memory.append(
                    "synthesis",
                    "comparative_analysis_skipped",
                    "Síntese comparativa pulada por falta de patentes elegíveis.",
                    {"patents_compared": 0},
                )
                log_event(
                    logger,
                    logging.INFO,
                    "comparative_analysis_skipped",
                    reason="Nenhuma patente elegível para síntese comparativa",
                )
            elif has_substantive_comparative_analysis(state.comparative_analysis):
                comparative_status = "ok"
                comparative_detail = "Síntese comparativa gerada"
                memory.append(
                    "synthesis",
                    "comparative_analysis_completed",
                    "Síntese comparativa gerada via Ollama.",
                    {"patents_compared": len(analysis_patents)},
                )
            else:
                comparative_status = "degraded"
                comparative_detail = "Fallback da síntese comparativa"
                state.errors.append("Falha na geração da análise comparativa via Ollama.")
                memory.append(
                    "synthesis",
                    "comparative_analysis_fallback",
                    "Síntese comparativa caiu em fallback após falha do Ollama.",
                    {"patents_compared": len(analysis_patents)},
                )
                log_event(
                    logger,
                    logging.WARNING,
                    "comparative_analysis_fallback",
                    patents_compared=len(analysis_patents),
                )
        else:
            state.comparative_analysis = COMPARATIVE_ANALYSIS_NO_INPUT
            comparative_status = "skipped"
            comparative_detail = "Nenhuma patente elegível para síntese comparativa"
            memory.append(
                "synthesis",
                "comparative_analysis_skipped",
                "Síntese comparativa pulada por falta de patentes elegíveis.",
                {"patents_compared": 0},
            )
            log_event(
                logger,
                logging.INFO,
                "comparative_analysis_skipped",
                reason="Nenhuma patente elegível para síntese comparativa",
            )
        state.comparative_analysis_duration_seconds = round(
            time.perf_counter() - comp_start,
            3,
        )
        if comparative_status == "ok":
            log_event(
                logger,
                logging.INFO,
                "comparative_analysis_completed",
                patents_compared=len(analysis_patents),
                duration_seconds=state.comparative_analysis_duration_seconds,
            )
    elif not pipeline_features.enable_comparative_analysis:
        state.comparative_analysis = ""
        comparative_status = "disabled"
        comparative_detail = "Feature de síntese comparativa desabilitada"
    elif state.llm_available and evaluator.is_degraded():
        state.comparative_analysis = ""
        comparative_status = "degraded"
        comparative_detail = "Circuit breaker do LLM ativo; síntese comparativa pulada"
    elif not state.llm_available:
        state.comparative_analysis = ""
        comparative_status = "skipped"
        comparative_detail = "LLM indisponível para síntese comparativa"
    else:
        state.comparative_analysis = ""
        comparative_status = "skipped"
        comparative_detail = "Síntese comparativa requer ao menos 2 patentes"
    _record_stage_metric(
        state,
        "comparative_analysis",
        synthesis_start,
        time.perf_counter(),
        comparative_status,
        items_processed=len(state.evaluations),
        detail=comparative_detail,
    )
    whitespace_start = time.perf_counter()
    whitespace_status = "skipped"
    whitespace_detail = "Whitespace analysis indisponível"
    state.whitespace_analysis = {}
    if not pipeline_features.enable_whitespace_analysis:
        whitespace_status = "disabled"
        whitespace_detail = "Feature de whitespace analysis desabilitada"
    elif len(state.evaluations) > 1 and hasattr(evaluator, "generate_whitespace_analysis"):
        state.whitespace_analysis = evaluator.generate_whitespace_analysis(
            state.patents,
            state.evaluations,
            query,
        )
        if state.whitespace_analysis.get("status") == "ok":
            whitespace_status = "ok"
            whitespace_detail = "Whitespace analysis estruturada gerada"
            memory.append(
                "synthesis",
                "whitespace_analysis_completed",
                "Matriz estruturada de whitespace gerada.",
                {
                    "selected_patents": state.whitespace_analysis.get("corpus_summary", {}).get("selected_patents", 0),
                    "candidates": len(state.whitespace_analysis.get("whitespace_candidates", [])),
                },
            )
            log_event(
                logger,
                logging.INFO,
                "whitespace_analysis_completed",
                selected_patents=state.whitespace_analysis.get("corpus_summary", {}).get("selected_patents", 0),
                candidates=len(state.whitespace_analysis.get("whitespace_candidates", [])),
            )
        else:
            whitespace_detail = "Whitespace analysis sem corpus elegível"
    _record_stage_metric(
        state,
        "whitespace_analysis",
        whitespace_start,
        time.perf_counter(),
        whitespace_status,
        items_processed=len(state.whitespace_analysis.get("coverage_matrix", [])),
        detail=whitespace_detail,
    )
    state.prisma_flow = (
        _prisma_stage_artifact(state, state.coverage_metrics)
        if pipeline_features.enable_prisma
        else {}
    )
    state.llm_cache_stats = evaluator.cache_stats()
    state.llm_telemetry = evaluator.telemetry_stats()
    state.rerank_duration_seconds = round(
        state.llm_telemetry.get("operations", {}).get("rerank", {}).get("total_duration_seconds", 0.0),
        3,
    )
    state.observability_metrics = _build_observability_metrics(state)

    _log_stage("reporting", "Gerando relatórios", output_dir=output_dir)

    report_start = time.perf_counter()
    state.writing_context = _build_writing_context(state)
    memory.set_slot(
        "writer",
        {
            "top_patents": state.writing_context.get("top_patents", []),
            "route_summary": state.writing_context.get("route_summary", {}),
        },
        overwrite=True,
    )
    memory.append(
        "writer",
        "context_prepared",
        "Contexto compartilhado preparado para o writer.",
        {
            "top_patents": len(state.writing_context.get("top_patents", [])),
            "route_summary": state.writing_context.get("route_summary", {}),
        },
    )
    state.memory_sidecar = memory.to_dict()
    state.memory_journal = [entry.to_dict() for entry in memory.journal]
    reporter = ReportGenerator(output_dir=output_dir)
    md_path, json_path = reporter.generate_report(
        query,
        state.patents,
        state.evaluations,
        state.comparative_analysis,
        run_metadata=state.to_dict(),
    )
    state.output_paths = {
        "markdown": os.path.abspath(md_path),
        "json": os.path.abspath(json_path),
        "state": os.path.abspath(store.state_path),
    }
    _record_stage_metric(
        state,
        "reporting",
        report_start,
        time.perf_counter(),
        "ok",
        items_processed=len(state.evaluations),
        detail="Relatórios Markdown e JSON",
    )

    state.status = "completed"
    state.finished_at = datetime.now().isoformat(timespec="seconds")
    state.total_duration_seconds = round(time.perf_counter() - start_time, 3)
    finalize_start = time.perf_counter()
    memory.append(
        "finalization",
        "report_generated",
        "Relatórios finais gerados com sucesso.",
        {"markdown": md_path, "json": json_path},
    )
    state.memory_sidecar = memory.to_dict()
    state.memory_journal = [entry.to_dict() for entry in memory.journal]
    if pipeline_features.enable_prisma and state.prisma_flow:
        prisma_path = store.save_artifact(f"prisma_flow_{state.run_id}.json", state.prisma_flow)
        state.output_paths["prisma"] = os.path.abspath(prisma_path)
    if pipeline_features.enable_snapshot and state.config_snapshot:
        snapshot_path = store.save_artifact(f"config_snapshot_{state.run_id}.json", state.config_snapshot)
        state.output_paths["snapshot"] = os.path.abspath(snapshot_path)
    if state.whitespace_analysis:
        whitespace_path = store.save_artifact(
            f"whitespace_analysis_{state.run_id}.json",
            state.whitespace_analysis,
        )
        state.output_paths["whitespace_json"] = os.path.abspath(whitespace_path)
    journal_path = store.save_artifact(f"memory_journal_{state.run_id}.json", state.memory_journal)
    sidecar_path = store.save_artifact(f"memory_sidecar_{state.run_id}.json", state.memory_sidecar)
    state.output_paths["memory_journal"] = os.path.abspath(journal_path)
    state.output_paths["memory_sidecar"] = os.path.abspath(sidecar_path)
    _record_stage_metric(
        state,
        "finalization",
        finalize_start,
        time.perf_counter(),
        "ok",
        items_processed=len(state.output_paths),
        detail="Persistência de artefatos e estado",
    )
    reporter.write_report_files(
        state.output_paths["markdown"],
        state.output_paths["json"],
        query,
        state.patents,
        state.evaluations,
        state.comparative_analysis,
        run_metadata=state.to_dict(),
    )
    store.save(state)

    log_event(
        logger,
        logging.INFO,
        "reports_generated",
        markdown=state.output_paths.get("markdown", ""),
        json=state.output_paths.get("json", ""),
        prisma=state.output_paths.get("prisma", ""),
        snapshot=state.output_paths.get("snapshot", ""),
        whitespace_json=state.output_paths.get("whitespace_json", ""),
        memory_journal=state.output_paths.get("memory_journal", ""),
        memory_sidecar=state.output_paths.get("memory_sidecar", ""),
    )

    summary_fields = {
        "query": query,
        "patents_found": len(state.patents),
        "total_duration_seconds": round(state.total_duration_seconds, 1),
    }
    if state.coverage_metrics:
        summary_fields.update({
            "duplicates_removed": state.coverage_metrics.get("duplicates_removed", 0),
            "screened": state.coverage_metrics.get("screened", 0),
            "included": state.coverage_metrics.get("included", 0),
            "review": state.coverage_metrics.get("review", 0),
        })
    if state.llm_available:
        scored = [
            e for e in state.evaluations
            if e.screening_decision == "include" and not e.llm_error
        ]
        avg_score = (
            sum(e.relevance_score for e in scored) / len(scored)
            if scored
            else 0
        )
        summary_fields["average_relevance_score"] = round(avg_score, 1)

        top_patents = sorted(
            _pair_patents_with_evaluations(state.patents, state.evaluations),
            key=lambda x: x[1].relevance_score,
            reverse=True,
        )[:3]

        if top_patents:
            for i, (patent, evaluation) in enumerate(top_patents, 1):
                log_event(
                    logger,
                    logging.INFO,
                    "top_patent",
                    rank=i,
                    patent_id=_display_patent_id(patent),
                    relevance_score=evaluation.relevance_score,
                    title=patent.title[:60],
                )

    log_event(
        logger,
        logging.INFO,
        "run_summary",
        **summary_fields,
    )

    if state.manual_review_queue:
        patent_map = {
            patent.record_id: patent
            for patent in state.patents
        }
        for item in state.manual_review_queue[:10]:
            record_id = item.get("record_id", "")
            patent = patent_map.get(record_id)
            if patent:
                log_event(
                    logger,
                    logging.INFO,
                    "manual_review_item",
                    record_id=record_id,
                    patent_id=_display_patent_id(patent),
                    route=item.get("route", "N/A"),
                )
            else:
                log_event(
                    logger,
                    logging.INFO,
                    "manual_review_item",
                    record_id=record_id,
                    route=item.get("route", "N/A"),
                )
        if len(state.manual_review_queue) > 10:
            log_event(
                logger,
                logging.INFO,
                "manual_review_overflow",
                omitted=len(state.manual_review_queue) - 10,
            )

    if state.thematic_clusters and state.thematic_clusters.get("clusters"):
        for cluster in state.thematic_clusters["clusters"][:5]:
            log_event(
                logger,
                logging.INFO,
                "thematic_cluster_summary",
                cluster=cluster["cluster"],
                patents=cluster["count"],
                average_score=round(cluster["average_score"], 1),
            )

    if state.errors:
        for error in state.errors:
            log_event(
                logger,
                logging.WARNING,
                "run_error",
                detail=error,
            )

    log_event(
        logger,
        logging.INFO,
        "run_completed",
        status=state.status,
        total_duration_seconds=round(state.total_duration_seconds, 1),
        output_paths=state.output_paths,
    )
    return state
