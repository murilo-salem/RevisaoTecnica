"""
Protocolo metodologico da revisão.
"""

from typing import Dict, List

import config


def build_review_protocol(query: str, max_results: int, model: str) -> Dict[str, object]:
    """Monta o protocolo versionado da execução."""
    return {
        "version": config.REVIEW_PROTOCOL_VERSION,
        "query": query,
        "sources": [
            "Google Patents",
            "Patentscope",
        ],
        "stages": [
            "identification",
            "deduplication",
            "screening",
            "manual_review",
            "full_extraction",
            "synthesis",
        ],
        "criteria": {
            "include": [
                "Alinhamento claro com a query ou seus sinônimos técnicos.",
                "Documento com título, resumo ou snippet suficientes para análise.",
                "Potencial técnico relevante para o domínio pesquisado.",
            ],
            "exclude": [
                "Documentos sem relação técnica com a query.",
                "Duplicatas de outra fonte ou publicação equivalente.",
                "Registro sem metadados mínimos para avaliação.",
            ],
        },
        "thresholds": {
            "include_score": config.SCREEN_INCLUDE_THRESHOLD,
            "review_score": config.SCREEN_REVIEW_THRESHOLD,
            "max_items_for_manual_review": config.SCREEN_MAX_ITEMS_FOR_REVIEW,
        },
        "limits": {
            "max_results": max_results,
        },
        "model": model,
    }

