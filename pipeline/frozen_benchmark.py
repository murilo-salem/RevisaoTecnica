"""
Componentes offline para benchmark congelado do pipeline.
"""

from __future__ import annotations

import json
from typing import Callable, Dict, List, Tuple

from models.patent import Patent, PatentEvaluation
from scraper.base import BaseScraper


def _patent_from_payload(payload: Dict[str, object]) -> Patent:
    patent = Patent(
        title=str(payload.get("title", "")),
        patent_id=str(payload.get("patent_id", "")),
        abstract=str(payload.get("abstract", "")),
        inventors=[str(item) for item in payload.get("inventors", [])],
        assignee=str(payload.get("assignee", "")),
        filing_date=str(payload.get("filing_date", "")),
        publication_date=str(payload.get("publication_date", "")),
        url=str(payload.get("url", "")),
        snippet=str(payload.get("snippet", "")),
        source=str(payload.get("source", "")),
    )
    return patent


def _build_scrapers_from_patents(patents: List[Patent]) -> List[BaseScraper]:
    by_source: Dict[str, List[Patent]] = {}
    for patent in patents:
        source_name = patent.source or "Frozen"
        by_source.setdefault(source_name, []).append(patent)
    return [
        FrozenScraper(source_patents, source_name=source_name)
        for source_name, source_patents in by_source.items()
    ]


def _evaluation_from_payload(payload: Dict[str, object], patent: Patent) -> PatentEvaluation:
    evaluation = PatentEvaluation(
        patent_id=patent.patent_id,
        screening_score=float(payload.get("screening_score", 0) or 0),
        screening_decision=str(payload.get("screening_decision", "")),
        screening_reason=str(payload.get("screening_reason", "")),
        evidence_snippets=[str(item) for item in payload.get("evidence_snippets", [])],
        thematic_cluster=str(payload.get("thematic_cluster", "")),
        relevance_score=float(payload.get("relevance_score", 0) or 0),
        summary=str(payload.get("summary", "")),
        key_findings=[str(item) for item in payload.get("key_findings", [])],
        potential_applications=[str(item) for item in payload.get("potential_applications", [])],
        technical_domain=str(payload.get("technical_domain", "")),
        innovation_level=str(payload.get("innovation_level", "")),
        co2_role=str(payload.get("co2_role", "")),
        storage_role=str(payload.get("storage_role", "")),
        system_boundary=str(payload.get("system_boundary", "")),
        cycle_type=str(payload.get("cycle_type", "")),
        heat_source_sink=str(payload.get("heat_source_sink", "")),
        claim_focus=str(payload.get("claim_focus", "")),
        exclusion_category=str(payload.get("exclusion_category", "")),
        problem_statement=str(payload.get("problem_statement", "")),
        solution_summary=str(payload.get("solution_summary", "")),
        claimed_advantages=[str(item) for item in payload.get("claimed_advantages", [])],
        limitations=[str(item) for item in payload.get("limitations", [])],
        maturity_level=str(payload.get("maturity_level", "")),
        confidence=float(payload.get("confidence", 0) or 0),
        rerank_applied=bool(payload.get("rerank_applied", False)),
        rerank_reason=str(payload.get("rerank_reason", "")),
        manual_review_required=bool(payload.get("manual_review_required", False)),
        llm_error=str(payload.get("llm_error", "")),
    )
    return evaluation


class FrozenScraper(BaseScraper):
    """Scraper offline com corpus local congelado."""

    def __init__(self, patents: List[Patent], source_name: str):
        super().__init__()
        self._patents = patents
        self.source_name = source_name

    def search(self, query: str, max_results: int = 10) -> List[Patent]:
        return [
            Patent(**patent.to_dict())
            for patent in self._patents[:max_results]
        ]

    def get_patent_details(self, patent_url: str) -> Patent:
        for patent in self._patents:
            if patent.url == patent_url:
                return Patent(**patent.to_dict())
        return Patent(url=patent_url, source=self.source_name)


