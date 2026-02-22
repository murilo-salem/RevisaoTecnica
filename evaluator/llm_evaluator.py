"""
Avaliador de patentes usando Ollama LLM.

Integra com o Ollama (modelo gemma3:4b) para avaliar relevância,
gerar resumos e análises de patentes encontradas.
"""

import json
import logging
import re
from typing import List, Optional

import requests

import config
from models.patent import Patent, PatentEvaluation

logger = logging.getLogger(__name__)


class OllamaEvaluator:
    """Avaliador de patentes usando Ollama com gemma3:4b."""

    def __init__(self, model: str = None, base_url: str = None):
        self.model = model or config.OLLAMA_MODEL
        self.base_url = base_url or config.OLLAMA_BASE_URL
        self.api_url = f"{self.base_url}/api/generate"

    def check_connection(self) -> bool:
        """Verifica se o Ollama está acessível e o modelo disponível."""
        try:
            response = requests.get(
                f"{self.base_url}/api/tags",
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()
            models = [m.get("name", "") for m in data.get("models", [])]

            # Verifica se o modelo está disponível (com ou sem tag :latest)
            model_available = any(
                self.model in m or m.startswith(self.model.split(":")[0])
                for m in models
            )

            if model_available:
                logger.info(f"Ollama conectado. Modelo '{self.model}' disponível.")
                return True
            else:
                logger.warning(
                    f"Modelo '{self.model}' não encontrado. "
                    f"Modelos disponíveis: {models}"
                )
                return False
        except Exception as e:
            logger.error(f"Erro ao conectar com Ollama: {e}")
            return False

    def _call_ollama(self, prompt: str) -> str:
        """Faz chamada ao Ollama e retorna a resposta."""
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.3,
                "top_p": 0.9,
                "num_predict": 2048,
            },
        }

        try:
            response = requests.post(
                self.api_url,
                json=payload,
                timeout=config.OLLAMA_TIMEOUT,
            )
            response.raise_for_status()
            data = response.json()
            return data.get("response", "").strip()
        except requests.exceptions.Timeout:
            logger.error("Timeout ao chamar Ollama. Aumente OLLAMA_TIMEOUT se necessário.")
            return ""
        except Exception as e:
            logger.error(f"Erro ao chamar Ollama: {e}")
            return ""

    def evaluate_patent(
        self, patent: Patent, search_context: str
    ) -> PatentEvaluation:
        """
        Avalia uma patente usando o LLM.

        Args:
            patent: Patente a ser avaliada.
            search_context: Contexto original da busca.

        Returns:
            PatentEvaluation com análise detalhada.
        """
        prompt = self._build_evaluation_prompt(patent, search_context)
        response_text = self._call_ollama(prompt)

        if not response_text:
            logger.warning(f"Resposta vazia do LLM para patente {patent.patent_id}")
            return PatentEvaluation(patent_id=patent.patent_id)

        evaluation = self._parse_evaluation_response(response_text, patent.patent_id)
        return evaluation

    def _build_evaluation_prompt(self, patent: Patent, search_context: str) -> str:
        """Constrói o prompt para avaliação da patente."""
        abstract_text = patent.abstract or patent.snippet or "Não disponível"
        inventors_text = ", ".join(patent.inventors) if patent.inventors else "Não informado"

        return f"""Você é um especialista em análise de patentes. Analise a patente abaixo e forneça uma avaliação estruturada.

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
Forneça sua análise EXATAMENTE no formato JSON abaixo (sem texto adicional fora do JSON):

{{
    "relevance_score": <número de 0 a 10, onde 10 é extremamente relevante>,
    "summary": "<resumo técnico da patente em 2-3 frases em português>",
    "key_findings": ["<achado 1>", "<achado 2>", "<achado 3>"],
    "potential_applications": ["<aplicação 1>", "<aplicação 2>"],
    "technical_domain": "<domínio técnico principal>",
    "innovation_level": "<Incremental|Significativa|Disruptiva>"
}}

Responda APENAS com o JSON, sem texto adicional."""

    def _parse_evaluation_response(
        self, response_text: str, patent_id: str
    ) -> PatentEvaluation:
        """Parseia a resposta do LLM em um objeto PatentEvaluation."""
        evaluation = PatentEvaluation(patent_id=patent_id)

        # Tenta extrair JSON da resposta
        json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', response_text, re.DOTALL)

        if json_match:
            try:
                data = json.loads(json_match.group())
                evaluation.relevance_score = float(data.get("relevance_score", 0))
                evaluation.summary = data.get("summary", "")
                evaluation.key_findings = data.get("key_findings", [])
                evaluation.potential_applications = data.get(
                    "potential_applications", []
                )
                evaluation.technical_domain = data.get("technical_domain", "")
                evaluation.innovation_level = data.get("innovation_level", "")
                return evaluation
            except (json.JSONDecodeError, ValueError) as e:
                logger.warning(f"Erro ao parsear JSON da avaliação: {e}")

        # Fallback: usa o texto completo como resumo
        logger.info("Usando resposta raw do LLM como resumo.")
        evaluation.summary = response_text[:500]
        evaluation.relevance_score = 5.0  # Score neutro
        return evaluation

    def generate_comparative_analysis(
        self,
        patents: List[Patent],
        evaluations: List[PatentEvaluation],
        search_context: str,
    ) -> str:
        """
        Gera análise comparativa de todas as patentes encontradas.

        Args:
            patents: Lista de patentes.
            evaluations: Lista de avaliações correspondentes.
            search_context: Contexto da busca original.

        Returns:
            Texto da análise comparativa em Markdown.
        """
        patents_summary = []
        for patent, evaluation in zip(patents, evaluations):
            patents_summary.append(
                f"- **{patent.title}** (ID: {patent.patent_id})\n"
                f"  Score: {evaluation.relevance_score}/10 | "
                f"Inovação: {evaluation.innovation_level}\n"
                f"  Resumo: {evaluation.summary}"
            )

        patents_text = "\n".join(patents_summary)

        prompt = f"""Você é um especialista em análise de patentes. Com base nas patentes avaliadas abaixo, forneça uma análise comparativa.

## Contexto da Busca
"{search_context}"

## Patentes Avaliadas
{patents_text}

## Instruções
Forneça uma análise comparativa em Markdown com as seguintes seções:

1. **Panorama Geral** — Visão geral do estado da arte baseado nas patentes encontradas
2. **Tendências Identificadas** — Principais tendências tecnológicas observadas
3. **Lacunas e Oportunidades** — Áreas não cobertas ou oportunidades de inovação
4. **Recomendações** — Sugestões para quem está pesquisando neste domínio
5. **Ranking Final** — Ranking das patentes por relevância com justificativa

Escreva em português e seja conciso mas informativo."""

        response = self._call_ollama(prompt)
        if not response:
            return "⚠️ Não foi possível gerar a análise comparativa."

        return response
