"""
Helpers compartilhados para análise comparativa e fallback de relatório.
"""

COMPARATIVE_ANALYSIS_FALLBACK = "⚠️ Não foi possível gerar a análise comparativa."
COMPARATIVE_ANALYSIS_NO_INPUT = (
    "⚠️ Nenhuma patente elegível para síntese comparativa e whitespace após a triagem."
)


def has_substantive_comparative_analysis(text: str) -> bool:
    """Indica se a síntese comparativa contém conteúdo útil e não apenas avisos."""
    cleaned = (text or "").strip()
    return bool(cleaned) and not cleaned.startswith("⚠️")
