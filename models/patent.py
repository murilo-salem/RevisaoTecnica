"""
Modelos de dados para patentes e avaliações.
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Patent:
    """Representa uma patente encontrada via scraping."""
    record_id: str = ""
    family_id: str = ""
    title: str = ""
    patent_id: str = ""
    abstract: str = ""
    inventors: List[str] = field(default_factory=list)
    assignee: str = ""
    filing_date: str = ""
    publication_date: str = ""
    url: str = ""
    snippet: str = ""
    source: str = ""  # ex: "Google Patents", "Lens.org"

    def to_dict(self) -> dict:
        return {
            "record_id": self.record_id,
            "family_id": self.family_id,
            "title": self.title,
            "patent_id": self.patent_id,
            "abstract": self.abstract,
            "inventors": self.inventors,
            "assignee": self.assignee,
            "filing_date": self.filing_date,
            "publication_date": self.publication_date,
            "url": self.url,
            "snippet": self.snippet,
            "source": self.source,
        }

    def short_description(self) -> str:
        """Descrição curta para exibição."""
        inventors_str = ", ".join(self.inventors[:3])
        display_id = self.patent_id or self.record_id or "N/A"
        if len(self.inventors) > 3:
            inventors_str += " et al."
        return (
            f"[{display_id}] {self.title}\n"
            f"  Inventores: {inventors_str or 'N/A'}\n"
            f"  Assignee: {self.assignee or 'N/A'}\n"
            f"  Data: {self.publication_date or self.filing_date or 'N/A'}"
        )


@dataclass
class PatentEvaluation:
    """Resultado da avaliação de uma patente pelo LLM."""
    record_id: str = ""
    patent_id: str = ""
    analysis_route: str = ""
    route_reason: str = ""
    screening_score: float = 0.0
    screening_decision: str = ""
    screening_reason: str = ""
    evidence_snippets: List[str] = field(default_factory=list)
    thematic_cluster: str = ""
    relevance_score: float = 0.0  # 0-10
    summary: str = ""
    key_findings: List[str] = field(default_factory=list)
    potential_applications: List[str] = field(default_factory=list)
    technical_domain: str = ""
    innovation_level: str = ""  # "Incremental", "Significativa", "Disruptiva"
    co2_role: str = ""
    storage_role: str = ""
    system_boundary: str = ""
    cycle_type: str = ""
    heat_source_sink: str = ""
    claim_focus: str = ""
    exclusion_category: str = ""
    problem_statement: str = ""
    solution_summary: str = ""
    claimed_advantages: List[str] = field(default_factory=list)
    limitations: List[str] = field(default_factory=list)
    maturity_level: str = ""
    confidence: float = 0.0
    rerank_applied: bool = False
    rerank_reason: str = ""
    manual_review_required: bool = False
    llm_error: str = ""

    def to_dict(self) -> dict:
        return {
            "record_id": self.record_id,
            "patent_id": self.patent_id,
            "analysis_route": self.analysis_route,
            "route_reason": self.route_reason,
            "screening_score": self.screening_score,
            "screening_decision": self.screening_decision,
            "screening_reason": self.screening_reason,
            "evidence_snippets": self.evidence_snippets,
            "thematic_cluster": self.thematic_cluster,
            "relevance_score": self.relevance_score,
            "summary": self.summary,
            "key_findings": self.key_findings,
            "potential_applications": self.potential_applications,
            "technical_domain": self.technical_domain,
            "innovation_level": self.innovation_level,
            "co2_role": self.co2_role,
            "storage_role": self.storage_role,
            "system_boundary": self.system_boundary,
            "cycle_type": self.cycle_type,
            "heat_source_sink": self.heat_source_sink,
            "claim_focus": self.claim_focus,
            "exclusion_category": self.exclusion_category,
            "problem_statement": self.problem_statement,
            "solution_summary": self.solution_summary,
            "claimed_advantages": self.claimed_advantages,
            "limitations": self.limitations,
            "maturity_level": self.maturity_level,
            "confidence": self.confidence,
            "rerank_applied": self.rerank_applied,
            "rerank_reason": self.rerank_reason,
            "manual_review_required": self.manual_review_required,
            "llm_error": self.llm_error,
        }
