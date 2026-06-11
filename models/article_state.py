"""
Estado de execução do pipeline de análise de artigo.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional

from models.article import ArticleAnalysis, ArticleWhitespaceReport, PatentExtraction
from models.patent import Patent


@dataclass
class ArticleRunState:
    innovation_description: str = ""
    analysis_model: str = ""
    extraction_model: str = ""

    run_id: str = field(
        default_factory=lambda: datetime.now().strftime("%Y%m%d_%H%M%S") + "_article"
    )
    article_title: str = ""
    status: str = "queued"  # "queued" | "running" | "completed" | "error"
    current_stage: str = ""  # "article_analysis"|"search"|"extraction"|"whitespace"|"done"

    article_analysis: Optional[ArticleAnalysis] = None

    patents: List[Patent] = field(default_factory=list)
    patents_by_source: Dict[str, int] = field(default_factory=dict)
    patents_by_query: Dict[str, List[str]] = field(default_factory=dict)

    patent_extractions: List[PatentExtraction] = field(default_factory=list)
    extracted_count: int = 0

    whitespace_report: Optional[ArticleWhitespaceReport] = None

    stage_metrics: List[dict] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

    started_at: str = field(
        default_factory=lambda: datetime.now().isoformat(timespec="seconds")
    )
    finished_at: str = ""
    total_duration_seconds: float = 0.0

    def to_dict(self) -> dict:
        return {
            "run_id": self.run_id,
            "run_type": "article",
            "article_title": self.article_title,
            "innovation_description": self.innovation_description,
            "analysis_model": self.analysis_model,
            "extraction_model": self.extraction_model,
            "status": self.status,
            "current_stage": self.current_stage,
            "article_analysis": self.article_analysis.to_dict() if self.article_analysis else None,
            "patents": [p.to_dict() for p in self.patents],
            "patents_by_source": self.patents_by_source,
            "patents_by_query": self.patents_by_query,
            "patent_extractions": [e.to_dict() for e in self.patent_extractions],
            "extracted_count": self.extracted_count,
            "total_extractions": len(self.patents),
            "whitespace_report": self.whitespace_report.to_dict() if self.whitespace_report else None,
            "stage_metrics": self.stage_metrics,
            "errors": self.errors,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "total_duration_seconds": self.total_duration_seconds,
        }
