"""
Classe base abstrata para scrapers de patentes.
"""

from abc import ABC, abstractmethod
import logging
import re
from typing import Any, Dict, List

from logging_utils import log_event

from models.patent import Patent


class BaseScraper(ABC):
    """Interface base para scrapers de patentes."""

    BLOCK_PATTERNS = (
        "captcha",
        "verify you are human",
        "unusual traffic",
        "access denied",
        "human verification",
        "security check",
        "temporarily blocked",
        "request blocked",
    )

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__module__)
        self.scraper_name = self.__class__.__name__.replace("Scraper", "")
        self.diagnostics: List[Dict[str, str]] = []

    def _add_diagnostic(self, kind: str, detail: str, url: str = "") -> None:
        self.diagnostics.append({
            "kind": kind,
            "detail": detail,
            "url": url,
        })
        self._log(
            logging.WARNING,
            "scraper_diagnostic",
            kind=kind,
            detail=detail,
            url=url,
        )

    def _log(self, level: int, event: str, **fields: Any) -> None:
        """Emite log estruturado com contexto do scraper."""
        log_event(
            self.logger,
            level,
            event,
            scraper=self.scraper_name,
            **fields,
        )

    def get_diagnostics(self) -> List[Dict[str, str]]:
        return list(self.diagnostics)

    def reset_diagnostics(self) -> None:
        self.diagnostics.clear()

    def _contains_block_signal(self, text: str) -> bool:
        lowered = re.sub(r"\s+", " ", (text or "").lower())
        return any(pattern in lowered for pattern in self.BLOCK_PATTERNS)

    @abstractmethod
    def search(self, query: str, max_results: int = 10) -> List[Patent]:
        """
        Busca patentes com base na query fornecida.

        Args:
            query: String de busca.
            max_results: Número máximo de resultados.

        Returns:
            Lista de objetos Patent encontrados.
        """
        raise NotImplementedError

    @abstractmethod
    def get_patent_details(self, patent_url: str) -> Patent:
        """
        Obtém detalhes completos de uma patente específica.

        Args:
            patent_url: URL da patente.

        Returns:
            Objeto Patent com detalhes completos.
        """
        raise NotImplementedError
