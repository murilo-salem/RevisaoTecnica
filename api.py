"""
API REST assíncrona para o pipeline RevisaoTecnica.

Endpoints:
  GET  /health                  — status do serviço e Ollama
  POST /runs                    — submete um run (retorna run_id imediatamente)
  GET  /runs                    — lista todos os runs (memória + arquivos)
  GET  /runs/{run_id}           — estado completo do run
  GET  /runs/{run_id}/patents   — patentes coletadas
  GET  /runs/{run_id}/evaluations — avaliações LLM
"""

from __future__ import annotations

import glob
import json
import os
from datetime import datetime
from typing import Any, List, Optional

import config
from evaluator.llm_evaluator import OllamaEvaluator
from fastapi import BackgroundTasks, FastAPI, HTTPException
from pipeline.article_orchestrator import run_article_analysis
from pipeline.features import PipelineFeatures
from pipeline.orchestrator import run_agent
from pipeline.state import RunState
from models.article_state import ArticleRunState
from pydantic import BaseModel, Field

app = FastAPI(title="RevisaoTecnica API", version="1.0.0")

# run_id → RunState (completed) | dict {"status": "queued"|"running"|"error", ...}
_jobs: dict[str, Any] = {}

# article_run_id → ArticleRunState | dict
_article_jobs: dict[str, Any] = {}


# --------------------------------------------------------------------------- #
# Schemas                                                                      #
# --------------------------------------------------------------------------- #


class ArticleRunRequest(BaseModel):
    article_text: str
    innovation_description: str
    analysis_model: str = Field(default_factory=lambda: config.OLLAMA_MODEL)
    extraction_model: str = Field(default_factory=lambda: config.OLLAMA_EXTRACTION_MODEL)
    max_results_per_query: int = Field(default=5, ge=1, le=20)
    max_queries: int = Field(default=4, ge=1, le=8)
    user_queries: Optional[List[str]] = None


class FeaturesRequest(BaseModel):
    require_evidence: bool = True
    enable_thematic_clusters: bool = True
    enable_structural_roles: bool = True
    enable_screening_rerank: bool = True
    enable_prisma: bool = True
    enable_snapshot: bool = True
    enable_comparative_analysis: bool = True
    enable_whitespace_analysis: bool = True
    enable_manual_review_queue: bool = True


class RunRequest(BaseModel):
    query: str
    max_results: int = Field(default=10, ge=1, le=50)
    model: str = Field(default_factory=lambda: config.OLLAMA_MODEL)
    include_threshold: float = Field(default_factory=lambda: config.SCREEN_INCLUDE_THRESHOLD)
    review_threshold: float = Field(default_factory=lambda: config.SCREEN_REVIEW_THRESHOLD)
    features: FeaturesRequest = Field(default_factory=FeaturesRequest)


# --------------------------------------------------------------------------- #
# Background task                                                               #
# --------------------------------------------------------------------------- #


def _execute_article_run(job_id: str, req: ArticleRunRequest) -> None:
    _article_jobs[job_id]["status"] = "running"
    try:
        def _state_sink(state):
            _article_jobs[job_id] = state

        state = run_article_analysis(
            article_text=req.article_text,
            innovation_description=req.innovation_description,
            analysis_model=req.analysis_model,
            extraction_model=req.extraction_model,
            max_results_per_query=req.max_results_per_query,
            max_queries=req.max_queries,
            state_sink=_state_sink,
            user_queries=req.user_queries,
        )
        _article_jobs[job_id] = state
    except Exception as exc:
        _article_jobs[job_id] = {"status": "error", "error": str(exc)}


def _execute_run(job_id: str, req: RunRequest) -> None:
    _jobs[job_id]["status"] = "running"
    try:
        config.SCREEN_INCLUDE_THRESHOLD = req.include_threshold
        config.SCREEN_REVIEW_THRESHOLD = req.review_threshold
        features = PipelineFeatures(
            require_evidence=req.features.require_evidence,
            enable_thematic_clusters=req.features.enable_thematic_clusters,
            enable_structural_roles=req.features.enable_structural_roles,
            enable_screening_rerank=req.features.enable_screening_rerank,
            enable_prisma=req.features.enable_prisma,
            enable_snapshot=req.features.enable_snapshot,
            enable_comparative_analysis=req.features.enable_comparative_analysis,
            enable_whitespace_analysis=req.features.enable_whitespace_analysis,
            enable_manual_review_queue=req.features.enable_manual_review_queue,
        )

        def _state_sink(state):
            _jobs[job_id] = state

        state = run_agent(
            query=req.query,
            max_results=req.max_results,
            model=req.model,
            output_dir=config.OUTPUT_DIR,
            features=features,
            state_sink=_state_sink,
        )
        _jobs[job_id] = state
    except Exception as exc:
        _jobs[job_id] = {"status": "error", "error": str(exc)}


# --------------------------------------------------------------------------- #
# Helpers                                                                       #
# --------------------------------------------------------------------------- #


def _load_run_from_file(run_id: str) -> dict | None:
    """Recupera estado de run persistido em arquivo JSON."""
    path = os.path.join(config.OUTPUT_DIR, f"run_state_{run_id}.json")
    if not os.path.isfile(path):
        return None
    with open(path) as f:
        return json.load(f)


