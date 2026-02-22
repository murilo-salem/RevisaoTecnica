"""
Gerador de relatórios de análise de patentes.

Gera relatórios em Markdown e JSON com os resultados
da busca e avaliação de patentes.
"""

import json
import logging
import os
from datetime import datetime
from typing import List, Tuple

import config
from models.patent import Patent, PatentEvaluation

logger = logging.getLogger(__name__)


class ReportGenerator:
    """Gerador de relatórios de análise de patentes."""

    def __init__(self, output_dir: str = None):
        self.output_dir = output_dir or config.OUTPUT_DIR
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_report(
        self,
        query: str,
        patents: List[Patent],
        evaluations: List[PatentEvaluation],
        comparative_analysis: str = "",
    ) -> Tuple[str, str]:
        """
        Gera relatórios completos em Markdown e JSON.

        Args:
            query: Query de busca original.
            patents: Lista de patentes encontradas.
            evaluations: Lista de avaliações das patentes.
            comparative_analysis: Análise comparativa gerada pelo LLM.

        Returns:
            Tuple com (caminho_markdown, caminho_json).
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_query = "".join(c if c.isalnum() or c in " -_" else "" for c in query)
        safe_query = safe_query.replace(" ", "_")[:50]

        md_path = os.path.join(
            self.output_dir, f"patentes_{safe_query}_{timestamp}.md"
        )
        json_path = os.path.join(
            self.output_dir, f"patentes_{safe_query}_{timestamp}.json"
        )

        # Gera Markdown
        md_content = self._generate_markdown(
            query, patents, evaluations, comparative_analysis
        )
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(md_content)

        # Gera JSON
        json_content = self._generate_json(
            query, patents, evaluations, comparative_analysis
        )
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(json_content, f, ensure_ascii=False, indent=2)

        logger.info(f"Relatório Markdown salvo em: {md_path}")
        logger.info(f"Relatório JSON salvo em: {json_path}")

        return md_path, json_path

    def _generate_markdown(
        self,
        query: str,
        patents: List[Patent],
        evaluations: List[PatentEvaluation],
        comparative_analysis: str,
    ) -> str:
        """Gera relatório em formato Markdown."""
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        lines = [
            f"# 📋 Relatório de Análise de Patentes",
            f"",
            f"**Data:** {timestamp}",
            f"**Busca:** `{query}`",
            f"**Total de patentes encontradas:** {len(patents)}",
            f"**Modelo de avaliação:** {config.OLLAMA_MODEL}",
            f"",
            f"---",
            f"",
            f"## 📊 Resumo Executivo",
            f"",
        ]

        # Tabela resumo
        if patents and evaluations:
            # Ordena por relevância
            paired = list(zip(patents, evaluations))
            paired.sort(key=lambda x: x[1].relevance_score, reverse=True)

            avg_score = sum(e.relevance_score for e in evaluations) / len(evaluations)
            lines.append(f"**Score médio de relevância:** {avg_score:.1f}/10\n")

            lines.extend([
                f"| # | Patente | Score | Inovação | Domínio |",
                f"|---|---------|-------|----------|---------|",
            ])

            for i, (patent, evaluation) in enumerate(paired, 1):
                score_emoji = "🟢" if evaluation.relevance_score >= 7 else (
                    "🟡" if evaluation.relevance_score >= 4 else "🔴"
                )
                lines.append(
                    f"| {i} | [{patent.patent_id}]({patent.url}) — "
                    f"{patent.title[:60]}{'...' if len(patent.title) > 60 else ''} | "
                    f"{score_emoji} {evaluation.relevance_score:.1f} | "
                    f"{evaluation.innovation_level or 'N/A'} | "
                    f"{evaluation.technical_domain or 'N/A'} |"
                )

            lines.append("")
            lines.append("---")
            lines.append("")

        # Detalhes de cada patente
        lines.extend([
            f"## 🔍 Análise Detalhada das Patentes",
            f"",
        ])

        eval_map = {e.patent_id: e for e in evaluations}

        for i, patent in enumerate(patents, 1):
            evaluation = eval_map.get(patent.patent_id, PatentEvaluation())
            inventors_str = ", ".join(patent.inventors) if patent.inventors else "N/A"

            lines.extend([
                f"### {i}. {patent.title}",
                f"",
                f"| Campo | Valor |",
                f"|-------|-------|",
                f"| **ID** | `{patent.patent_id}` |",
                f"| **Inventores** | {inventors_str} |",
                f"| **Titular** | {patent.assignee or 'N/A'} |",
                f"| **Data** | {patent.publication_date or patent.filing_date or 'N/A'} |",
                f"| **Fonte** | {patent.source} |",
                f"| **URL** | [{patent.patent_id}]({patent.url}) |",
                f"| **Score de Relevância** | {evaluation.relevance_score:.1f}/10 |",
                f"| **Nível de Inovação** | {evaluation.innovation_level or 'N/A'} |",
                f"",
            ])

            # Abstract
            if patent.abstract or patent.snippet:
                lines.extend([
                    f"**Abstract:**",
                    f"> {patent.abstract or patent.snippet}",
                    f"",
                ])

            # Avaliação do LLM
            if evaluation.summary:
                lines.extend([
                    f"**Avaliação do LLM:**",
                    f"{evaluation.summary}",
                    f"",
                ])

            if evaluation.key_findings:
                lines.append("**Achados-chave:**")
                for finding in evaluation.key_findings:
                    lines.append(f"- {finding}")
                lines.append("")

            if evaluation.potential_applications:
                lines.append("**Aplicações potenciais:**")
                for app in evaluation.potential_applications:
                    lines.append(f"- {app}")
                lines.append("")

            lines.extend(["---", ""])

        # Análise comparativa
        if comparative_analysis:
            lines.extend([
                f"## 🔬 Análise Comparativa",
                f"",
                comparative_analysis,
                f"",
                f"---",
                f"",
            ])

        # Rodapé
        lines.extend([
            f"## ℹ️ Informações do Sistema",
            f"",
            f"- **Gerado por:** Agente de Web Scraping de Patentes",
            f"- **Modelo LLM:** {config.OLLAMA_MODEL}",
            f"- **Data de geração:** {timestamp}",
            f"- **Query de busca:** `{query}`",
        ])

        return "\n".join(lines)

    def _generate_json(
        self,
        query: str,
        patents: List[Patent],
        evaluations: List[PatentEvaluation],
        comparative_analysis: str,
    ) -> dict:
        """Gera relatório em formato JSON."""
        eval_map = {e.patent_id: e for e in evaluations}

        results = []
        for patent in patents:
            evaluation = eval_map.get(patent.patent_id, PatentEvaluation())
            results.append({
                "patent": patent.to_dict(),
                "evaluation": evaluation.to_dict(),
            })

        # Ordena por relevância
        results.sort(
            key=lambda x: x["evaluation"]["relevance_score"],
            reverse=True,
        )

        return {
            "metadata": {
                "query": query,
                "timestamp": datetime.now().isoformat(),
                "total_patents": len(patents),
                "model": config.OLLAMA_MODEL,
                "average_relevance": (
                    sum(e.relevance_score for e in evaluations) / len(evaluations)
                    if evaluations
                    else 0
                ),
            },
            "results": results,
            "comparative_analysis": comparative_analysis,
        }
