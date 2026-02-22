"""
Classe base abstrata para scrapers de patentes.
"""

from abc import ABC, abstractmethod
from typing import List

from models.patent import Patent


class BaseScraper(ABC):
    """Interface base para scrapers de patentes."""

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
        pass

    @abstractmethod
    def get_patent_details(self, patent_url: str) -> Patent:
        """
        Obtém detalhes completos de uma patente específica.

        Args:
            patent_url: URL da patente.

        Returns:
            Objeto Patent com detalhes completos.
        """
        pass