class FrozenEvaluator:
    """Evaluator determinístico para benchmark offline."""

    def __init__(
        self,
        evaluations: Dict[str, Dict[str, object]],
        comparative_analysis: str,
        whitespace_analysis: Dict[str, object] | None = None,
    ):
        self._evaluations = evaluations
        self._comparative_analysis = comparative_analysis
        self._whitespace_analysis = whitespace_analysis or {}
        self.cache_hits = 0
        self.cache_misses = 0

    def check_connection(self) -> bool:
        return True

    @property
    def total_failures(self) -> int:
        return 0

    def is_degraded(self) -> bool:
        return False

    def cache_stats(self) -> Dict[str, int]:
        return {
            "hits": self.cache_hits,
            "misses": self.cache_misses,
            "entries": 0,
        }

    def telemetry_stats(self) -> Dict[str, object]:
        return {
            "degraded": False,
            "total_failures": 0,
            "consecutive_failures": 0,
            "recent_errors": [],
            "operations": {
                "screening": {
                    "calls": len(self._evaluations),
                    "successes": len(self._evaluations),
                    "failures": 0,
                    "retries": 0,
                    "cache_hits": 0,
                    "degraded_skips": 0,
                    "prompt_chars": 0,
                    "response_chars": 0,
                    "total_duration_seconds": 0.0,
                    "average_duration_seconds": 0.0,
                    "max_duration_seconds": 0.0,
                }
            },
        }

    def _payload_for_patent(self, patent: Patent) -> Dict[str, object]:
        key = patent.patent_id or patent.title
        return self._evaluations.get(key, {})

    def screen_patent(
        self,
        patent: Patent,
        search_context: str,
        require_evidence: bool = True,
        enable_thematic_clusters: bool = True,
        enable_structural_roles: bool = True,
        enable_screening_rerank: bool = True,
    ) -> PatentEvaluation:
        payload = self._payload_for_patent(patent)
        evaluation = _evaluation_from_payload(payload, patent)
        evaluation.record_id = patent.record_id
        if not enable_structural_roles:
            evaluation.co2_role = ""
            evaluation.storage_role = ""
            evaluation.system_boundary = ""
            evaluation.cycle_type = ""
            evaluation.heat_source_sink = ""
            evaluation.claim_focus = ""
            evaluation.exclusion_category = ""
        if not enable_screening_rerank:
            evaluation.rerank_applied = False
            evaluation.rerank_reason = ""
        if not evaluation.screening_decision:
            evaluation.screening_decision = "review"
            evaluation.screening_reason = "Patente sem avaliação congelada."
            evaluation.manual_review_required = True
        return evaluation

    def evaluate_patent(
        self,
        patent: Patent,
        search_context: str,
        screening: PatentEvaluation | None = None,
        require_evidence: bool = True,
        enable_thematic_clusters: bool = True,
        enable_structural_roles: bool = True,
        enable_screening_rerank: bool = True,
    ) -> PatentEvaluation:
        if screening is None:
            screening = self.screen_patent(
                patent,
                search_context,
                require_evidence=require_evidence,
                enable_thematic_clusters=enable_thematic_clusters,
                enable_structural_roles=enable_structural_roles,
                enable_screening_rerank=enable_screening_rerank,
            )
        payload = self._payload_for_patent(patent)
        evaluation = _evaluation_from_payload(payload, patent)
        evaluation.record_id = patent.record_id
        evaluation.screening_score = screening.screening_score
        evaluation.screening_decision = screening.screening_decision
        evaluation.screening_reason = screening.screening_reason
        evaluation.analysis_route = screening.analysis_route
        evaluation.route_reason = screening.route_reason
        evaluation.manual_review_required = screening.manual_review_required
        if not enable_structural_roles:
            evaluation.co2_role = ""
            evaluation.storage_role = ""
            evaluation.system_boundary = ""
            evaluation.cycle_type = ""
            evaluation.heat_source_sink = ""
            evaluation.claim_focus = ""
            evaluation.exclusion_category = ""
        if not enable_screening_rerank:
            evaluation.rerank_applied = False
            evaluation.rerank_reason = ""
        if not evaluation.evidence_snippets:
            evaluation.evidence_snippets = screening.evidence_snippets
        return evaluation

    def generate_comparative_analysis(
        self,
        patents: List[Patent],
        evaluations: List[PatentEvaluation],
        search_context: str,
    ) -> str:
        return self._comparative_analysis

    def generate_whitespace_analysis(
        self,
        patents: List[Patent],
        evaluations: List[PatentEvaluation],
        search_context: str,
    ) -> Dict[str, object]:
        if self._whitespace_analysis:
            return self._whitespace_analysis

        selected = [
            evaluation for evaluation in evaluations
            if evaluation.screening_decision in {"include", "review"} and not evaluation.llm_error
        ]
        return {
            "status": "ok" if len(selected) >= 2 else "no_input",
            "query": search_context,
            "corpus_summary": {
                "considered_patents": len(patents),
                "selected_patents": len(selected),
                "core": sum(1 for item in selected if item.screening_decision == "include"),
                "frontier": sum(1 for item in selected if item.screening_decision == "review"),
                "adjacent": 0,
            },
            "coverage_matrix": [
                {
                    "patent_id": evaluation.patent_id,
                    "bucket": "core" if evaluation.screening_decision == "include" else "frontier",
                    "co2_role": evaluation.co2_role or "not_clear",
                    "storage_role": evaluation.storage_role or "not_clear",
                    "system_boundary": evaluation.system_boundary or "not_clear",
                    "cycle_type": evaluation.cycle_type or "not_clear",
                    "heat_source_sink": evaluation.heat_source_sink or "not_clear",
                    "claim_focus": evaluation.claim_focus or "not_clear",
                    "exclusion_category": evaluation.exclusion_category or "",
                }
                for evaluation in selected
            ],
            "axes": {},
            "whitespace_candidates": [],
            "markdown_summary": "",
        }


