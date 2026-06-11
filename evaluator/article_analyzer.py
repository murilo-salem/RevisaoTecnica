"""
Analisa artigos científicos usando LLM forte (27B) para extrair
claims e strings de busca de patentes.
"""

import logging
import time
from typing import List, Optional

import config
from evaluator.llm_evaluator import OllamaEvaluator
from logging_utils import log_event
from models.article import ArticleAnalysis, TargetClaim

logger = logging.getLogger(__name__)

_ANALYSIS_PROMPT = """\
Você é um especialista em análise de patentes e propriedade intelectual.
Analise o artigo científico e a descrição de inovação abaixo.

ARTIGO:
{article_text}

DESCRIÇÃO DA INOVAÇÃO:
{innovation_description}

Sua tarefa:
1. Identifique as reivindicações técnicas centrais da inovação (máx. 8 reivindicações)
2. Gere de 3 a {max_queries} strings de busca de patentes em inglês, cobrindo ângulos técnicos distintos
3. Identifique as dimensões técnicas principais para análise de whitespace
4. Sintetize a hipótese de novidade

Responda APENAS em JSON válido, sem texto adicional antes ou depois:
{{
  "article_title": "título extraído do artigo ou deduzido do contexto",
  "core_innovation": "descrição em 2-3 frases da inovação central",
  "novelty_hypothesis": "o que torna esta inovação potencialmente nova em relação ao estado da arte",
  "claims": [
    {{"id": 1, "text": "descrição técnica precisa da reivindicação", "type": "method", "is_independent": true}},
    {{"id": 2, "text": "...", "type": "system", "is_independent": false}}
  ],
  "search_queries": ["query1 em inglês", "query2 em inglês"],
  "technical_dimensions": ["dimensão técnica 1", "dimensão técnica 2"]
}}

Tipos válidos para claims: "method", "system", "composition", "use"
"""

_INNOVATION_PROMPT = """\
Você é um especialista em análise de patentes e propriedade intelectual.
Com base na descrição de inovação abaixo, identifique as reivindicações técnicas centrais.

DESCRIÇÃO DA INOVAÇÃO:
{innovation_description}

Sua tarefa:
1. Identifique as reivindicações técnicas centrais (máx. 8 reivindicações)
2. Identifique as dimensões técnicas principais para análise de whitespace
3. Sintetize a hipótese de novidade

Responda APENAS em JSON válido, sem texto adicional antes ou depois:
{{
  "article_title": "nome ou título deduzido da inovação",
  "core_innovation": "descrição em 2-3 frases da inovação central",
  "novelty_hypothesis": "o que torna esta inovação potencialmente nova em relação ao estado da arte",
  "claims": [
    {{"id": 1, "text": "descrição técnica precisa da reivindicação", "type": "method", "is_independent": true}},
    {{"id": 2, "text": "...", "type": "system", "is_independent": false}}
  ],
  "search_queries": [],
  "technical_dimensions": ["dimensão técnica 1", "dimensão técnica 2"]
}}

Tipos válidos para claims: "method", "system", "composition", "use"
"""

_VALID_CLAIM_TYPES = {"method", "system", "composition", "use"}


