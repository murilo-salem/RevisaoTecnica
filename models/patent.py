"""
Modelos de dados para patentes e avaliações.
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Patent:
    """Representa uma patente encontrada via scraping."""
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
        if len(self.inventors) > 3:
            inventors_str += " et al."
        return (
            f"[{self.patent_id}] {self.title}\n"
            f"  Inventores: {inventors_str or 'N/A'}\n"
            f"  Assignee: {self.assignee or 'N/A'}\n"
            f"  Data: {self.publication_date or self.filing_date or 'N/A'}"
        )


@dataclass
class PatentEvaluation:
    """Resultado da avaliação de uma patente pelo LLM."""
    patent_id: str = ""
    relevance_score: float = 0.0  # 0-10
    summary: str = ""
    key_findings: List[str] = field(default_factory=list)
    potential_applications: List[str] = field(default_factory=list)
    technical_domain: str = ""
    innovation_level: str = ""  # "Incremental", "Significativa", "Disruptiva"

    def to_dict(self) -> dict:
        return {
            "patent_id": self.patent_id,
            "relevance_score": self.relevance_score,
            "summary": self.summary,
            "key_findings": self.key_findings,
            "potential_applications": self.potential_applications,
            "technical_domain": self.technical_domain,
            "innovation_level": self.innovation_level,
        }
