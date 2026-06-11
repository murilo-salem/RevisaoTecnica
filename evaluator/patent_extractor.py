"""
Extrai pontos técnicos de patentes em relação às reivindicações de um artigo alvo.
Usa LLM médio (12B) para velocidade.
"""

import logging
import time
from typing import List

import config
from evaluator.llm_evaluator import OllamaEvaluator
from logging_utils import log_event
from models.article import PatentExtraction, TargetClaim
from models.patent import Patent

logger = logging.getLogger(__name__)

_EXTRACTION_PROMPT = """\
Analise esta patente em relação às reivindicações de uma inovação alvo.

PATENTE:
Título: {title}
Abstract: {abstract}

REIVINDICAÇÕES DO ARTIGO ALVO:
{claims_text}

Para cada reivindicação do artigo alvo, avalie se esta patente a cobre total ou parcialmente.

Responda APENAS em JSON válido, sem texto adicional:
{{
  "core_contribution": "contribuição principal desta patente em 1-2 frases",
  "covers_claims": [1, 3],
  "partial_coverage": [{{"claim_id": 2, "aspect": "aspecto coberto parcialmente"}}],
  "similarity": "medium",
  "distinguishing_factors": "o que diferencia esta patente do artigo alvo"
}}

Valores válidos para similarity: "high", "medium", "low"
Se a patente não cobre nenhuma reivindicação: covers_claims=[] e partial_coverage=[]
"""

_VALID_SIMILARITIES = {"high", "medium", "low"}


class PatentExtractor:
    """Usa o LLM médio (12B) para extrair pontos de cada patente em relação ao artigo alvo."""

    def __init__(self, model: str = None):
        self._model = model or config.OLLAMA_EXTRACTION_MODEL
        self._evaluator = OllamaEvaluator(model=self._model)

    def extract(self, patent: Patent, claims: List[TargetClaim]) -> PatentExtraction:
        abstract_text = (patent.abstract or patent.snippet or "Abstract não disponível.")[:2000]
        claims_text = "\n".join(f"{c.id}. [{c.type}] {c.text}" for c in claims)

        prompt = _EXTRACTION_PROMPT.format(
            title=patent.title or "Sem título",
            abstract=abstract_text,
            claims_text=claims_text,
        )
        started = time.perf_counter()
        response_text = self._evaluator._call_ollama(
            prompt,
            response_format="json",
            num_predict=1024,
            operation="patent_extraction",
        )
        duration = round(time.perf_counter() - started, 2)

        fallback = PatentExtraction(
            record_id=patent.record_id,
            patent_id=patent.patent_id or patent.record_id,
            core_contribution="Extração não disponível.",
        )

        if not response_text:
            return fallback

        data = self._evaluator._parse_json_response(response_text)
        if not data:
            return fallback

        covers: List[int] = []
        for item in data.get("covers_claims", []):
            try:
                covers.append(int(item))
            except (ValueError, TypeError):
                pass

        partial: List[dict] = []
        for item in data.get("partial_coverage", []):
            if isinstance(item, dict) and "claim_id" in item:
                try:
                    partial.append(
                        {
                            "claim_id": int(item["claim_id"]),
                            "aspect": str(item.get("aspect", "")).strip(),
                        }
                    )
                except (ValueError, TypeError):
                    pass

        similarity = str(data.get("similarity", "low")).lower()
        if similarity not in _VALID_SIMILARITIES:
            similarity = "low"

        extraction = PatentExtraction(
            record_id=patent.record_id,
            patent_id=patent.patent_id or patent.record_id,
            core_contribution=str(data.get("core_contribution", "")).strip(),
            covers_claims=covers,
            partial_coverage=partial,
            similarity=similarity,
            distinguishing_factors=str(data.get("distinguishing_factors", "")).strip(),
        )
        log_event(
            logger,
            logging.DEBUG,
            "patent_extraction_completed",
            patent_id=extraction.patent_id,
            covers=covers,
            similarity=similarity,
            duration=duration,
        )
        return extraction