def build_frozen_components(
    fixture_path: str,
) -> Tuple[List[BaseScraper], Callable[..., FrozenEvaluator]]:
    with open(fixture_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    sources = data.get("sources", {})
    scrapers: List[BaseScraper] = []
    for source_name, patents_payload in sources.items():
        patents = []
        for payload in patents_payload:
            patent = _patent_from_payload(payload)
            if not patent.source:
                patent.source = source_name
            patents.append(patent)
        scrapers.append(FrozenScraper(patents, source_name=source_name))

    evaluations = data.get("evaluations", {})
    comparative_analysis = str(data.get("comparative_analysis", ""))
    whitespace_analysis = data.get("whitespace_analysis", {})

    def evaluator_factory(**_: object) -> FrozenEvaluator:
        return FrozenEvaluator(
            evaluations=evaluations,
            comparative_analysis=comparative_analysis,
            whitespace_analysis=whitespace_analysis if isinstance(whitespace_analysis, dict) else {},
        )

    return scrapers, evaluator_factory


def build_frozen_scrapers_from_fixture(fixture_path: str) -> List[BaseScraper]:
    with open(fixture_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    patents: List[Patent] = []
    for source_name, patents_payload in data.get("sources", {}).items():
        for payload in patents_payload:
            patent = _patent_from_payload(payload)
            if not patent.source:
                patent.source = source_name
            patents.append(patent)
    return _build_scrapers_from_patents(patents)


def build_frozen_scrapers_from_run_state(run_state_path: str) -> List[BaseScraper]:
    with open(run_state_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    patents = [
        _patent_from_payload(payload)
        for payload in data.get("patents", [])
        if isinstance(payload, dict)
    ]
    return _build_scrapers_from_patents(patents)
