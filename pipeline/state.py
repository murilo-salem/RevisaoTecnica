"""
Estado persistido de uma execução do pipeline.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List

from models.patent import Patent, PatentEvaluation


@dataclass
class RunState:
    """Resumo persistido de uma execução."""

    query: str
    max_results: int
    model: str
    output_dir: str
    feature_flags: Dict[str, object] = field(default_factory=dict)
    config_snapshot: Dict[str, object] = field(default_factory=dict)
    snapshot_hash: str = ""
    protocol: Dict[str, object] = field(default_factory=dict)
    writing_context: Dict[str, object] = field(default_factory=dict)
    memory_sidecar: Dict[str, object] = field(default_factory=dict)
    memory_journal: List[Dict[str, object]] = field(default_factory=list)
    stage_metrics: List[Dict[str, object]] = field(default_factory=list)
    llm_cache_stats: Dict[str, int] = field(default_factory=dict)
    llm_telemetry: Dict[str, object] = field(default_factory=dict)
    observability_metrics: Dict[str, object] = field(default_factory=dict)
    run_id: str = field(default_factory=lambda: datetime.now().strftime("%Y%m%d_%H%M%S"))
    started_at: str = field(
        default_factory=lambda: datetime.now().isoformat(timespec="seconds")
    )
    finished_at: str = ""
    status: str = "running"
    current_stage: str = ""
    screened_count: int = 0
    llm_available: bool = False
    patents: List[Patent] = field(default_factory=list)
    evaluations: List[PatentEvaluation] = field(default_factory=list)
    patents_by_source: Dict[str, int] = field(default_factory=dict)
    scraper_diagnostics: Dict[str, List[Dict[str, str]]] = field(default_factory=dict)
    coverage_metrics: Dict[str, int] = field(default_factory=dict)
    manual_review_queue: List[Dict[str, object]] = field(default_factory=list)
    prisma_flow: Dict[str, object] = field(default_factory=dict)
    thematic_clusters: Dict[str, object] = field(default_factory=dict)
    whitespace_analysis: Dict[str, object] = field(default_factory=dict)
    scraper_durations: Dict[str, float] = field(default_factory=dict)
    evaluation_duration_seconds: float = 0.0
    rerank_duration_seconds: float = 0.0
    comparative_analysis_duration_seconds: float = 0.0
    total_duration_seconds: float = 0.0
    comparative_analysis: str = ""
    output_paths: Dict[str, str] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Converte o estado para JSON serializável."""
        return {
            "query": self.query,
            "max_results": self.max_results,
            "model": self.model,
            "output_dir": self.output_dir,
            "feature_flags": self.feature_flags,
            "config_snapshot": self.config_snapshot,
            "snapshot_hash": self.snapshot_hash,
            "protocol": self.protocol,
            "writing_context": self.writing_context,
            "memory_sidecar": self.memory_sidecar,
            "memory_journal": self.memory_journal,
            "stage_metrics": self.stage_metrics,
            "llm_cache_stats": self.llm_cache_stats,
            "llm_telemetry": self.llm_telemetry,
            "observability_metrics": self.observability_metrics,
            "run_id": self.run_id,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "status": self.status,
            "current_stage": self.current_stage,
            "screened_count": self.screened_count,
            "llm_available": self.llm_available,
            "patents": [patent.to_dict() for patent in self.patents],
            "evaluations": [evaluation.to_dict() for evaluation in self.evaluations],
            "patents_by_source": self.patents_by_source,
            "scraper_diagnostics": self.scraper_diagnostics,
            "coverage_metrics": self.coverage_metrics,
            "manual_review_queue": self.manual_review_queue,
            "prisma_flow": self.prisma_flow,
            "thematic_clusters": self.thematic_clusters,
            "whitespace_analysis": self.whitespace_analysis,
            "scraper_durations": self.scraper_durations,
            "evaluation_duration_seconds": self.evaluation_duration_seconds,
            "rerank_duration_seconds": self.rerank_duration_seconds,
            "comparative_analysis_duration_seconds": self.comparative_analysis_duration_seconds,
            "total_duration_seconds": self.total_duration_seconds,
            "comparative_analysis": self.comparative_analysis,
            "output_paths": self.output_paths,
            "errors": self.errors,
        }
