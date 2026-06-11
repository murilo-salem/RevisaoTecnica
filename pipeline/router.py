"""
Roteador temático e de profundidade para o pipeline.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

import config
from models.patent import Patent, PatentEvaluation


@dataclass(frozen=True)
class RouteDecision:
    """Resultado do roteamento de uma patente."""

    route: str
    reason: str
    slot: str

    def to_dict(self) -> dict:
        return {
            "route": self.route,
            "reason": self.reason,
            "slot": self.slot,
        }


class ThemeRouter:
    """Política simples e explícita de roteamento por tema e evidência."""

    ROUTE_SCREEN_ONLY = "screen_only"
    ROUTE_MANUAL_REVIEW = "manual_review"
    ROUTE_DEEP_EXTRACTION = "deep_extraction"
    ROUTE_THEMATIC_SYNTHESIS = "thematic_synthesis"

    def __init__(self, priority_clusters: List[str] | None = None):
        self.priority_clusters = priority_clusters or list(config.ROUTER_PRIORITY_CLUSTERS)

    def route(self, patent: Patent, evaluation: PatentEvaluation) -> RouteDecision:
        text = " ".join([
            patent.title or "",
            patent.abstract or "",
            patent.snippet or "",
            evaluation.screening_reason or "",
            evaluation.thematic_cluster or "",
        ]).lower()

        if evaluation.screening_decision == "exclude":
            return RouteDecision(
                route=self.ROUTE_SCREEN_ONLY,
                reason="Patente excluída na triagem.",
                slot="screening",
            )

        if evaluation.llm_error:
            return RouteDecision(
                route=self.ROUTE_MANUAL_REVIEW,
                reason="Falha do LLM; revisão humana necessária.",
                slot="review",
            )

        if evaluation.screening_decision == "review":
            return RouteDecision(
                route=self.ROUTE_MANUAL_REVIEW,
                reason="Triagem indicou revisão humana.",
                slot="review",
            )

        if evaluation.confidence and evaluation.confidence < 0.55:
            return RouteDecision(
                route=self.ROUTE_MANUAL_REVIEW,
                reason="Confiança baixa na evidência extraída.",
                slot="review",
            )

        if any(cluster.lower() in text for cluster in self.priority_clusters):
            return RouteDecision(
                route=self.ROUTE_THEMATIC_SYNTHESIS,
                reason="Tema prioritário detectado para síntese aprofundada.",
                slot="synthesis",
            )

        if evaluation.evidence_snippets:
            return RouteDecision(
                route=self.ROUTE_DEEP_EXTRACTION,
                reason="Há evidência suficiente para extração detalhada.",
                slot="writer",
            )

        return RouteDecision(
            route=self.ROUTE_MANUAL_REVIEW,
            reason="Sem evidência suficiente para avançar automaticamente.",
            slot="review",
        )
