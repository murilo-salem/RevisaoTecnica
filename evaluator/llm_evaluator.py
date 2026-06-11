"""
Avaliador de patentes usando Ollama LLM.

Integra com o Ollama para triagem em duas fases, extração estruturada
e geração de análises comparativas.
"""

import json
import hashlib
import os
import logging
import re
import time
from typing import Any, Dict, List, Optional, Tuple

import requests

from analysis_utils import (
    COMPARATIVE_ANALYSIS_FALLBACK,
    COMPARATIVE_ANALYSIS_NO_INPUT,
)
import config
from logging_utils import log_event
from models.patent import Patent, PatentEvaluation

logger = logging.getLogger(__name__)


class OllamaEvaluator:
    """Avaliador de patentes usando Ollama."""

    QUERY_STOPWORDS = {
        "a",
        "an",
        "the",
        "of",
        "for",
        "to",
        "in",
        "on",
        "and",
        "or",
        "with",
        "from",
        "using",
        "use",
        "via",
        "by",
        "into",
        "through",
        "de",
        "da",
        "do",
        "das",
        "dos",
        "para",
        "com",
        "por",
        "em",
        "na",
        "no",
    }
    GENERIC_QUERY_TERMS = {
        "energy",
        "thermal",
        "storage",
        "system",
        "systems",
        "method",
        "methods",
        "process",
        "processes",
        "technology",
        "technologies",
        "generation",
        "production",
        "analysis",
        "review",
        "patent",
        "patents",
    }

    def __init__(self, model: str = None, base_url: str = None, cache_dir: str = None):
        self.requested_model = model or config.OLLAMA_MODEL
        self.model = self.requested_model
        self.base_url = base_url or config.OLLAMA_BASE_URL
        self.api_url = f"{self.base_url}/api/generate"
        self.cache_dir = cache_dir or config.LLM_CACHE_DIR
        self.cache_path = os.path.join(self.cache_dir, f"{self._safe_name(self.model)}.json")
        self.cache_enabled = config.ENABLE_LLM_CACHE
        self.cache_hits = 0
        self.cache_misses = 0
        self._response_cache: Dict[str, str] = {}
        self.last_error = ""
        self.last_health_error = ""
        self.total_failures = 0
        self.consecutive_failures = 0
        self.degraded = False
        self.recent_errors: List[Dict[str, str]] = []
        self._telemetry: Dict[str, Dict[str, Any]] = {}
        self._load_cache()

    def _safe_name(self, value: str) -> str:
        return re.sub(r"[^A-Za-z0-9_.-]+", "_", value or "model")

    def _set_active_model(self, model_name: str) -> None:
        normalized_target = self._normalize_text(model_name)
        if not normalized_target or normalized_target == self._normalize_text(self.model):
            return
        self.model = model_name
        self.cache_path = os.path.join(self.cache_dir, f"{self._safe_name(self.model)}.json")
        self._response_cache = {}
        self._load_cache()

    def _split_model_reference(self, model_name: str) -> Tuple[str, str]:
        base, _, tag = (model_name or "").partition(":")
        return self._normalize_text(base), self._normalize_text(tag)

    def _resolve_available_model(self, models: List[str]) -> str:
        requested = self.requested_model or self.model
        normalized_requested = self._normalize_text(requested)
        for model_name in models:
            if self._normalize_text(model_name) == normalized_requested:
                return model_name

        requested_base, requested_tag = self._split_model_reference(requested)
        compatible: List[str] = []
        for model_name in models:
            available_base, available_tag = self._split_model_reference(model_name)
            if available_base != requested_base:
                continue
            if not requested_tag:
                compatible.append(model_name)
                continue
            if available_tag == requested_tag or re.match(
                rf"^{re.escape(requested_tag)}(?:[-_.].+)?$",
                available_tag,
            ):
                compatible.append(model_name)

        if not compatible:
            return ""
        return sorted(compatible, key=lambda name: (len(name), name))[0]

    def _log(self, level: int, event: str, **fields: Any) -> None:
        """Emite logs estruturados do evaluator com contexto estável."""
        log_event(
            logger,
            level,
            event,
            model=self.model,
            base_url=self.base_url,
            **fields,
        )

    def _normalize_text(self, value: str) -> str:
        return re.sub(r"\s+", " ", (value or "").strip().lower())

    def _query_tokens(self, search_context: str) -> List[str]:
        tokens = re.findall(r"[a-z0-9]+", self._normalize_text(search_context))
        return [
            token
            for token in tokens
            if len(token) >= 3 and token not in self.QUERY_STOPWORDS
        ]

    def _token_in_text(self, token: str, text: str) -> bool:
        if token in {"carbon", "dioxide", "co2", "sco2"}:
            return any(
                alias in text
                for alias in (
                    "carbon dioxide",
                    "co2",
                    "sco2",
                    "supercritical carbon dioxide",
                    "transcritical carbon dioxide",
                )
            )
        return re.search(rf"\b{re.escape(token)}\b", text) is not None

    def _contains_any_phrase(self, text: str, phrases: List[str]) -> bool:
        return any(phrase in text for phrase in phrases)

    def _focus_profile(self, patent: Patent) -> Dict[str, Any]:
        title_text = self._normalize_text(patent.title)
        body_text = self._normalize_text(" ".join([
            patent.title,
            patent.abstract,
            patent.snippet,
        ]))
        co2_aliases = (
            "carbon dioxide",
            "co2",
            "sco2",
            "supercritical carbon dioxide",
            "transcritical carbon dioxide",
        )
        storage_phrases = (
            "thermal energy storage",
            "energy storage",
            "thermal storage",
            "heat storage",
            "storage tank",
            "storage system",
        )
        thermal_terms = (
            "thermal",
            "heat",
            "isothermal",
            "temperature",
            "heat exchanger",
        )

        profile = {
            "title_co2": self._contains_any_phrase(title_text, list(co2_aliases)),
            "body_co2": self._contains_any_phrase(body_text, list(co2_aliases)),
            "title_storage": self._contains_any_phrase(title_text, list(storage_phrases)),
            "body_storage": self._contains_any_phrase(body_text, list(storage_phrases)),
            "title_thermal": self._contains_any_phrase(title_text, list(thermal_terms)),
            "body_thermal": self._contains_any_phrase(body_text, list(thermal_terms)),
            "carbon_storage_phrase": self._contains_any_phrase(
                body_text,
                [
                    "carbon dioxide energy storage",
                    "co2 energy storage",
                    "compressed carbon dioxide energy storage",
                    "supercritical compressed carbon dioxide energy storage",
                ],
            ),
            "thermal_storage_phrase": self._contains_any_phrase(
                body_text,
                [
                    "thermal energy storage",
                    "thermal storage",
                    "heat storage",
                ],
            ),
            "supercritical_focus": self._contains_any_phrase(
                body_text,
                ["supercritical", "transcritical", "isothermal and isobaric"],
            ),
            "underground_focus": self._contains_any_phrase(
                body_text,
                ["underground", "underwater", "subsurface", "subterranean"],
            ),
            "transmission_focus": self._contains_any_phrase(
                title_text,
                ["transmission", "transfer"],
            ),
            "cooling_focus": self._contains_any_phrase(
                body_text,
                ["cooling", "refrigeration", "subcool"],
            ),
            "capture_focus": self._contains_any_phrase(
                body_text,
                ["capture", "adsorption", "sorbent", "carbonator", "absorption"],
            ),
            "industrial_heat_focus": self._contains_any_phrase(
                body_text,
                ["calcination", "material activation", "steam generation", "hydrogen electrolysis"],
            ),
            "power_plant_focus": self._contains_any_phrase(
                body_text,
                ["power plant", "steam turbine", "peak shaving"],
            ),
            "work_cycle_focus": self._contains_any_phrase(
                body_text,
                ["mechanical work", "producing work", "ejector", "expansion machine"],
            ),
        }

        positive = 0.0
        if profile["title_co2"]:
            positive += 0.25
        elif profile["body_co2"]:
            positive += 0.18
        if profile["title_storage"]:
            positive += 0.22
        elif profile["body_storage"]:
            positive += 0.16
        if profile["title_thermal"]:
            positive += 0.12
        elif profile["body_thermal"]:
            positive += 0.08
        if profile["carbon_storage_phrase"]:
            positive += 0.18
        if profile["thermal_storage_phrase"]:
            positive += 0.12
        if profile["supercritical_focus"]:
            positive += 0.06
        if profile["underground_focus"]:
            positive += 0.04

        negative = 0.0
        if profile["transmission_focus"] and not profile["title_storage"]:
            negative += 0.08
        if profile["cooling_focus"]:
            negative += 0.10
        if profile["capture_focus"]:
            negative += 0.28
        if profile["industrial_heat_focus"]:
            negative += 0.35
        if profile["power_plant_focus"]:
            negative += 0.08
        if profile["work_cycle_focus"]:
            negative += 0.12

        profile["focus_strength"] = max(0.0, min(1.0, positive - negative))
        return profile

    def _query_alignment(self, search_context: str, patent: Patent) -> Dict[str, Any]:
        query_tokens = self._query_tokens(search_context)
        if not query_tokens:
            return {
                "weighted_coverage": 1.0,
                "distinctive_total": 0,
                "distinctive_hits": 0,
                "title_distinctive_hits": 0,
            }

        body_text = self._normalize_text(" ".join([
            patent.title,
            patent.abstract,
            patent.snippet,
        ]))
        title_text = self._normalize_text(patent.title)
        if not body_text:
            return {
                "weighted_coverage": 0.0,
                "distinctive_total": sum(
                    1 for token in query_tokens if token not in self.GENERIC_QUERY_TERMS
                ),
                "distinctive_hits": 0,
                "title_distinctive_hits": 0,
            }

        total_weight = 0.0
        matched_weight = 0.0
        distinctive_total = 0
        distinctive_hits = 0
        title_distinctive_hits = 0

        for token in query_tokens:
            is_generic = token in self.GENERIC_QUERY_TERMS
            weight = 1.0 if is_generic else 2.0
            total_weight += weight

            body_hit = self._token_in_text(token, body_text)
            title_hit = self._token_in_text(token, title_text)
            if body_hit:
                matched_weight += weight
                if not is_generic:
                    distinctive_hits += 1
            if not is_generic:
                distinctive_total += 1
                if title_hit:
                    title_distinctive_hits += 1

        return {
            "weighted_coverage": matched_weight / total_weight if total_weight else 1.0,
            "distinctive_total": distinctive_total,
            "distinctive_hits": distinctive_hits,
            "title_distinctive_hits": title_distinctive_hits,
        }

    def _apply_screening_guardrails(
        self,
        evaluation: PatentEvaluation,
        patent: Patent,
        search_context: str,
    ) -> Dict[str, Any]:
        alignment = self._query_alignment(search_context, patent)
        raw_score = float(evaluation.screening_score or 0)
        coverage = alignment["weighted_coverage"]
        title_bonus = 0.2 if alignment["title_distinctive_hits"] else 0.0
        evidence_penalty = 0.5 if not (patent.abstract or patent.snippet) else 0.0
        calibrated_score = raw_score * (0.55 + (0.45 * coverage))
        calibrated_score += title_bonus
        calibrated_score -= evidence_penalty
        evaluation.screening_score = round(max(0.0, min(10.0, calibrated_score)), 1)

        reasons: List[str] = []
        if alignment["distinctive_total"] and alignment["distinctive_hits"] == 0:
            evaluation.screening_decision = "exclude" if coverage < 0.55 else "review"
            evaluation.screening_score = min(
                evaluation.screening_score,
                3.5 if evaluation.screening_decision == "exclude" else config.SCREEN_REVIEW_THRESHOLD,
            )
            reasons.append("faltam termos distintivos da query no título e no resumo")
        elif evaluation.screening_decision == "include" and coverage < 0.60:
            evaluation.screening_decision = "review"
            evaluation.screening_score = min(evaluation.screening_score, 6.0)
            reasons.append("o alinhamento textual com a query é apenas parcial")
        elif evaluation.screening_decision == "review" and coverage < 0.35:
            evaluation.screening_decision = "exclude"
            evaluation.screening_score = min(evaluation.screening_score, 3.5)
            reasons.append("o alinhamento textual com a query é baixo")

        if evaluation.screening_decision == "include" and evaluation.screening_score < config.SCREEN_INCLUDE_THRESHOLD:
            evaluation.screening_decision = (
                "review"
                if evaluation.screening_score >= config.SCREEN_REVIEW_THRESHOLD
                else "exclude"
            )
        elif evaluation.screening_decision == "review" and evaluation.screening_score < config.SCREEN_REVIEW_THRESHOLD:
            evaluation.screening_decision = "exclude"

        if reasons:
            prefix = f"{evaluation.screening_reason.strip().rstrip('.')}." if evaluation.screening_reason else ""
            evaluation.screening_reason = (
                f"{prefix} Guardrail de alinhamento: {'; '.join(reasons)}."
            ).strip()

        if evaluation.confidence:
            evaluation.confidence = round(
                max(0.0, min(1.0, evaluation.confidence * (0.7 + (0.3 * coverage)))),
                2,
            )
        return alignment

    def _apply_relevance_guardrails(
        self,
        evaluation: PatentEvaluation,
        screening: PatentEvaluation,
        patent: Patent,
        search_context: str,
    ) -> None:
        alignment = self._query_alignment(search_context, patent)
        focus = self._focus_profile(patent)
        coverage = alignment["weighted_coverage"]
        raw_score = float(evaluation.relevance_score or screening.screening_score or 0)
        blended_score = (raw_score * 0.75) + (screening.screening_score * 0.25)
        blended_score *= 0.7 + (0.3 * coverage)
        if alignment["title_distinctive_hits"]:
            blended_score += 0.2
        if focus["carbon_storage_phrase"]:
            blended_score += 0.35
        if focus["title_storage"]:
            blended_score += 0.25
        elif focus["body_storage"]:
            blended_score -= 0.05
        if focus["supercritical_focus"]:
            blended_score += 0.15
        if focus["transmission_focus"]:
            blended_score -= 0.25
        if focus["cooling_focus"]:
            blended_score -= 0.25
        if focus["power_plant_focus"]:
            blended_score -= 0.20
        if focus["work_cycle_focus"]:
            blended_score -= 0.25
        if not (patent.abstract or patent.snippet):
            blended_score -= 0.5

        if screening.screening_decision == "include":
            blended_score = min(blended_score, screening.screening_score + 1.1)
            blended_score += (focus["focus_strength"] - 0.7) * 1.8
        elif screening.screening_decision == "review":
            blended_score = min(blended_score, 6.5)
        else:
            blended_score = min(blended_score, 3.5)

        evaluation.relevance_score = round(max(0.0, min(10.0, blended_score)), 1)
        if evaluation.confidence:
            evaluation.confidence = round(
                max(
                    0.0,
                    min(
                        1.0,
                        min(evaluation.confidence, screening.confidence or evaluation.confidence)
                        * (0.8 + (0.2 * coverage)),
                    ),
                ),
                2,
            )

    def _comparative_fact_sheet(
        self,
        selected_pairs: List[Tuple[Patent, PatentEvaluation]],
        search_context: str,
    ) -> str:
        lines = []
        for patent, evaluation in selected_pairs:
            evidence = evaluation.evidence_snippets[:2]
            if not evidence and (patent.abstract or patent.snippet):
                evidence = [(patent.abstract or patent.snippet)[:220]]
            alignment = self._query_alignment(search_context, patent)
            lines.extend([
                f"### {patent.patent_id or patent.record_id}",
                f"- Papel Analítico: {self._comparative_bucket_label(patent, evaluation, search_context)}",
                f"- Triagem: {(evaluation.screening_decision or 'N/A').upper()}",
                f"- Título: {patent.title}",
                f"- Score: {evaluation.relevance_score}/10",
                f"- Cobertura da Query: {round(alignment.get('weighted_coverage', 0.0) * 100, 1)}%",
                f"- Cluster: {evaluation.thematic_cluster or 'N/A'}",
                f"- Domínio: {evaluation.technical_domain or 'N/A'}",
                f"- Papel do CO2: {evaluation.co2_role or 'N/A'}",
                f"- Papel do armazenamento: {evaluation.storage_role or 'N/A'}",
                f"- Limite sistêmico: {evaluation.system_boundary or 'N/A'}",
                f"- Tipo de ciclo: {evaluation.cycle_type or 'N/A'}",
                f"- Foco das claims: {evaluation.claim_focus or 'N/A'}",
                f"- Resumo: {(evaluation.summary or 'Resumo não disponível.')[:260]}",
                f"- Razão da Triagem: {(evaluation.screening_reason or 'N/A')[:220]}",
                f"- Evidências: {' | '.join(evidence) if evidence else 'N/A'}",
                "",
            ])
        return "\n".join(lines).strip()

    def _comparative_decision_priority(self, evaluation: PatentEvaluation) -> int:
        decision = self._normalize_text(evaluation.screening_decision)
        return {
            "include": 0,
            "review": 1,
            "exclude": 2,
        }.get(decision, 3)

    def _comparative_sorted_pairs(
        self,
        selected_pairs: List[Tuple[Patent, PatentEvaluation]],
    ) -> List[Tuple[Patent, PatentEvaluation]]:
        return sorted(
            selected_pairs,
            key=lambda item: (
                self._comparative_decision_priority(item[1]),
                -(item[1].relevance_score or 0),
                item[0].patent_id or item[0].record_id or "",
            ),
        )

    def _comparative_patent_key(self, patent: Patent, evaluation: PatentEvaluation) -> str:
        return patent.record_id or patent.patent_id or evaluation.record_id or evaluation.patent_id or ""

    def _pair_comparative_inputs(
        self,
        patents: List[Patent],
        evaluations: List[PatentEvaluation],
    ) -> List[Tuple[Patent, PatentEvaluation]]:
        eval_map: Dict[str, PatentEvaluation] = {}
        for evaluation in evaluations:
            key = evaluation.record_id or evaluation.patent_id
            if key:
                eval_map[key] = evaluation

        pairs: List[Tuple[Patent, PatentEvaluation]] = []
        for patent in patents:
            key = patent.record_id or patent.patent_id
            if not key:
                continue
            evaluation = eval_map.get(key)
            if evaluation is not None:
                pairs.append((patent, evaluation))
        return pairs

    def _is_whitespace_adjacent(
        self,
        patent: Patent,
        evaluation: PatentEvaluation,
        search_context: str,
    ) -> bool:
        if self._normalize_text(evaluation.screening_decision) != "exclude" or evaluation.llm_error:
            return False

        focus = self._focus_profile(patent)
        alignment = self._query_alignment(search_context, patent)
        boundary_signal = any([
            focus["supercritical_focus"],
            focus["underground_focus"],
            focus["transmission_focus"],
            focus["work_cycle_focus"],
            focus["cooling_focus"],
            focus["capture_focus"],
        ])
        return bool(
            (evaluation.screening_score or 0.0) >= max(4.0, config.SCREEN_REVIEW_THRESHOLD - 0.5)
            or (
                alignment.get("weighted_coverage", 0.0) >= 0.35
                and alignment.get("distinctive_hits", 0) >= 1
                and focus.get("focus_strength", 0.0) >= 0.18
                and boundary_signal
            )
        )

    def _comparative_bucket(
        self,
        patent: Patent,
        evaluation: PatentEvaluation,
        search_context: str,
    ) -> str:
        decision = self._normalize_text(evaluation.screening_decision)
        if decision == "include":
            return "core"
        if decision == "review":
            return "frontier"
        if self._is_whitespace_adjacent(patent, evaluation, search_context):
            return "adjacent"
        return ""

    def _comparative_bucket_label(
        self,
        patent: Patent,
        evaluation: PatentEvaluation,
        search_context: str,
    ) -> str:
        bucket = self._comparative_bucket(patent, evaluation, search_context)
        return {
            "core": "Nucleo direto",
            "frontier": "Fronteira tecnica",
            "adjacent": "Adjacencia exploratoria",
        }.get(bucket, "Fora do escopo comparativo")

    def _select_comparative_pairs(
        self,
        patents: List[Patent],
        evaluations: List[PatentEvaluation],
        search_context: str,
    ) -> List[Tuple[Patent, PatentEvaluation]]:
        core_pairs: List[Tuple[Patent, PatentEvaluation]] = []
        frontier_pairs: List[Tuple[Patent, PatentEvaluation]] = []
        adjacent_pairs: List[Tuple[Patent, PatentEvaluation]] = []

        for patent, evaluation in self._pair_comparative_inputs(patents, evaluations):
            if evaluation.llm_error:
                continue
            bucket = self._comparative_bucket(patent, evaluation, search_context)
            if bucket == "core":
                core_pairs.append((patent, evaluation))
            elif bucket == "frontier":
                frontier_pairs.append((patent, evaluation))
            elif bucket == "adjacent":
                adjacent_pairs.append((patent, evaluation))

        if not core_pairs and not frontier_pairs:
            return []

        ordered_adjacent = self._comparative_sorted_pairs(adjacent_pairs)
        adjacent_limit = min(config.WHITESPACE_MAX_ADJACENT, len(ordered_adjacent))
        return (
            self._comparative_sorted_pairs(core_pairs)
            + self._comparative_sorted_pairs(frontier_pairs)
            + ordered_adjacent[:adjacent_limit]
        )

    def _markdown_heading_key(self, line: str) -> str:
        stripped = line.strip()
        if not stripped.startswith("#"):
            return ""
        heading = re.sub(r"^#+\s*", "", stripped)
        heading = re.sub(r"^\d+[\.\)]?\s*", "", heading)
        return self._normalize_text(heading)

    def _has_markdown_section(self, response: str, keyword: str) -> bool:
        normalized_keyword = self._normalize_text(keyword)
        return any(
            normalized_keyword in self._markdown_heading_key(line)
            for line in response.splitlines()
        )

    def _strip_markdown_sections(
        self,
        response: str,
        keywords: List[str],
    ) -> str:
        normalized_keywords = [self._normalize_text(keyword) for keyword in keywords]
        cleaned_lines: List[str] = []
        skipping = False

        for line in response.splitlines():
            heading_key = self._markdown_heading_key(line)
            if heading_key:
                if any(keyword in heading_key for keyword in normalized_keywords):
                    skipping = True
                    continue
                if skipping:
                    skipping = False
            if not skipping:
                cleaned_lines.append(line)

        return "\n".join(cleaned_lines).strip()

    def _comparative_patent_id(self, patent: Patent) -> str:
        return patent.patent_id or patent.record_id or "N/A"

    def _comparative_ids_text(self, patent_ids: List[str]) -> str:
        usable = [patent_id for patent_id in patent_ids if patent_id]
        return ", ".join(usable) if usable else "N/A"

    def _comparative_ranking_reason(
        self,
        patent: Patent,
        evaluation: PatentEvaluation,
    ) -> str:
        focus = self._focus_profile(patent)
        reasons: List[str] = []

        if evaluation.co2_role == "stored_thermodynamic_medium":
            reasons.append("CO2 aparece como meio termodinamico armazenado")
        elif evaluation.co2_role == "working_fluid":
            reasons.append("CO2 aparece principalmente como fluido de trabalho")
        elif evaluation.co2_role == "refrigerant_loop":
            reasons.append("CO2 aparece principalmente em circuito de refrigeracao")

        if evaluation.storage_role == "explicit_thermal_storage":
            reasons.append("armazenamento termico explicito como parte central")
        elif evaluation.storage_role == "underground_thermal_storage":
            reasons.append("armazenamento termico subterraneo como componente distintivo")
        elif evaluation.storage_role == "implicit_or_support_storage":
            reasons.append("armazenamento aparece mais como subsistema de apoio")

        if focus["carbon_storage_phrase"]:
            reasons.append("armazenamento explícito de CO2 como núcleo da arquitetura")
        elif focus["supercritical_focus"] and focus["body_storage"]:
            reasons.append("armazenamento com CO2 supercrítico e integração térmica direta")

        if focus["transmission_focus"] or focus["work_cycle_focus"]:
            reasons.append("CO2 usado principalmente como fluido de trabalho para transferência térmica")
        elif focus["cooling_focus"]:
            reasons.append("ênfase em refrigeração/sub-resfriamento, mais adjacente ao núcleo da query")

        if focus["underground_focus"] and not focus["carbon_storage_phrase"]:
            reasons.append("armazenamento subterrâneo aparece como subsistema de suporte")

        if not reasons:
            reasons.append("alinhamento técnico sustentado pelas evidências extraídas")

        return "; ".join(reasons[:2])

    def _comparative_panorama_section(
        self,
        selected_pairs: List[Tuple[Patent, PatentEvaluation]],
        search_context: str,
    ) -> str:
        ranked_pairs = self._comparative_sorted_pairs(selected_pairs)
        all_ids = [self._comparative_patent_id(patent) for patent, _ in ranked_pairs]
        core_storage_ids: List[str] = []
        adjacent_ids: List[str] = []
        frontier_ids: List[str] = []
        underground_ids: List[str] = []

        for patent, evaluation in ranked_pairs:
            patent_id = self._comparative_patent_id(patent)
            focus = self._focus_profile(patent)
            bucket = self._comparative_bucket(patent, evaluation, search_context)
            if bucket == "frontier":
                frontier_ids.append(patent_id)
            elif bucket == "adjacent":
                adjacent_ids.append(patent_id)
            if focus["underground_focus"]:
                underground_ids.append(patent_id)
            if focus["carbon_storage_phrase"] or (
                focus["body_co2"] and focus["body_storage"] and focus["supercritical_focus"]
            ):
                core_storage_ids.append(patent_id)
            if (
                bucket != "adjacent"
                and (focus["transmission_focus"] or focus["work_cycle_focus"] or focus["cooling_focus"])
            ):
                adjacent_ids.append(patent_id)

        if not core_storage_ids and ranked_pairs:
            core_storage_ids = [self._comparative_patent_id(ranked_pairs[0][0])]

        if not adjacent_ids:
            adjacent_ids = [
                patent_id
                for patent_id in all_ids
                if patent_id not in core_storage_ids and patent_id not in frontier_ids
            ]

        lines = [
            "### 1. Panorama Geral",
            "",
            f"- O conjunto comparativo agrega {len(all_ids)} patente(s) e nao deve ser tratado como bloco homogeneo: ha um nucleo direto, fronteiras tecnicas em revisao e adjacencias uteis apenas para delimitar whitespace [IDs: {self._comparative_ids_text(all_ids)}]",
        ]
        if core_storage_ids:
            lines.append(
                f"- O subgrupo mais diretamente alinhado ao núcleo da query é {self._comparative_ids_text(core_storage_ids)}, com foco em armazenamento de CO2, compressão/expansão e controle termodinâmico do meio armazenado [IDs: {self._comparative_ids_text(core_storage_ids)}]"
            )
        if frontier_ids:
            lines.append(
                f"- {self._comparative_ids_text(frontier_ids)} formam a fronteira tecnica: sao casos proximos do problema, mas ainda ambiguos quanto ao papel exato do CO2 no armazenamento ou na funcao arquitetural central [IDs: {self._comparative_ids_text(frontier_ids)}]"
            )
        if adjacent_ids:
            lines.append(
                f"- {self._comparative_ids_text(adjacent_ids)} entram como adjacencia exploratoria: tratam CO2 principalmente como fluido de trabalho em transferencia termica ou distribuicao de energia, de modo que ajudam a delimitar combinacoes pouco cobertas sem virar evidencia de cobertura consolidada [IDs: {self._comparative_ids_text(adjacent_ids)}]"
            )
        if underground_ids and set(underground_ids) != set(all_ids):
            lines.append(
                f"- A mencao a armazenamento subterraneo ou subaquatico aparece apenas em {self._comparative_ids_text(underground_ids)} e nao deve ser generalizada para todo o conjunto comparativo [IDs: {self._comparative_ids_text(underground_ids)}]"
            )
        elif underground_ids:
            lines.append(
                f"- A referencia a armazenamento subterraneo ou subaquatico aparece em todo o conjunto comparativo [IDs: {self._comparative_ids_text(underground_ids)}]"
            )
        lines.append("")
        return "\n".join(lines).strip()

    def _comparative_ranking_section(
        self,
        selected_pairs: List[Tuple[Patent, PatentEvaluation]],
    ) -> str:
        ranking = self._comparative_sorted_pairs(selected_pairs)
        lines = [
            "### 5. Ranking Final",
            "",
        ]
        for position, (patent, evaluation) in enumerate(ranking, start=1):
            patent_id = self._comparative_patent_id(patent)
            lines.append(
                f"{position}. **{patent_id}** — {self._comparative_ranking_reason(patent, evaluation)}; "
                f"score {evaluation.relevance_score}/10 [IDs: {patent_id}]"
            )
        lines.append("")
        return "\n".join(lines).strip()

    def _comparative_support_appendix(
        self,
        selected_pairs: List[Tuple[Patent, PatentEvaluation]],
    ) -> str:
        cluster_map: Dict[str, List[str]] = {}
        ranking = self._comparative_sorted_pairs(selected_pairs)
        for patent, evaluation in selected_pairs:
            cluster = evaluation.thematic_cluster or evaluation.technical_domain or "General / Other"
            cluster_map.setdefault(cluster, []).append(self._comparative_patent_id(patent))

        lines = [
            "### 6. Mapa de Evidências por ID",
            "",
        ]
        for cluster, ids in sorted(cluster_map.items(), key=lambda item: (-len(item[1]), item[0])):
            lines.append(f"- **{cluster}** [IDs: {', '.join(ids)}]")
        lines.extend([
            "",
            "### 7. Ranking por ID",
            "",
        ])
        for position, (patent, evaluation) in enumerate(ranking, start=1):
            patent_id = self._comparative_patent_id(patent)
            lines.append(
                f"{position}. **{patent_id}** — score {evaluation.relevance_score}/10 "
                f"[IDs: {patent_id}]"
            )
        return "\n".join(lines)

    def _comparative_whitespace_section(
        self,
        selected_pairs: List[Tuple[Patent, PatentEvaluation]],
        search_context: str,
    ) -> str:
        core_ids: List[str] = []
        frontier_ids: List[str] = []
        adjacent_ids: List[str] = []
        transfer_ids: List[str] = []
        supercritical_ids: List[str] = []
        underground_ids: List[str] = []
        cooling_ids: List[str] = []
        capture_ids: List[str] = []

        for patent, evaluation in self._comparative_sorted_pairs(selected_pairs):
            patent_id = self._comparative_patent_id(patent)
            focus = self._focus_profile(patent)
            bucket = self._comparative_bucket(patent, evaluation, search_context)
            if bucket == "core":
                core_ids.append(patent_id)
            elif bucket == "frontier":
                frontier_ids.append(patent_id)
            elif bucket == "adjacent":
                adjacent_ids.append(patent_id)

            if focus["transmission_focus"] or focus["work_cycle_focus"]:
                transfer_ids.append(patent_id)
            if focus["supercritical_focus"]:
                supercritical_ids.append(patent_id)
            if focus["underground_focus"]:
                underground_ids.append(patent_id)
            if focus["cooling_focus"]:
                cooling_ids.append(patent_id)
            if focus["capture_focus"]:
                capture_ids.append(patent_id)

        def format_ids(*groups: List[str]) -> str:
            ordered: List[str] = []
            for group in groups:
                for patent_id in group:
                    if patent_id and patent_id not in ordered:
                        ordered.append(patent_id)
            return self._comparative_ids_text(ordered[:4])

        bullets: List[str] = []
        if core_ids and (transfer_ids or frontier_ids or adjacent_ids):
            bullets.append(
                "- O whitespace mais promissor esta na combinacao entre arquiteturas de ciclo/transferencia termica com CO2 e armazenamento explicito do inventario termico, porque esses elementos ainda aparecem fragmentados entre nucleo, fronteira e adjacencia [IDs: "
                f"{format_ids(core_ids, frontier_ids, transfer_ids, adjacent_ids)}]"
            )
        if supercritical_ids and underground_ids and not set(underground_ids).issubset(set(core_ids)):
            bullets.append(
                "- Ha espaco para reivindicacoes em armazenamento subterraneo ou subaquatico com CO2 supercritico e integracao termica mais explicita, ja que essa combinacao surge mais na borda do corpus do que como cobertura consolidada [IDs: "
                f"{format_ids(underground_ids, supercritical_ids, frontier_ids, adjacent_ids)}]"
            )
        if cooling_ids or capture_ids:
            bullets.append(
                "- Gestao termica transiente, subresfriamento e acoplamentos com captura/reatores aparecem de forma lateral; isso sugere oportunidade em claims de controle, operacao multi-regime e integracao de processo ainda pouco amarradas ao armazenamento central [IDs: "
                f"{format_ids(cooling_ids, capture_ids, frontier_ids, core_ids)}]"
            )
        if frontier_ids:
            bullets.append(
                "- As patentes em review delimitam fronteiras tecnicas onde o papel do CO2 ainda esta ambiguo entre meio armazenado, fluido de trabalho e interface de troca termica; esse tipo de ambiguidade costuma ser um bom proxy para whitespace exploravel com recorte arquitetural mais especifico [IDs: "
                f"{format_ids(frontier_ids, core_ids, adjacent_ids)}]"
            )
        if not bullets:
            bullets.append(
                "- O principal whitespace esta em recombinar subcomponentes que hoje aparecem dispersos entre o nucleo e a borda tecnica do conjunto, em vez de buscar um tema totalmente ausente [IDs: "
                f"{format_ids(core_ids, frontier_ids, adjacent_ids)}]"
            )

        lines = [
            "### 3. Whitespaces e Oportunidades",
            "",
            *bullets[:4],
            "",
        ]
        return "\n".join(lines).strip()

    def _build_whitespace_candidates(
        self,
        selected_pairs: List[Tuple[Patent, PatentEvaluation]],
        search_context: str,
    ) -> List[Dict[str, Any]]:
        ranked_pairs = self._comparative_sorted_pairs(selected_pairs)
        core_rows: List[Dict[str, Any]] = []
        frontier_rows: List[Dict[str, Any]] = []
        adjacent_rows: List[Dict[str, Any]] = []

        for patent, evaluation in ranked_pairs:
            row = {
                "patent_id": self._comparative_patent_id(patent),
                "bucket": self._comparative_bucket(patent, evaluation, search_context),
                "co2_role": evaluation.co2_role or "not_clear",
                "storage_role": evaluation.storage_role or "not_clear",
                "system_boundary": evaluation.system_boundary or "not_clear",
                "cycle_type": evaluation.cycle_type or "not_clear",
                "heat_source_sink": evaluation.heat_source_sink or "not_clear",
                "claim_focus": evaluation.claim_focus or "not_clear",
                "exclusion_category": evaluation.exclusion_category or "",
                "screening_decision": evaluation.screening_decision or "",
                "relevance_score": evaluation.relevance_score or 0.0,
            }
            if row["bucket"] == "core":
                core_rows.append(row)
            elif row["bucket"] == "frontier":
                frontier_rows.append(row)
            elif row["bucket"] == "adjacent":
                adjacent_rows.append(row)

        def ids(rows: List[Dict[str, Any]]) -> List[str]:
            return [str(row["patent_id"]) for row in rows if row.get("patent_id")]

        candidates: List[Dict[str, Any]] = []
        if core_rows and (frontier_rows or adjacent_rows):
            candidates.append({
                "opportunity": "hybrid_cycle_storage_architecture",
                "confidence": "medium",
                "rationale": (
                    "Combinar ciclos/transferencia com CO2 e armazenamento termico explicitamente "
                    "reivindicado ainda aparece fragmentado entre nucleo e borda tecnica."
                ),
                "core_ids": ids(core_rows)[:3],
                "frontier_ids": ids(frontier_rows)[:3],
                "adjacent_ids": ids(adjacent_rows)[:3],
            })

        underground_rows = [
            row for row in frontier_rows + adjacent_rows
            if row["storage_role"] == "underground_thermal_storage"
        ]
        supercritical_rows = [
            row for row in core_rows + frontier_rows + adjacent_rows
            if row["cycle_type"] == "supercritical_or_transcritical_co2"
        ]
        if underground_rows and supercritical_rows:
            candidates.append({
                "opportunity": "underground_supercritical_storage_integration",
                "confidence": "medium",
                "rationale": (
                    "Armazenamento subterraneo e regimes supercriticos aparecem proximos, "
                    "mas nao consolidados como uma mesma arquitetura reivindicada."
                ),
                "core_ids": ids(core_rows)[:3],
                "frontier_ids": ids(underground_rows)[:3],
                "adjacent_ids": ids(supercritical_rows)[:3],
            })

        control_rows = [
            row for row in frontier_rows + adjacent_rows
            if row["claim_focus"] in {"component_or_operation", "cycle_integration"}
            and row["heat_source_sink"] in {"cooling_or_refrigeration", "industrial_heat", "general_thermal_management"}
        ]
        if control_rows:
            candidates.append({
                "opportunity": "control_and_operability_claims",
                "confidence": "medium",
                "rationale": (
                    "Ha espaco para claims de controle, operacao transiente e integracao de processo "
                    "onde o papel do CO2 e do armazenamento ainda esta ambiguo."
                ),
                "core_ids": ids(core_rows)[:3],
                "frontier_ids": ids(control_rows)[:3],
                "adjacent_ids": ids(adjacent_rows)[:3],
            })

        return candidates[:4]

    def generate_whitespace_analysis(
        self,
        patents: List[Patent],
        evaluations: List[PatentEvaluation],
        search_context: str,
    ) -> Dict[str, Any]:
        """Gera uma matriz estruturada de whitespace a partir do corpus elegível."""
        selected_pairs = self._select_comparative_pairs(patents, evaluations, search_context)
        if len(selected_pairs) < 2:
            return {
                "status": "no_input",
                "query": search_context,
                "corpus_summary": {
                    "considered_patents": len(patents),
                    "selected_patents": len(selected_pairs),
                    "core": 0,
                    "frontier": 0,
                    "adjacent": 0,
                },
                "coverage_matrix": [],
                "axes": {},
                "whitespace_candidates": [],
                "markdown_summary": "",
            }

        rows: List[Dict[str, Any]] = []
        axes: Dict[str, Dict[str, Dict[str, List[str]]]] = {
            axis: {}
            for axis in (
                "co2_role",
                "storage_role",
                "system_boundary",
                "cycle_type",
                "heat_source_sink",
                "claim_focus",
                "exclusion_category",
            )
        }
        counts = {"core": 0, "frontier": 0, "adjacent": 0}

        for patent, evaluation in self._comparative_sorted_pairs(selected_pairs):
            patent_id = self._comparative_patent_id(patent)
            bucket = self._comparative_bucket(patent, evaluation, search_context)
            counts[bucket] = counts.get(bucket, 0) + 1
            row = {
                "patent_id": patent_id,
                "record_id": patent.record_id,
                "title": patent.title,
                "screening_decision": evaluation.screening_decision,
                "screening_score": evaluation.screening_score,
                "relevance_score": evaluation.relevance_score,
                "bucket": bucket,
                "technical_domain": evaluation.technical_domain,
                "thematic_cluster": evaluation.thematic_cluster,
                "co2_role": evaluation.co2_role or "not_clear",
                "storage_role": evaluation.storage_role or "not_clear",
                "system_boundary": evaluation.system_boundary or "not_clear",
                "cycle_type": evaluation.cycle_type or "not_clear",
                "heat_source_sink": evaluation.heat_source_sink or "not_clear",
                "claim_focus": evaluation.claim_focus or "not_clear",
                "exclusion_category": evaluation.exclusion_category or "",
            }
            rows.append(row)
            for axis in axes:
                value = str(row.get(axis, "") or "not_clear")
                bucket_map = axes[axis].setdefault(value, {
                    "core": [],
                    "frontier": [],
                    "adjacent": [],
                })
                bucket_map.setdefault(bucket, []).append(patent_id)

        return {
            "status": "ok",
            "query": search_context,
            "corpus_summary": {
                "considered_patents": len(patents),
                "selected_patents": len(selected_pairs),
                "core": counts.get("core", 0),
                "frontier": counts.get("frontier", 0),
                "adjacent": counts.get("adjacent", 0),
            },
            "coverage_matrix": rows,
            "axes": axes,
            "whitespace_candidates": self._build_whitespace_candidates(selected_pairs, search_context),
            "markdown_summary": self._comparative_whitespace_section(selected_pairs, search_context),
        }

    def _comparative_completion_sections(
        self,
        selected_pairs: List[Tuple[Patent, PatentEvaluation]],
        response: str,
    ) -> str:
        cluster_map: Dict[str, List[str]] = {}
        ranking = self._comparative_sorted_pairs(selected_pairs)
        for patent, evaluation in selected_pairs:
            cluster = evaluation.thematic_cluster or evaluation.technical_domain or "General / Other"
            cluster_map.setdefault(cluster, []).append(self._comparative_patent_id(patent))

        lines: List[str] = []
        if not self._has_markdown_section(response, "recomendações"):
            lines.extend([
                "### 4. Recomendações",
                "",
                f"- Priorizar arquiteturas centradas em armazenamento explícito de CO2 e controle termodinâmico rigoroso [IDs: {', '.join([pid for pid in cluster_map.get('CO2 Cycle Configurations', []) if pid]) or self._comparative_patent_id(ranking[0][0])}]",
            ])
            if cluster_map.get("Thermal Transfer Mechanisms"):
                lines.append(
                    f"- Tratar as patentes de transferência térmica como adjacentes ao núcleo do problema e validar seu papel de armazenamento com leitura humana adicional [IDs: {', '.join(cluster_map['Thermal Transfer Mechanisms'])}]"
                )
            lines.append("")

        return "\n".join(lines).strip()

    def _comparative_has_id_support(self, response: str, patent_ids: List[str]) -> bool:
        cited = {
            patent_id
            for patent_id in patent_ids
            if patent_id and patent_id in response
        }
        return "[IDs:" in response and len(cited) >= min(2, len([pid for pid in patent_ids if pid]))

    def _cache_key(
        self,
        prompt: str,
        response_format: Optional[Any],
        num_predict: int,
    ) -> str:
        payload = {
            "model": self.model,
            "base_url": self.base_url,
            "prompt": prompt,
            "response_format": response_format if response_format not in ("", "text") else None,
            "num_predict": num_predict,
            "temperature": 0.3,
            "top_p": 0.9,
        }
        encoded = json.dumps(payload, sort_keys=True, ensure_ascii=False).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()

    def _load_cache(self) -> None:
        if not self.cache_enabled:
            return
        try:
            if os.path.exists(self.cache_path):
                with open(self.cache_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if isinstance(data, dict):
                    self._response_cache = {str(k): str(v) for k, v in data.items()}
        except Exception as e:
            self._log(
                logging.WARNING,
                "llm_cache_load_failed",
                cache_path=self.cache_path,
                detail=str(e),
            )
            self._response_cache = {}

    def _save_cache(self) -> None:
        if not self.cache_enabled:
            return
        try:
            os.makedirs(self.cache_dir, exist_ok=True)
            with open(self.cache_path, "w", encoding="utf-8") as f:
                json.dump(self._response_cache, f, ensure_ascii=False, indent=2)
        except Exception as e:
            self._log(
                logging.WARNING,
                "llm_cache_save_failed",
                cache_path=self.cache_path,
                detail=str(e),
            )

    def cache_stats(self) -> Dict[str, int]:
        return {
            "hits": self.cache_hits,
            "misses": self.cache_misses,
            "entries": len(self._response_cache),
        }

    def _operation_metrics(self, operation: str) -> Dict[str, Any]:
        return self._telemetry.setdefault(operation, {
            "calls": 0,
            "successes": 0,
            "failures": 0,
            "retries": 0,
            "cache_hits": 0,
            "degraded_skips": 0,
            "prompt_chars": 0,
            "response_chars": 0,
            "total_duration_seconds": 0.0,
            "max_duration_seconds": 0.0,
        })

    def _record_call_metric(
        self,
        operation: str,
        duration_seconds: float,
        prompt_chars: int,
        response_chars: int = 0,
        success: bool = False,
        cache_hit: bool = False,
        retries: int = 0,
        degraded_skip: bool = False,
    ) -> None:
        metric = self._operation_metrics(operation)
        metric["calls"] += 1
        metric["prompt_chars"] += prompt_chars
        metric["response_chars"] += response_chars
        metric["total_duration_seconds"] += duration_seconds
        metric["max_duration_seconds"] = max(metric["max_duration_seconds"], duration_seconds)
        metric["retries"] += retries
        if success:
            metric["successes"] += 1
        else:
            metric["failures"] += 1
        if cache_hit:
            metric["cache_hits"] += 1
        if degraded_skip:
            metric["degraded_skips"] += 1

    def _push_recent_error(self, operation: str, detail: str) -> None:
        self.recent_errors.append({
            "operation": operation,
            "detail": detail,
        })
        if len(self.recent_errors) > 10:
            self.recent_errors = self.recent_errors[-10:]

    def _register_failure(self, operation: str, detail: str) -> None:
        self.total_failures += 1
        self.consecutive_failures += 1
        self._push_recent_error(operation, detail)
        if self.total_failures >= config.OLLAMA_MAX_FAILURES_BEFORE_DEGRADE:
            self.degraded = True

    def _register_success(self) -> None:
        self.consecutive_failures = 0

    def is_degraded(self) -> bool:
        return self.degraded

    def telemetry_stats(self) -> Dict[str, Any]:
        operations: Dict[str, Any] = {}
        for operation, metric in self._telemetry.items():
            calls = metric["calls"] or 1
            operations[operation] = {
                **metric,
                "total_duration_seconds": round(metric["total_duration_seconds"], 3),
                "average_duration_seconds": round(metric["total_duration_seconds"] / calls, 3),
                "max_duration_seconds": round(metric["max_duration_seconds"], 3),
            }
        return {
            "degraded": self.degraded,
            "total_failures": self.total_failures,
            "consecutive_failures": self.consecutive_failures,
            "recent_errors": list(self.recent_errors),
            "operations": operations,
        }

    def check_connection(self) -> bool:
        """Verifica se o Ollama está acessível e o modelo disponível."""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=10)
            response.raise_for_status()
            data = response.json()
            models = [m.get("name", "") for m in data.get("models", [])]

            resolved_model = self._resolve_available_model(models)
            if resolved_model and resolved_model != self.model:
                self._set_active_model(resolved_model)
                self._log(
                    logging.INFO,
                    "ollama_model_alias_resolved",
                    requested_model=self.requested_model,
                    resolved_model=resolved_model,
                    available_models=models,
                )

            if resolved_model and self._probe_model_generation():
                self._log(
                    logging.INFO,
                    "ollama_connection_ok",
                    available_models=models,
                )
                return True

            if resolved_model:
                self._log(
                    logging.WARNING,
                    "ollama_healthcheck_failed",
                    available_models=models,
                    detail=self.last_health_error or "sem detalhe",
                )
                return False

            self._log(
                logging.WARNING,
                "ollama_model_missing",
                requested_model=self.requested_model,
                available_models=models,
            )
            return False
        except Exception as e:
            self._log(
                logging.ERROR,
                "ollama_connection_error",
                detail=str(e),
            )
            return False

    def _probe_model_generation(self) -> bool:
        """Executa uma geração curta para validar o endpoint do modelo."""
        started = time.perf_counter()
        payload = {
            "model": self.model,
            "prompt": config.OLLAMA_HEALTHCHECK_PROMPT,
            "stream": False,
            "format": "json",
            "options": {
                "temperature": 0.0,
                "top_p": 1.0,
                "num_predict": 32,
            },
        }

        try:
            response = requests.post(
                self.api_url,
                json=payload,
                timeout=min(config.OLLAMA_TIMEOUT, 30),
            )
            response.raise_for_status()
            data = response.json()
            response_text = data.get("response", "").strip()
            parsed = self._parse_json_response(response_text)
            if parsed.get("status") == "ok":
                self.last_health_error = ""
                self._record_call_metric(
                    "healthcheck",
                    time.perf_counter() - started,
                    prompt_chars=len(config.OLLAMA_HEALTHCHECK_PROMPT),
                    response_chars=len(response_text),
                    success=True,
                )
                return True
            self.last_health_error = "Smoke test retornou payload inesperado."
            self._record_call_metric(
                "healthcheck",
                time.perf_counter() - started,
                prompt_chars=len(config.OLLAMA_HEALTHCHECK_PROMPT),
                response_chars=len(response_text),
                success=False,
            )
            return False
        except Exception as e:
            self.last_health_error = str(e)
            self._log(
                logging.ERROR,
                "ollama_smoke_test_error",
                detail=str(e),
            )
            self._record_call_metric(
                "healthcheck",
                time.perf_counter() - started,
                prompt_chars=len(config.OLLAMA_HEALTHCHECK_PROMPT),
                success=False,
            )
            return False

    def _call_ollama(
        self,
        prompt: str,
        response_format: Optional[Any] = "json",
        num_predict: int = 2048,
        operation: str = "generic",
    ) -> str:
        """Faz chamada ao Ollama e retorna a resposta."""
        started = time.perf_counter()
        if self.degraded:
            self.last_error = "Circuit breaker do Ollama ativo para a execução."
            self._record_call_metric(
                operation,
                time.perf_counter() - started,
                prompt_chars=len(prompt),
                success=False,
                degraded_skip=True,
            )
            return ""

        cache_key = self._cache_key(prompt, response_format, num_predict)
        if self.cache_enabled:
            cached = self._response_cache.get(cache_key)
            if cached is not None:
                self.cache_hits += 1
                self._log(
                    logging.INFO,
                    "llm_cache_hit",
                    operation=operation,
                    cache_key=cache_key,
                )
                self.last_error = ""
                self._register_success()
                self._record_call_metric(
                    operation,
                    time.perf_counter() - started,
                    prompt_chars=len(prompt),
                    response_chars=len(cached),
                    success=True,
                    cache_hit=True,
                )
                return cached
            self.cache_misses += 1

        normalized_format = None if response_format in (None, "", "text") else response_format
        base_options = {
            "temperature": 0.3,
            "top_p": 0.9,
            "num_predict": num_predict,
        }
        request_options = [base_options]

        # Geração em texto livre é mais sensível; uma segunda tentativa mais curta
        # evita forçar o modelo a produzir respostas longas quando o backend degrada.
        if normalized_format is None and num_predict > 1024:
            request_options.append({
                "temperature": 0.2,
                "top_p": 0.8,
                "num_predict": 1024,
            })

        for attempt_index, options in enumerate(request_options, start=1):
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": options,
            }
            if normalized_format is not None:
                payload["format"] = normalized_format

            try:
                response = requests.post(
                    self.api_url,
                    json=payload,
                    timeout=config.OLLAMA_TIMEOUT,
                )
                response.raise_for_status()
                data = response.json()
                response_text = data.get("response", "").strip()
                if self.cache_enabled and response_text:
                    self._response_cache[cache_key] = response_text
                    self._save_cache()
                self.last_error = ""
                self._register_success()
                self._record_call_metric(
                    operation,
                    time.perf_counter() - started,
                    prompt_chars=len(prompt),
                    response_chars=len(response_text),
                    success=True,
                    retries=attempt_index - 1,
                )
                return response_text
            except requests.exceptions.Timeout:
                self.last_error = "Timeout ao chamar Ollama."
                self._log(
                    logging.ERROR,
                    "ollama_timeout",
                    operation=operation,
                    timeout_seconds=config.OLLAMA_TIMEOUT,
                    attempt=attempt_index,
                )
                self._register_failure(operation, self.last_error)
                self._record_call_metric(
                    operation,
                    time.perf_counter() - started,
                    prompt_chars=len(prompt),
                    success=False,
                    retries=attempt_index - 1,
                )
                return ""
            except requests.exceptions.HTTPError as e:
                status_code = e.response.status_code if e.response is not None else None
                should_retry = (
                    status_code is not None
                    and status_code >= 500
                    and attempt_index < len(request_options)
                )
                if should_retry:
                    self._log(
                        logging.WARNING,
                        "ollama_http_retry",
                        operation=operation,
                        status_code=status_code,
                        attempt=attempt_index,
                    )
                    continue
                self.last_error = f"Erro HTTP ao chamar Ollama: {e}"
                self._log(
                    logging.ERROR,
                    "ollama_http_error",
                    operation=operation,
                    status_code=status_code,
                    detail=str(e),
                    attempt=attempt_index,
                )
                self._register_failure(operation, self.last_error)
                self._record_call_metric(
                    operation,
                    time.perf_counter() - started,
                    prompt_chars=len(prompt),
                    success=False,
                    retries=attempt_index - 1,
                )
                return ""
            except requests.exceptions.RequestException as e:
                self.last_error = f"Erro ao chamar Ollama: {e}"
                self._log(
                    logging.ERROR,
                    "ollama_request_error",
                    operation=operation,
                    detail=str(e),
                    attempt=attempt_index,
                )
                self._register_failure(operation, self.last_error)
                self._record_call_metric(
                    operation,
                    time.perf_counter() - started,
                    prompt_chars=len(prompt),
                    success=False,
                    retries=attempt_index - 1,
                )
                return ""
            except Exception as e:
                self.last_error = f"Erro inesperado ao chamar Ollama: {e}"
                self._log(
                    logging.ERROR,
                    "ollama_unexpected_error",
                    operation=operation,
                    detail=str(e),
                    attempt=attempt_index,
                )
                self._register_failure(operation, self.last_error)
                self._record_call_metric(
                    operation,
                    time.perf_counter() - started,
                    prompt_chars=len(prompt),
                    success=False,
                    retries=attempt_index - 1,
                )
                return ""

        return ""

    def _llm_failure_evaluation(self, patent: Patent, reason: str) -> PatentEvaluation:
        """Converte falha de infraestrutura do LLM em revisão manual, não exclusão."""
        fallback_evidence = patent.abstract or patent.snippet or patent.title
        evaluation = PatentEvaluation(
            record_id=patent.record_id,
            patent_id=patent.patent_id,
            screening_score=0.0,
            screening_decision="review",
            screening_reason="Falha do LLM; revisão manual necessária.",
            confidence=0.0,
            manual_review_required=True,
            llm_error=reason,
        )
        if fallback_evidence:
            evaluation.evidence_snippets = [fallback_evidence[:240]]
        return evaluation

    def _parse_json_response(self, response_text: str) -> Dict[str, Any]:
        """Extrai um objeto JSON da resposta do modelo."""
        try:
            data = json.loads(response_text)
            if isinstance(data, dict):
                return data
        except json.JSONDecodeError:
            pass

        json_match = re.search(r"\{.*\}", response_text, re.DOTALL)
        if json_match:
            try:
                data = json.loads(json_match.group())
                if isinstance(data, dict):
                    return data
            except json.JSONDecodeError:
                self._log(
                    logging.WARNING,
                    "llm_json_extract_failed",
                    response_preview=response_text[:240],
                )

        return {}

    def _normalize_string_list(self, value: Any) -> List[str]:
        """Normaliza um campo para lista de strings."""
        if not value:
            return []
        if isinstance(value, list):
            return [str(item).strip() for item in value if str(item).strip()]
        if isinstance(value, str):
            return [item.strip() for item in re.split(r"[;\n]", value) if item.strip()]
        return [str(value).strip()]

    def _normalize_short_text(self, value: Any, max_chars: int = 120) -> str:
        text = str(value or "").strip()
        if not text:
            return ""
        return text[:max_chars]

    def _canonical_category(
        self,
        value: str,
        rules: List[Tuple[str, List[str]]],
        default: str = "",
    ) -> str:
        normalized = self._normalize_text(value)
        if not normalized:
            return default
        for label, patterns in rules:
            if normalized == label:
                return label
            if any(pattern in normalized for pattern in patterns):
                return label
        return default or self._normalize_short_text(value)

    def _canonical_co2_role(self, value: str) -> str:
        return self._canonical_category(
            value,
            [
                ("stored_thermodynamic_medium", ["stored", "armazenado", "medium", "meio armazen", "co2 supercrit", "thermodynamic medium"]),
                ("working_fluid", ["working fluid", "fluido de trabalho", "transfer loop", "transfer", "ciclo de trabalho"]),
                ("refrigerant_loop", ["refrigerant", "refriger", "subresfri", "subcool", "transcritical"]),
                ("capture_process_stream", ["capture", "captura", "adsorption", "absorption", "sorbent"]),
                ("co2_present_unclear_role", ["unclear", "ambiguous", "nao claro", "presente"]),
                ("co2_not_central", ["not central", "nao central", "ausente", "indireto"]),
            ],
        )

    def _canonical_storage_role(self, value: str) -> str:
        return self._canonical_category(
            value,
            [
                ("underground_thermal_storage", ["underground", "subterr", "underwater", "subsurface"]),
                ("explicit_thermal_storage", ["explicit", "thermal storage", "armazenamento term", "storage vessel", "storage system"]),
                ("implicit_or_support_storage", ["implicit", "support", "bypass", "subsystem", "apoio"]),
                ("storage_not_explicit", ["not explicit", "nao explicito", "storage absent"]),
            ],
        )

    def _canonical_system_boundary(self, value: str) -> str:
        return self._canonical_category(
            value,
            [
                ("dedicated_storage_system", ["dedicated", "storage system", "sistema dedicado", "arquitetura dedicada"]),
                ("cycle_or_transfer_subsystem", ["cycle", "transfer", "subsystem", "circuit", "loop"]),
                ("process_integration", ["process", "integra", "planta", "processo"]),
                ("industrial_heat_process", ["industrial heat", "calcination", "steam generation", "industrial"]),
                ("unclear_boundary", ["unclear", "nao claro", "ambiguous"]),
            ],
        )

    def _canonical_cycle_type(self, value: str) -> str:
        return self._canonical_category(
            value,
            [
                ("supercritical_or_transcritical_co2", ["supercritical", "transcritical", "isothermal and isobaric"]),
                ("refrigeration_cycle", ["refriger", "subcool", "cooling"]),
                ("power_or_work_cycle", ["work cycle", "power cycle", "producing work", "expansion"]),
                ("not_clear", ["not clear", "nao claro", "unclear"]),
            ],
        )

    def _canonical_heat_source_sink(self, value: str) -> str:
        return self._canonical_category(
            value,
            [
                ("industrial_heat", ["industrial", "calcination", "steam", "electrolysis"]),
                ("cooling_or_refrigeration", ["cooling", "refriger", "subcool"]),
                ("power_generation", ["power", "steam turbine", "generation"]),
                ("general_thermal_management", ["thermal", "heat", "energy storage", "heat exchanger"]),
                ("not_clear", ["not clear", "nao claro", "unclear"]),
            ],
        )

    def _canonical_claim_focus(self, value: str) -> str:
        return self._canonical_category(
            value,
            [
                ("system_architecture", ["system", "architecture", "sistema", "armazenamento", "storage architecture"]),
                ("cycle_integration", ["cycle", "ciclo", "transfer", "fluido de trabalho", "working fluid"]),
                ("process_integration", ["process", "processo", "captura", "industrial", "calcination", "integration"]),
                ("component_or_operation", ["component", "operation", "operacao", "control", "subcool", "valve"]),
            ],
        )

    def _canonical_exclusion_category(self, value: str) -> str:
        return self._canonical_category(
            value,
            [
                ("generic_tes", ["generic", "thermal energy storage", "tes gener"]),
                ("co2_working_fluid_only", ["working fluid", "fluido de trabalho"]),
                ("cooling_only", ["cooling", "refriger"]),
                ("capture_process", ["capture", "captura", "adsorption", "absorption"]),
                ("industrial_heat_adjacent", ["industrial", "calcination"]),
                ("low_alignment", ["low alignment", "baixo alinhamento"]),
                ("boundary_case", ["boundary", "limítrofe", "limite"]),
            ],
        )

    def _infer_exclusion_category(
        self,
        patent: Patent,
        evaluation: PatentEvaluation,
        search_context: str,
    ) -> str:
        focus = self._focus_profile(patent)
        alignment = self._query_alignment(search_context, patent)
        if evaluation.screening_decision != "exclude" and alignment["weighted_coverage"] >= 0.45:
            return ""
        if focus["capture_focus"]:
            return "capture_process"
        if focus["cooling_focus"]:
            return "cooling_only"
        if focus["industrial_heat_focus"]:
            return "industrial_heat_adjacent"
        if focus["transmission_focus"] or focus["work_cycle_focus"]:
            return "co2_working_fluid_only"
        if focus["body_storage"] and not focus["body_co2"]:
            return "generic_tes"
        if alignment["weighted_coverage"] < 0.35:
            return "low_alignment"
        return "boundary_case"

    def _backfill_structural_roles(
        self,
        evaluation: PatentEvaluation,
        patent: Patent,
        search_context: str,
    ) -> None:
        focus = self._focus_profile(patent)
        alignment = self._query_alignment(search_context, patent)

        if not evaluation.co2_role:
            if focus["capture_focus"]:
                evaluation.co2_role = "capture_process_stream"
            elif focus["carbon_storage_phrase"] or (
                focus["body_co2"] and focus["body_storage"] and focus["supercritical_focus"]
            ):
                evaluation.co2_role = "stored_thermodynamic_medium"
            elif focus["transmission_focus"] or focus["work_cycle_focus"]:
                evaluation.co2_role = "working_fluid"
            elif focus["cooling_focus"]:
                evaluation.co2_role = "refrigerant_loop"
            elif focus["body_co2"]:
                evaluation.co2_role = "co2_present_unclear_role"
            else:
                evaluation.co2_role = "co2_not_central"

        if not evaluation.storage_role:
            if focus["underground_focus"] and focus["body_storage"]:
                evaluation.storage_role = "underground_thermal_storage"
            elif focus["thermal_storage_phrase"] or focus["body_storage"]:
                evaluation.storage_role = "explicit_thermal_storage"
            elif focus["transmission_focus"] or focus["work_cycle_focus"]:
                evaluation.storage_role = "implicit_or_support_storage"
            else:
                evaluation.storage_role = "storage_not_explicit"

        if not evaluation.system_boundary:
            if focus["capture_focus"]:
                evaluation.system_boundary = "process_integration"
            elif focus["industrial_heat_focus"]:
                evaluation.system_boundary = "industrial_heat_process"
            elif focus["transmission_focus"] or focus["work_cycle_focus"]:
                evaluation.system_boundary = "cycle_or_transfer_subsystem"
            elif focus["body_storage"]:
                evaluation.system_boundary = "dedicated_storage_system"
            else:
                evaluation.system_boundary = "unclear_boundary"

        if not evaluation.cycle_type:
            if focus["supercritical_focus"]:
                evaluation.cycle_type = "supercritical_or_transcritical_co2"
            elif focus["cooling_focus"]:
                evaluation.cycle_type = "refrigeration_cycle"
            elif focus["work_cycle_focus"]:
                evaluation.cycle_type = "power_or_work_cycle"
            else:
                evaluation.cycle_type = "not_clear"

        if not evaluation.heat_source_sink:
            if focus["industrial_heat_focus"]:
                evaluation.heat_source_sink = "industrial_heat"
            elif focus["cooling_focus"]:
                evaluation.heat_source_sink = "cooling_or_refrigeration"
            elif focus["power_plant_focus"]:
                evaluation.heat_source_sink = "power_generation"
            elif alignment["weighted_coverage"] >= 0.5:
                evaluation.heat_source_sink = "general_thermal_management"
            else:
                evaluation.heat_source_sink = "not_clear"

        if not evaluation.claim_focus:
            if focus["body_storage"] and focus["body_co2"]:
                evaluation.claim_focus = "system_architecture"
            elif focus["transmission_focus"] or focus["work_cycle_focus"]:
                evaluation.claim_focus = "cycle_integration"
            elif focus["capture_focus"] or focus["industrial_heat_focus"]:
                evaluation.claim_focus = "process_integration"
            else:
                evaluation.claim_focus = "component_or_operation"

        if not evaluation.exclusion_category:
            evaluation.exclusion_category = self._infer_exclusion_category(
                patent,
                evaluation,
                search_context,
            )

    def _apply_structural_fields(
        self,
        evaluation: PatentEvaluation,
        data: Dict[str, Any],
        patent: Patent,
        search_context: str,
        enable_thematic_clusters: bool = True,
        enable_structural_roles: bool = True,
    ) -> None:
        evaluation.technical_domain = self._normalize_short_text(data.get("technical_domain", ""))
        evaluation.thematic_cluster = (
            self._normalize_short_text(data.get("thematic_cluster", ""))
            if enable_thematic_clusters
            else ""
        )
        if not enable_structural_roles:
            evaluation.co2_role = ""
            evaluation.storage_role = ""
            evaluation.system_boundary = ""
            evaluation.cycle_type = ""
            evaluation.heat_source_sink = ""
            evaluation.claim_focus = ""
            evaluation.exclusion_category = ""
            return
        evaluation.co2_role = self._canonical_co2_role(str(data.get("co2_role", "")))
        evaluation.storage_role = self._canonical_storage_role(str(data.get("storage_role", "")))
        evaluation.system_boundary = self._canonical_system_boundary(str(data.get("system_boundary", "")))
        evaluation.cycle_type = self._canonical_cycle_type(str(data.get("cycle_type", "")))
        evaluation.heat_source_sink = self._canonical_heat_source_sink(str(data.get("heat_source_sink", "")))
        evaluation.claim_focus = self._canonical_claim_focus(str(data.get("claim_focus", "")))
        evaluation.exclusion_category = self._canonical_exclusion_category(str(data.get("exclusion_category", "")))
        self._backfill_structural_roles(evaluation, patent, search_context)

    def _should_rerank_screening(self, evaluation: PatentEvaluation) -> bool:
        if evaluation.llm_error:
            return False
        score = float(evaluation.screening_score or 0.0)
        if evaluation.screening_decision == "review":
            return True
        if config.SCREEN_RERANK_MIN_SCORE <= score <= config.SCREEN_RERANK_MAX_SCORE:
            return True
        if evaluation.screening_decision == "include" and (evaluation.confidence or 0.0) < 0.7:
            return True
        return False

    def screen_patent(
        self,
        patent: Patent,
        search_context: str,
        require_evidence: bool = True,
        enable_thematic_clusters: bool = True,
        enable_structural_roles: bool = True,
        enable_screening_rerank: bool = True,
    ) -> PatentEvaluation:
        """Executa a triagem rápida da patente."""
        prompt = self._build_screening_prompt(
            patent,
            search_context,
            require_evidence=require_evidence,
            enable_thematic_clusters=enable_thematic_clusters,
            enable_structural_roles=enable_structural_roles,
        )
        response_text = self._call_ollama(prompt, operation="screening")
        evaluation = PatentEvaluation(record_id=patent.record_id, patent_id=patent.patent_id)

        if not response_text:
            self._log(
                logging.WARNING,
                "screening_empty_response",
                patent_id=patent.patent_id,
                record_id=patent.record_id,
            )
            return self._llm_failure_evaluation(
                patent,
                self.last_error or "Sem resposta do modelo.",
            )

        data = self._parse_json_response(response_text)
        if not data:
            self._log(
                logging.WARNING,
                "screening_invalid_response",
                patent_id=patent.patent_id,
                record_id=patent.record_id,
                response_preview=response_text[:240],
            )
            return self._llm_failure_evaluation(
                patent,
                "Resposta inválida ou não estruturada do modelo na triagem.",
            )
        try:
            evaluation.screening_score = float(data.get("screening_score", 0) or 0)
            evaluation.screening_decision = str(data.get("decision", "")).strip().lower()
            evaluation.screening_reason = data.get("screening_reason", "")
            evaluation.evidence_snippets = self._normalize_string_list(
                data.get("evidence_snippets", [])
            )
            evaluation.confidence = float(data.get("confidence", 0) or 0)
        except (TypeError, ValueError) as e:
            self._log(
                logging.WARNING,
                "screening_parse_error",
                patent_id=patent.patent_id,
                record_id=patent.record_id,
                detail=str(e),
            )
            return self._llm_failure_evaluation(
                patent,
                "Resposta inválida do modelo na triagem.",
            )

        if require_evidence and not evaluation.evidence_snippets:
            fallback_evidence = patent.abstract or patent.snippet or patent.title
            if fallback_evidence:
                evaluation.evidence_snippets = [fallback_evidence[:240]]

        if not enable_thematic_clusters:
            evaluation.thematic_cluster = ""

        if not evaluation.screening_decision:
            if evaluation.screening_score >= config.SCREEN_INCLUDE_THRESHOLD:
                evaluation.screening_decision = "include"
            elif evaluation.screening_score >= config.SCREEN_REVIEW_THRESHOLD:
                evaluation.screening_decision = "review"
            else:
                evaluation.screening_decision = "exclude"

        if evaluation.screening_decision not in {"include", "review", "exclude"}:
            return self._llm_failure_evaluation(
                patent,
                f"Decisão inválida retornada pelo modelo: {evaluation.screening_decision}",
            )

        self._apply_structural_fields(
            evaluation,
            data,
            patent,
            search_context,
            enable_thematic_clusters=enable_thematic_clusters,
            enable_structural_roles=enable_structural_roles,
        )
        self._apply_screening_guardrails(evaluation, patent, search_context)
        if enable_screening_rerank and self._should_rerank_screening(evaluation):
            reranked = self.rerank_screening_patent(
                patent,
                search_context,
                evaluation,
                require_evidence=require_evidence,
                enable_thematic_clusters=enable_thematic_clusters,
                enable_structural_roles=enable_structural_roles,
            )
            if reranked is not None:
                evaluation = reranked
        evaluation.manual_review_required = evaluation.screening_decision == "review"
        return evaluation

    def evaluate_patent(
        self,
        patent: Patent,
        search_context: str,
        screening: Optional[PatentEvaluation] = None,
        require_evidence: bool = True,
        enable_thematic_clusters: bool = True,
        enable_structural_roles: bool = True,
        enable_screening_rerank: bool = True,
    ) -> PatentEvaluation:
        """Executa a extração estruturada da patente."""
        if screening is None:
            screening = self.screen_patent(
                patent,
                search_context,
                require_evidence=require_evidence,
                enable_thematic_clusters=enable_thematic_clusters,
                enable_structural_roles=enable_structural_roles,
                enable_screening_rerank=enable_screening_rerank,
            )

        if screening.screening_decision == "exclude":
            return screening

        if screening.llm_error:
            return screening

        prompt = self._build_evaluation_prompt(
            patent,
            search_context,
            screening,
            require_evidence=require_evidence,
            enable_thematic_clusters=enable_thematic_clusters,
            enable_structural_roles=enable_structural_roles,
        )
        response_text = self._call_ollama(prompt, operation="evaluation")

        if not response_text:
            self._log(
                logging.WARNING,
                "evaluation_empty_response",
                patent_id=patent.patent_id,
                record_id=patent.record_id,
            )
            screening.summary = screening.screening_reason or "Sem resposta do modelo."
            screening.llm_error = screening.llm_error or self.last_error or "Sem resposta do modelo."
            return screening

        evaluation = self._parse_detailed_response(
            response_text,
            patent.patent_id,
            patent.record_id,
        )
        evaluation.screening_score = screening.screening_score
        evaluation.screening_decision = screening.screening_decision
        evaluation.screening_reason = screening.screening_reason
        evaluation.llm_error = screening.llm_error
        evaluation.evidence_snippets = screening.evidence_snippets or evaluation.evidence_snippets
        if require_evidence and not evaluation.evidence_snippets:
            fallback_evidence = patent.abstract or patent.snippet or patent.title
            if fallback_evidence:
                evaluation.evidence_snippets = [fallback_evidence[:240]]
        self._apply_structural_fields(
            evaluation,
            evaluation.to_dict(),
            patent,
            search_context,
            enable_thematic_clusters=enable_thematic_clusters,
            enable_structural_roles=enable_structural_roles,
        )
        if enable_thematic_clusters:
            evaluation.thematic_cluster = evaluation.thematic_cluster or screening.thematic_cluster
        else:
            evaluation.thematic_cluster = ""
        if enable_structural_roles:
            evaluation.co2_role = evaluation.co2_role or screening.co2_role
            evaluation.storage_role = evaluation.storage_role or screening.storage_role
            evaluation.system_boundary = evaluation.system_boundary or screening.system_boundary
            evaluation.cycle_type = evaluation.cycle_type or screening.cycle_type
            evaluation.heat_source_sink = evaluation.heat_source_sink or screening.heat_source_sink
            evaluation.claim_focus = evaluation.claim_focus or screening.claim_focus
            evaluation.exclusion_category = evaluation.exclusion_category or screening.exclusion_category
        else:
            evaluation.co2_role = ""
            evaluation.storage_role = ""
            evaluation.system_boundary = ""
            evaluation.cycle_type = ""
            evaluation.heat_source_sink = ""
            evaluation.claim_focus = ""
            evaluation.exclusion_category = ""
        evaluation.rerank_applied = screening.rerank_applied if enable_screening_rerank else False
        evaluation.rerank_reason = screening.rerank_reason if enable_screening_rerank else ""
        evaluation.manual_review_required = screening.manual_review_required
        self._apply_relevance_guardrails(evaluation, screening, patent, search_context)
        return evaluation

    def _build_screening_prompt(
        self,
        patent: Patent,
        search_context: str,
        require_evidence: bool = True,
        enable_thematic_clusters: bool = True,
        enable_structural_roles: bool = True,
    ) -> str:
        """Constrói o prompt para triagem rápida."""
        abstract_text = patent.abstract or patent.snippet or "Não disponível"
        inventors_text = ", ".join(patent.inventors) if patent.inventors else "Não informado"
        evidence_instruction = (
            "Forneça pelo menos 1 trecho textual concreto como evidência."
            if require_evidence
            else "Evidência textual é opcional; priorize a decisão."
        )
        cluster_note = (
            '"thematic_cluster": "<cluster temático resumido>",'
            if enable_thematic_clusters
            else '"thematic_cluster": "",'
        )
        structural_block = ""
        if enable_structural_roles:
            structural_block = (
                '    "co2_role": "<stored_thermodynamic_medium|working_fluid|refrigerant_loop|capture_process_stream|co2_present_unclear_role|co2_not_central>",\n'
                '    "storage_role": "<explicit_thermal_storage|underground_thermal_storage|implicit_or_support_storage|storage_not_explicit>",\n'
                '    "system_boundary": "<dedicated_storage_system|cycle_or_transfer_subsystem|process_integration|industrial_heat_process|unclear_boundary>",\n'
                '    "cycle_type": "<supercritical_or_transcritical_co2|refrigeration_cycle|power_or_work_cycle|not_clear>",\n'
                '    "heat_source_sink": "<industrial_heat|cooling_or_refrigeration|power_generation|general_thermal_management|not_clear>",\n'
                '    "claim_focus": "<system_architecture|cycle_integration|process_integration|component_or_operation>",\n'
                '    "exclusion_category": "<generic_tes|co2_working_fluid_only|cooling_only|capture_process|industrial_heat_adjacent|low_alignment|boundary_case|>",\n'
            )

        return f"""Você é um pesquisador sênior de patentes executando uma triagem inicial.

## Contexto da Busca
O usuário está pesquisando sobre: "{search_context}"

## Dados da Patente
- **Título:** {patent.title}
- **ID:** {patent.patent_id}
- **Inventores:** {inventors_text}
- **Titular:** {patent.assignee or "Não informado"}
- **Data de Publicação:** {patent.publication_date or patent.filing_date or "Não informada"}
- **Resumo/Abstract:** {abstract_text}

## Instruções
Classifique a patente em uma destas decisões:
- include: claramente relevante
- review: possivelmente relevante, mas precisa de leitura humana
- exclude: fora de escopo

Use um padrão rigoroso:
- só use include quando a patente aderir aos termos distintivos da busca, não apenas a termos genéricos como "energy", "thermal", "storage", "system" ou "method"
- se houver alinhamento apenas parcial com a query, prefira review
- use toda a escala de score; não concentre tudo em notas 9-10
- patentes de armazenamento térmico genérico sem o elemento técnico central da query devem ser review ou exclude

{evidence_instruction}

{{
    "screening_score": <número de 0 a 10>,
    "decision": "<include|review|exclude>",
    "screening_reason": "<justificativa curta em português>",
    "technical_domain": "<domínio técnico principal>",
    {cluster_note}
{structural_block}    "evidence_snippets": ["<trecho 1>", "<trecho 2>"],
    "confidence": <número entre 0 e 1>
}}

	Responda APENAS com o JSON, sem texto adicional."""

    def _build_rerank_prompt(
        self,
        patent: Patent,
        search_context: str,
        screening: PatentEvaluation,
        require_evidence: bool = True,
        enable_thematic_clusters: bool = True,
        enable_structural_roles: bool = True,
    ) -> str:
        """Constrói o prompt para reranking dos casos limítrofes."""
        abstract_text = patent.abstract or patent.snippet or "Não disponível"
        evidence_instruction = (
            "Mantenha ao menos 1 evidência textual curta que sustente a decisão final."
            if require_evidence
            else "Evidência textual é opcional."
        )
        cluster_note = (
            '"thematic_cluster": "<cluster temático resumido>",'
            if enable_thematic_clusters
            else '"thematic_cluster": "",'
        )
        structural_context = ""
        structural_block = ""
        if enable_structural_roles:
            structural_context = (
                f'- **Papel do CO2:** {screening.co2_role or "N/A"}\n'
                f'- **Papel do armazenamento:** {screening.storage_role or "N/A"}\n'
                f'- **Limite do sistema:** {screening.system_boundary or "N/A"}\n'
                f'- **Tipo de ciclo:** {screening.cycle_type or "N/A"}\n'
                f'- **Foco das claims:** {screening.claim_focus or "N/A"}\n'
            )
            structural_block = (
                '    "co2_role": "<stored_thermodynamic_medium|working_fluid|refrigerant_loop|capture_process_stream|co2_present_unclear_role|co2_not_central>",\n'
                '    "storage_role": "<explicit_thermal_storage|underground_thermal_storage|implicit_or_support_storage|storage_not_explicit>",\n'
                '    "system_boundary": "<dedicated_storage_system|cycle_or_transfer_subsystem|process_integration|industrial_heat_process|unclear_boundary>",\n'
                '    "cycle_type": "<supercritical_or_transcritical_co2|refrigeration_cycle|power_or_work_cycle|not_clear>",\n'
                '    "heat_source_sink": "<industrial_heat|cooling_or_refrigeration|power_generation|general_thermal_management|not_clear>",\n'
                '    "claim_focus": "<system_architecture|cycle_integration|process_integration|component_or_operation>",\n'
                '    "exclusion_category": "<generic_tes|co2_working_fluid_only|cooling_only|capture_process|industrial_heat_adjacent|low_alignment|boundary_case|>",\n'
            )
        return f"""Você está fazendo um segundo passe de triagem para um caso limítrofe em busca de patentes.

## Contexto da Busca
"{search_context}"

## Patente
- **Título:** {patent.title}
- **ID:** {patent.patent_id}
- **Resumo:** {abstract_text}

## Primeira Triagem
- **Score:** {screening.screening_score}
- **Decisão:** {screening.screening_decision}
- **Justificativa:** {screening.screening_reason}
{structural_context}

## Instruções
Reavalie o caso com rigor máximo.
- `include` apenas se o CO2 e o armazenamento forem centrais à arquitetura reivindicada
- `review` se existir proximidade técnica real, mas ainda houver ambiguidade sobre o papel central do CO2, do armazenamento ou do limite sistêmico
- `exclude` se a patente for apenas adjacente, genérica ou focada em refrigeração, transferência, captura ou processo industrial sem o núcleo da query
- prefira `review` em vez de `include` quando houver qualquer dúvida estrutural
- use categorias explícitas de papel técnico, não descrições vagas

{evidence_instruction}

{{
    "screening_score": <número de 0 a 10>,
    "decision": "<include|review|exclude>",
    "screening_reason": "<justificativa final curta>",
    "technical_domain": "<domínio técnico principal>",
    {cluster_note}
{structural_block}    "evidence_snippets": ["<trecho 1>", "<trecho 2>"],
    "confidence": <número entre 0 e 1>
}}

Responda APENAS com o JSON."""

    def rerank_screening_patent(
        self,
        patent: Patent,
        search_context: str,
        screening: PatentEvaluation,
        require_evidence: bool = True,
        enable_thematic_clusters: bool = True,
        enable_structural_roles: bool = True,
    ) -> Optional[PatentEvaluation]:
        """Executa reranking para casos limítrofes sem descartar a triagem inicial."""
        prompt = self._build_rerank_prompt(
            patent,
            search_context,
            screening,
            require_evidence=require_evidence,
            enable_thematic_clusters=enable_thematic_clusters,
            enable_structural_roles=enable_structural_roles,
        )
        response_text = self._call_ollama(
            prompt,
            operation="rerank",
        )
        if not response_text:
            return None

        data = self._parse_json_response(response_text)
        if not data:
            return None

        reranked = PatentEvaluation(**screening.to_dict())
        try:
            reranked.screening_score = float(data.get("screening_score", screening.screening_score) or screening.screening_score)
            reranked.screening_decision = str(
                data.get("decision", screening.screening_decision)
            ).strip().lower() or screening.screening_decision
            reranked.screening_reason = self._normalize_short_text(
                data.get("screening_reason", screening.screening_reason),
                max_chars=220,
            ) or screening.screening_reason
            reranked.evidence_snippets = self._normalize_string_list(
                data.get("evidence_snippets", screening.evidence_snippets)
            ) or screening.evidence_snippets
            reranked.confidence = float(data.get("confidence", screening.confidence) or screening.confidence)
        except (TypeError, ValueError):
            return None

        if reranked.screening_decision not in {"include", "review", "exclude"}:
            return None

        self._apply_structural_fields(
            reranked,
            data,
            patent,
            search_context,
            enable_thematic_clusters=enable_thematic_clusters,
            enable_structural_roles=enable_structural_roles,
        )
        self._apply_screening_guardrails(reranked, patent, search_context)
        reranked.rerank_applied = True
        if reranked.screening_decision != screening.screening_decision:
            reranked.rerank_reason = (
                f"reranked:{screening.screening_decision}->{reranked.screening_decision}"
            )
        else:
            reranked.rerank_reason = "reranked:decision_confirmed"
        reranked.manual_review_required = reranked.screening_decision == "review"
        return reranked

    def _build_evaluation_prompt(
        self,
        patent: Patent,
        search_context: str,
        screening: PatentEvaluation,
        require_evidence: bool = True,
        enable_thematic_clusters: bool = True,
        enable_structural_roles: bool = True,
    ) -> str:
        """Constrói o prompt para extração estruturada da patente."""
        abstract_text = patent.abstract or patent.snippet or "Não disponível"
        inventors_text = ", ".join(patent.inventors) if patent.inventors else "Não informado"
        evidence_instruction = (
            "Inclua pelo menos 2 trechos de evidência textual concreta. Se não houver conteúdo suficiente, retorne o trecho mais informativo disponível do abstract ou do snippet."
            if require_evidence
            else "Evidência textual é opcional; foque na extração estruturada."
        )
        cluster_note = (
            '"thematic_cluster": "<cluster temático resumido>",'
            if enable_thematic_clusters
            else '"thematic_cluster": "",'
        )
        structural_context = ""
        structural_block = ""
        if enable_structural_roles:
            structural_context = (
                f'- **Papel do CO2:** {screening.co2_role or "Não informado"}\n'
                f'- **Papel do armazenamento:** {screening.storage_role or "Não informado"}\n'
                f'- **Limite do sistema:** {screening.system_boundary or "Não informado"}\n'
                f'- **Tipo de ciclo:** {screening.cycle_type or "Não informado"}\n'
            )
            structural_block = (
                '    "co2_role": "<papel técnico principal do CO2>",\n'
                '    "storage_role": "<papel do armazenamento no sistema>",\n'
                '    "system_boundary": "<limite sistêmico reivindicado>",\n'
                '    "cycle_type": "<tipo de ciclo ou regime termodinâmico>",\n'
                '    "heat_source_sink": "<fonte/sumidouro térmico principal>",\n'
                '    "claim_focus": "<foco principal das claims>",\n'
                '    "exclusion_category": "<categoria de exclusão se o caso for adjacente; senão vazio>",\n'
            )

        return f"""Você é um especialista em análise de patentes e extração estruturada para revisão sistemática.

## Contexto da Busca
O usuário está pesquisando sobre: "{search_context}"

## Triagem Inicial
- **Decisão:** {screening.screening_decision}
- **Score de triagem:** {screening.screening_score}
- **Justificativa:** {screening.screening_reason}
- **Domínio estimado:** {screening.technical_domain or "Não informado"}
{structural_context}

## Dados da Patente
- **Título:** {patent.title}
- **ID:** {patent.patent_id}
- **Inventores:** {inventors_text}
- **Titular:** {patent.assignee or "Não informado"}
- **Data de Publicação:** {patent.publication_date or patent.filing_date or "Não informada"}
- **Resumo/Abstract:** {abstract_text}

## Instruções
Extraia o conteúdo em formato JSON EXATO:

{evidence_instruction}

Calibre o relevance_score com rigor:
- 9-10 apenas para aderência técnica forte e específica à query
- 7-8.5 para aderência boa porém parcial
- 4.5-6.5 para casos limítrofes
- abaixo de 4.5 para baixa aderência
- não trate documentos genéricos do domínio como altamente relevantes só porque compartilham termos amplos

{{
    "relevance_score": <número de 0 a 10>,
    "summary": "<resumo técnico em 2-3 frases em português>",
    "problem_statement": "<problema técnico abordado>",
    "solution_summary": "<como a patente resolve o problema>",
    "key_findings": ["<achado 1>", "<achado 2>", "<achado 3>"],
    "claimed_advantages": ["<vantagem 1>", "<vantagem 2>"],
    "limitations": ["<limitação 1>", "<limitação 2>"],
    "potential_applications": ["<aplicação 1>", "<aplicação 2>"],
    "technical_domain": "<domínio técnico principal>",
    {cluster_note}
{structural_block}    "innovation_level": "<Incremental|Significativa|Disruptiva>",
    "maturity_level": "<Inicial|Intermediária|Madura>",
    "evidence_snippets": ["<trecho de evidência 1>", "<trecho de evidência 2>"],
    "confidence": <número entre 0 e 1>
}}

Responda APENAS com o JSON, sem texto adicional."""

    def _parse_detailed_response(
        self,
        response_text: str,
        patent_id: str,
        record_id: str = "",
    ) -> PatentEvaluation:
        """Parseia a resposta detalhada do LLM."""
        evaluation = PatentEvaluation(record_id=record_id, patent_id=patent_id)
        data = self._parse_json_response(response_text)

        if data:
            try:
                evaluation.relevance_score = float(data.get("relevance_score", 0) or 0)
                evaluation.summary = data.get("summary", "")
                evaluation.problem_statement = data.get("problem_statement", "")
                evaluation.solution_summary = data.get("solution_summary", "")
                evaluation.key_findings = self._normalize_string_list(
                    data.get("key_findings", [])
                )
                evaluation.claimed_advantages = self._normalize_string_list(
                    data.get("claimed_advantages", [])
                )
                evaluation.limitations = self._normalize_string_list(
                    data.get("limitations", [])
                )
                evaluation.potential_applications = self._normalize_string_list(
                    data.get("potential_applications", [])
                )
                evaluation.innovation_level = data.get("innovation_level", "")
                evaluation.maturity_level = data.get("maturity_level", "")
                evaluation.co2_role = self._normalize_short_text(data.get("co2_role", ""))
                evaluation.storage_role = self._normalize_short_text(data.get("storage_role", ""))
                evaluation.system_boundary = self._normalize_short_text(data.get("system_boundary", ""))
                evaluation.cycle_type = self._normalize_short_text(data.get("cycle_type", ""))
                evaluation.heat_source_sink = self._normalize_short_text(data.get("heat_source_sink", ""))
                evaluation.claim_focus = self._normalize_short_text(data.get("claim_focus", ""))
                evaluation.exclusion_category = self._normalize_short_text(data.get("exclusion_category", ""))
                evaluation.technical_domain = self._normalize_short_text(data.get("technical_domain", ""))
                evaluation.thematic_cluster = self._normalize_short_text(data.get("thematic_cluster", ""))
                evaluation.evidence_snippets = self._normalize_string_list(
                    data.get("evidence_snippets", [])
                )
                evaluation.confidence = float(data.get("confidence", 0) or 0)
                if not evaluation.evidence_snippets:
                    evaluation.evidence_snippets = [response_text[:240]]
                return evaluation
            except (ValueError, TypeError) as e:
                self._log(
                    logging.WARNING,
                    "evaluation_parse_error",
                    patent_id=patent_id,
                    record_id=record_id,
                    detail=str(e),
                )

        self._log(
            logging.INFO,
            "evaluation_raw_fallback_used",
            patent_id=patent_id,
            record_id=record_id,
        )
        evaluation.summary = response_text[:500]
        evaluation.relevance_score = 5.0
        return evaluation

    def generate_comparative_analysis(
        self,
        patents: List[Patent],
        evaluations: List[PatentEvaluation],
        search_context: str,
    ) -> str:
        """Gera análise comparativa de todas as patentes encontradas."""
        selected_pairs = self._select_comparative_pairs(patents, evaluations, search_context)
        if len(selected_pairs) < 2:
            return COMPARATIVE_ANALYSIS_NO_INPUT

        patent_ids = [patent.patent_id or patent.record_id for patent, _ in selected_pairs]
        patents_text = self._comparative_fact_sheet(selected_pairs, search_context)

        prompt = f"""Você é um especialista em análise de patentes. Com base nas patentes avaliadas abaixo, forneça uma análise comparativa.

## Contexto da Busca
"{search_context}"

## Patentes Elegíveis
{patents_text}

## Instruções
Forneça uma análise comparativa em Markdown com as seguintes seções:

1. **Panorama Geral** — Visão geral do estado da arte distinguindo núcleo direto, fronteiras técnicas e adjacências exploratórias
2. **Tendências Identificadas** — Principais tendências tecnológicas observadas
3. **Whitespaces e Oportunidades** — Combinações técnicas pouco cobertas, distinguindo o que é lacuna real versus apenas adjacência
4. **Recomendações** — Sugestões para quem está pesquisando neste domínio
5. **Ranking Final** — Ranking das patentes por relevância com justificativa

Regras obrigatórias:
- use apenas as patentes listadas e apenas estes IDs: {", ".join(patent_ids)}
- em cada bullet das seções 2, 3, 4 e em cada item da seção 5, termine com o formato exato `[IDs: ID1, ID2]`
- no Panorama Geral, cite explicitamente os IDs discutidos no parágrafo
- diferencie explicitamente o que é núcleo direto, fronteira técnica e adjacência exploratória
- patentes em review servem como fronteira técnica; não trate essas patentes como estado da arte consolidado sem ressalvas
- patentes excluídas adjacentes podem delimitar whitespace, mas não podem ser usadas para afirmar cobertura consolidada
- não atribua uma característica a todas as patentes se ela aparecer apenas em um subconjunto
- quando houver heterogeneidade, diga qual subconjunto sustenta cada afirmação e cite os IDs correspondentes
- não invente tendências sem suporte textual nas patentes listadas

Escreva em português e seja conciso mas informativo."""

        response = self._call_ollama(
            prompt,
            response_format=None,
            num_predict=1536,
            operation="comparative",
        )
        if not response:
            return COMPARATIVE_ANALYSIS_FALLBACK

        response = response.strip()
        response = self._strip_markdown_sections(
            response,
            [
                "panorama geral",
                "whitespaces e oportunidades",
                "lacunas e oportunidades",
                "recomendações",
                "recomendacoes",
                "ranking final",
            ],
        )
        panorama = self._comparative_panorama_section(selected_pairs, search_context)
        whitespace = self._comparative_whitespace_section(selected_pairs, search_context)
        ranking = self._comparative_ranking_section(selected_pairs)
        completion = self._comparative_completion_sections(selected_pairs, response)
        appendix = self._comparative_support_appendix(selected_pairs)
        response = "\n\n".join(
            block for block in [panorama, response, whitespace, completion, ranking] if block
        ).strip()
        if completion:
            response = response.strip()
        if not self._comparative_has_id_support(response, patent_ids):
            return f"{response}\n\n{appendix}".strip()
        return f"{response}\n\n{appendix}".strip()