class ArticleAnalyzer:
    """Usa o LLM forte (27B) para extrair claims e queries de busca de um artigo."""

    def __init__(self, model: str = None):
        self._model = model or config.OLLAMA_MODEL
        self._evaluator = OllamaEvaluator(model=self._model)

    def check_connection(self) -> bool:
        return self._evaluator.check_connection()

    def analyze(
        self,
        article_text: str,
        innovation_description: str,
        max_queries: int = 4,
    ) -> Optional[ArticleAnalysis]:
        truncated = article_text[: config.ARTICLE_TEXT_MAX_CHARS]
        prompt = _ANALYSIS_PROMPT.format(
            article_text=truncated,
            innovation_description=innovation_description,
            max_queries=max_queries,
        )
        started = time.perf_counter()
        response_text = self._evaluator._call_ollama(
            prompt,
            response_format="json",
            num_predict=3000,
            operation="article_analysis",
        )
        duration = round(time.perf_counter() - started, 2)

        if not response_text:
            log_event(
                logger,
                logging.WARNING,
                "article_analysis_failed",
                reason="LLM returned empty",
                duration=duration,
            )
            return None

        data = self._evaluator._parse_json_response(response_text)
        if not data:
            log_event(
                logger,
                logging.WARNING,
                "article_analysis_parse_failed",
                preview=response_text[:200],
                duration=duration,
            )
            return None

        claims: List[TargetClaim] = []
        for raw in data.get("claims", []):
            if not isinstance(raw, dict):
                continue
            try:
                claim_type = str(raw.get("type", "method")).lower()
                if claim_type not in _VALID_CLAIM_TYPES:
                    claim_type = "method"
                claims.append(
                    TargetClaim(
                        id=int(raw.get("id", len(claims) + 1)),
                        text=str(raw.get("text", "")).strip(),
                        type=claim_type,
                        is_independent=bool(raw.get("is_independent", True)),
                    )
                )
            except (ValueError, TypeError):
                continue

        queries = [
            q
            for q in data.get("search_queries", [])
            if q and isinstance(q, str)
        ][:max_queries]

        dimensions = [
            d for d in data.get("technical_dimensions", []) if d and isinstance(d, str)
        ]

        analysis = ArticleAnalysis(
            article_title=str(data.get("article_title", "")).strip() or "Sem título",
            core_innovation=str(data.get("core_innovation", "")).strip(),
            novelty_hypothesis=str(data.get("novelty_hypothesis", "")).strip(),
            claims=claims,
            search_queries=queries,
            technical_dimensions=dimensions,
        )
        log_event(
            logger,
            logging.INFO,
            "article_analysis_completed",
            article_title=analysis.article_title,
            claims_count=len(claims),
            queries_count=len(queries),
            duration=duration,
        )
        return analysis

    def analyze_innovation(
        self,
        innovation_description: str,
        max_queries: int = 4,
    ) -> Optional[ArticleAnalysis]:
        """Gera claims a partir apenas da descrição da inovação (sem artigo)."""
        prompt = _INNOVATION_PROMPT.format(
            innovation_description=innovation_description[: config.ARTICLE_TEXT_MAX_CHARS],
        )
        started = time.perf_counter()
        response_text = self._evaluator._call_ollama(
            prompt,
            response_format="json",
            num_predict=2000,
            operation="innovation_analysis",
        )
        duration = round(time.perf_counter() - started, 2)

        if not response_text:
            log_event(
                logger, logging.WARNING, "innovation_analysis_failed",
                reason="LLM returned empty", duration=duration,
            )
            return None

        data = self._evaluator._parse_json_response(response_text)
        if not data:
            log_event(
                logger, logging.WARNING, "innovation_analysis_parse_failed",
                preview=response_text[:200], duration=duration,
            )
            return None

        claims: List[TargetClaim] = []
        for raw in data.get("claims", []):
            if not isinstance(raw, dict):
                continue
            try:
                claim_type = str(raw.get("type", "method")).lower()
                if claim_type not in _VALID_CLAIM_TYPES:
                    claim_type = "method"
                claims.append(
                    TargetClaim(
                        id=int(raw.get("id", len(claims) + 1)),
                        text=str(raw.get("text", "")).strip(),
                        type=claim_type,
                        is_independent=bool(raw.get("is_independent", True)),
                    )
                )
            except (ValueError, TypeError):
                continue

        dimensions = [
            d for d in data.get("technical_dimensions", []) if d and isinstance(d, str)
        ]

        analysis = ArticleAnalysis(
            article_title=str(data.get("article_title", "")).strip() or "Inovação",
            core_innovation=str(data.get("core_innovation", "")).strip(),
            novelty_hypothesis=str(data.get("novelty_hypothesis", "")).strip(),
            claims=claims,
            search_queries=[],
            technical_dimensions=dimensions,
        )
        log_event(
            logger, logging.INFO, "innovation_analysis_completed",
            article_title=analysis.article_title,
            claims_count=len(claims),
            duration=duration,
        )
        return analysis