def _job_summary(job_id: str, state: Any) -> dict:
    if isinstance(state, RunState):
        return {
            "run_id": job_id,
            "query": state.query,
            "status": state.status,
            "started_at": state.started_at,
            "finished_at": state.finished_at,
        }
    return {
        "run_id": job_id,
        "query": state.get("query", ""),
        "status": state.get("status", "unknown"),
        "started_at": state.get("started_at", ""),
        "finished_at": "",
    }


# --------------------------------------------------------------------------- #
# Endpoints                                                                     #
# --------------------------------------------------------------------------- #


@app.get("/models")
def list_models():
    """Retorna os modelos disponíveis no Ollama."""
    import httpx
    try:
        resp = httpx.get(f"{config.OLLAMA_BASE_URL}/api/tags", timeout=5)
        resp.raise_for_status()
        models = [m["name"] for m in resp.json().get("models", [])]
    except Exception:
        models = [config.OLLAMA_MODEL]
    return {"models": models}


@app.get("/health")
def health():
    try:
        ev = OllamaEvaluator()
        ollama_ok = ev.check_connection()
    except Exception:
        ollama_ok = False
    return {"status": "ok", "ollama": ollama_ok}


@app.post("/runs", status_code=202)
def create_run(req: RunRequest, background_tasks: BackgroundTasks):
    job_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    _jobs[job_id] = {
        "status": "queued",
        "query": req.query,
        "started_at": datetime.now().isoformat(timespec="seconds"),
    }
    background_tasks.add_task(_execute_run, job_id, req)
    return {"run_id": job_id, "status": "queued"}


@app.get("/runs")
def list_runs():
    results = [_job_summary(jid, s) for jid, s in _jobs.items()]

    known_ids = set(_jobs.keys())
    pattern = os.path.join(config.OUTPUT_DIR, "run_state_*.json")
    for filepath in sorted(glob.glob(pattern), reverse=True):
        fname = os.path.basename(filepath)
        file_run_id = fname.removeprefix("run_state_").removesuffix(".json")
        if file_run_id in known_ids:
            continue
        try:
            with open(filepath) as f:
                data = json.load(f)
            results.append({
                "run_id": file_run_id,
                "query": data.get("query", ""),
                "status": data.get("status", "completed"),
                "started_at": data.get("started_at", ""),
                "finished_at": data.get("finished_at", ""),
            })
        except Exception:
            pass

    results.sort(key=lambda r: r["run_id"], reverse=True)
    return results


@app.get("/runs/{run_id}")
def get_run(run_id: str):
    if run_id in _jobs:
        state = _jobs[run_id]
        return state.to_dict() if isinstance(state, RunState) else state

    data = _load_run_from_file(run_id)
    if data is None:
        raise HTTPException(status_code=404, detail="Run not found")
    return data


@app.get("/runs/{run_id}/patents")
def get_run_patents(run_id: str):
    if run_id in _jobs:
        state = _jobs[run_id]
        if isinstance(state, RunState):
            return [p.to_dict() for p in state.patents]
        if state.get("status") in ("queued", "running"):
            return []
        raise HTTPException(status_code=404, detail="Run not found")

    data = _load_run_from_file(run_id)
    if data is None:
        raise HTTPException(status_code=404, detail="Run not found")
    return data.get("patents", [])


@app.get("/runs/{run_id}/evaluations")
def get_run_evaluations(run_id: str):
    if run_id in _jobs:
        state = _jobs[run_id]
        if isinstance(state, RunState):
            return [e.to_dict() for e in state.evaluations]
        if state.get("status") in ("queued", "running"):
            return []
        raise HTTPException(status_code=404, detail="Run not found")

    data = _load_run_from_file(run_id)
    if data is None:
        raise HTTPException(status_code=404, detail="Run not found")
    return data.get("evaluations", [])


# --------------------------------------------------------------------------- #
# Article analysis endpoints                                                    #
# --------------------------------------------------------------------------- #


@app.post("/article-runs", status_code=202)
def create_article_run(req: ArticleRunRequest, background_tasks: BackgroundTasks):
    job_id = datetime.now().strftime("%Y%m%d_%H%M%S") + "_article"
    _article_jobs[job_id] = {
        "status": "queued",
        "run_id": job_id,
        "run_type": "article",
        "innovation_description": req.innovation_description,
        "started_at": datetime.now().isoformat(timespec="seconds"),
    }
    background_tasks.add_task(_execute_article_run, job_id, req)
    return {"run_id": job_id, "status": "queued"}


@app.get("/article-runs")
def list_article_runs():
    return [
        {
            "run_id": jid,
            "run_type": "article",
            "article_title": (
                state.article_title
                if isinstance(state, ArticleRunState)
                else state.get("article_title", "")
            ),
            "status": (
                state.status
                if isinstance(state, ArticleRunState)
                else state.get("status", "unknown")
            ),
            "started_at": (
                state.started_at
                if isinstance(state, ArticleRunState)
                else state.get("started_at", "")
            ),
        }
        for jid, state in _article_jobs.items()
    ]


@app.get("/article-runs/{run_id}")
def get_article_run(run_id: str):
    if run_id not in _article_jobs:
        raise HTTPException(status_code=404, detail="Article run not found")
    state = _article_jobs[run_id]
    if isinstance(state, ArticleRunState):
        return state.to_dict()
    return state
