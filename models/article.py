"""
Modelos de dados para o pipeline de análise de artigo → whitespace.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class TargetClaim:
    id: int
    text: str
    type: str  # "method" | "system" | "composition" | "use"
    is_independent: bool = True

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "text": self.text,
            "type": self.type,
            "is_independent": self.is_independent,
        }


@dataclass
class ArticleAnalysis:
    article_title: str
    core_innovation: str
    novelty_hypothesis: str
    claims: List[TargetClaim] = field(default_factory=list)
    search_queries: List[str] = field(default_factory=list)
    technical_dimensions: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "article_title": self.article_title,
            "core_innovation": self.core_innovation,
            "novelty_hypothesis": self.novelty_hypothesis,
            "claims": [c.to_dict() for c in self.claims],
            "search_queries": self.search_queries,
            "technical_dimensions": self.technical_dimensions,
        }

    def claims_text(self) -> str:
        return "\n".join(f"{c.id}. [{c.type}] {c.text}" for c in self.claims)


@dataclass
class PatentExtraction:
    record_id: str
    patent_id: str
    core_contribution: str
    covers_claims: List[int] = field(default_factory=list)
    partial_coverage: List[dict] = field(default_factory=list)  # [{"claim_id": int, "aspect": str}]
    similarity: str = "low"  # "high" | "medium" | "low"
    distinguishing_factors: str = ""

    def to_dict(self) -> dict:
        return {
            "record_id": self.record_id,
            "patent_id": self.patent_id,
            "core_contribution": self.core_contribution,
            "covers_claims": self.covers_claims,
            "partial_coverage": self.partial_coverage,
            "similarity": self.similarity,
            "distinguishing_factors": self.distinguishing_factors,
        }


@dataclass
class ClaimCoverage:
    claim_id: int
    claim_text: str
    status: str  # "covered" | "partial" | "whitespace"
    covering_patents: List[str] = field(default_factory=list)
    partial_patents: List[dict] = field(default_factory=list)  # [{"patent_id": str, "aspect": str}]

    def to_dict(self) -> dict:
        return {
            "claim_id": self.claim_id,
            "claim_text": self.claim_text,
            "status": self.status,
            "covering_patents": self.covering_patents,
            "partial_patents": self.partial_patents,
        }


@dataclass
class ArticleWhitespaceReport:
    status: str
    claim_coverage: List[ClaimCoverage] = field(default_factory=list)
    whitespace_claims: List[int] = field(default_factory=list)
    partial_claims: List[int] = field(default_factory=list)
    covered_claims: List[int] = field(default_factory=list)
    whitespace_score: float = 0.0
    narrative: str = ""
    recommended_queries: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "status": self.status,
            "claim_coverage": [c.to_dict() for c in self.claim_coverage],
            "whitespace_claims": self.whitespace_claims,
            "partial_claims": self.partial_claims,
            "covered_claims": self.covered_claims,
            "whitespace_score": self.whitespace_score,
            "narrative": self.narrative,
            "recommended_queries": self.recommended_queries,
        }
