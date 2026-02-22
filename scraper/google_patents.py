"""
Scraper para Google Patents.

Realiza scraping de patentes no Google Patents usando requests + BeautifulSoup.
"""

import json
import logging
import random
import re
import time
import urllib.parse
from typing import List, Optional

import requests
from bs4 import BeautifulSoup

import config
from models.patent import Patent
from scraper.base import BaseScraper

logger = logging.getLogger(__name__)


class GooglePatentsScraper(BaseScraper):
    """Scraper para buscar patentes no Google Patents."""

    def __init__(self):
        self.session = requests.Session()
        # Usa um único User-Agent por sessão para parecer mais humano
        self.ua = random.choice(config.USER_AGENTS)
        self._update_headers()

    def _update_headers(self):
        """Atualiza headers com User-Agent fixo e Referer."""
        self.session.headers.update({
            "User-Agent": self.ua,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Referer": "https://duckduckgo.com/",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "cross-site",
        })

    def _make_request(self, url: str, params: dict = None) -> Optional[requests.Response]:
        """Faz request com retry e backoff exponencial."""
        for attempt in range(config.RETRY_ATTEMPTS):
            try:
                # Remove compression header that might cause issues with some environments
                if "Accept-Encoding" in self.session.headers:
                    del self.session.headers["Accept-Encoding"]
                
                response = self.session.get(
                    url,
                    params=params,
                    timeout=config.REQUEST_TIMEOUT,
                    allow_redirects=True
                )
                response.raise_for_status()
                return response
            except requests.exceptions.RequestException as e:
                wait_time = config.RETRY_DELAY * (2 ** attempt)
                logger.warning(
                    f"Tentativa {attempt + 1}/{config.RETRY_ATTEMPTS} falhou: {e}. "
                    f"Aguardando {wait_time}s..."
                )
                if attempt < config.RETRY_ATTEMPTS - 1:
                    time.sleep(wait_time)
                else:
                    logger.error(f"Todas as tentativas falharam para URL: {url}")
                    return None

    def search(self, query: str, max_results: int = 10) -> List[Patent]:
        """
        Busca patentes usando DuckDuckGo para encontrar links do Google Patents.
        Esta abordagem é mais robusta contra bloqueios e SPAs.
        """
        patents = []
        logger.info(f"Buscando patentes via DuckDuckGo para: '{query}'")

        # 1. Busca links no DuckDuckGo HTML
        links = self._search_duckduckgo(query, max_results)
        
        if not links:
            logger.warning("Nenhum link encontrado via DuckDuckGo. Tentando Google Scholar...")
            return self._search_html_fallback(query, max_results)

        # 2. Visita cada link para obter detalhes
        for i, url in enumerate(links[:max_results]):
            logger.info(f"Processando patente {i+1}/{len(links[:max_results])}: {url}")
            try:
                patent = self.get_patent_details(url)
                if patent and patent.title:
                    patents.append(patent)
                
                # Delay amigável
                time.sleep(random.uniform(1.0, 2.0))
            except Exception as e:
                logger.error(f"Erro ao obter detalhes de {url}: {e}")

        return patents

    def _search_duckduckgo(self, query: str, max_results: int) -> List[str]:
        """Busca URLs de patentes via DuckDuckGo HTML."""
        # Tenta primeiro sem aspas para maior abrangência
        search_query = f"site:patents.google.com {query}"
        links = self._fetch_ddg_links(search_query, max_results)
        
        # Se não encontrar nada, tenta com o termo exato
        if not links:
            search_query = f'site:patents.google.com "{query}"'
            links = self._fetch_ddg_links(search_query, max_results)
            
        return links

    def _fetch_ddg_links(self, search_query: str, max_results: int) -> List[str]:
        """Método auxiliar para buscar links no DDG."""
        url = "https://html.duckduckgo.com/html/"
        params = {"q": search_query}
        links = []
        try:
            response = self._make_request(url, params=params)
            if not response:
                return []
            
            soup = BeautifulSoup(response.text, "lxml")
            results = soup.select(".result__a")
            for res in results:
                href = res.get("href", "")
                if "uddg=" in href:
                    href = urllib.parse.unquote(href.split("uddg=")[1].split("&")[0])
                
                if "patents.google.com/patent/" in href:
                    clean_url = href.split("?")[0].split("#")[0]
                    if clean_url not in links:
                        links.append(clean_url)
                if len(links) >= max_results:
                    break
        except Exception as e:
            logger.error(f"Erro ao buscar no DDG: {e}")
        return links

    def get_patent_details(self, patent_url: str) -> Patent:
        """
        Obtém detalhes completos de uma patente específica.
        Analisa as tags semânticas do Google Patents.
        """
        patent = Patent(source="Google Patents", url=patent_url)

        # Extrai patent ID da URL
        match = re.search(r'/patent/([A-Z]{2}\d+[A-Z]?\d*)', patent_url)
        if match:
            patent.patent_id = match.group(1)

        response = self._make_request(patent_url)
        if response is None:
            return patent

        soup = BeautifulSoup(response.text, "lxml")

        # Título - Google Patents usa itemprop="title"
        title_elem = soup.select_one('[itemprop="title"]')
        if title_elem:
            patent.title = title_elem.get_text(strip=True)
        else:
            # Fallback para title tag
            title_tag = soup.find("title")
            if title_tag:
                patent.title = title_tag.get_text(strip=True).replace(" - Google Patents", "")

        # Abstract - itemprop="abstract" ou name="description"
        abstract_elem = soup.select_one('[itemprop="abstract"]')
        if abstract_elem:
            patent.abstract = abstract_elem.get_text(strip=True)
        else:
            meta_desc = soup.find("meta", {"name": "description"})
            if meta_desc:
                patent.abstract = meta_desc.get("content", "").strip()

        # Inventores - itemprop="inventor"
        inventor_elems = soup.select('[itemprop="inventor"]')
        for elem in inventor_elems:
            name = elem.get_text(strip=True)
            if name and name not in patent.inventors:
                patent.inventors.append(name)

        # Assignee / Titular - itemprop="assignee" ou "assigneeOriginal"
        assignee_elem = soup.select_one('[itemprop="assigneeOriginal"], [itemprop="assignee"]')
        if assignee_elem:
            patent.assignee = assignee_elem.get_text(strip=True)

        # Datas
        filing_date_elem = soup.select_one('[itemprop="filingDate"]')
        if filing_date_elem:
            patent.filing_date = filing_date_elem.get_text(strip=True)
            
        pub_date_elem = soup.select_one('[itemprop="publicationDate"]')
        if pub_date_elem:
            patent.publication_date = pub_date_elem.get_text(strip=True)

        return patent

    def _search_html_fallback(self, query: str, max_results: int) -> List[Patent]:
        """Busca direta via endpoint XHR do Google Patents."""
        logger.info(f"Tentando busca via XHR no Google Patents para: {query}")
        patents = []
        
        # Endpoint XHR que retorna JSON estruturado
        url = "https://patents.google.com/xhr/query"
        params = {
            "url": f"q=({query})",
            "exp": ""
        }
        
        try:
            response = self._make_request(url, params=params)
            if response and response.status_code == 200:
                data = response.json()
                if 'results' in data and 'cluster' in data['results']:
                    results_list = data['results']['cluster'][0].get('result', [])
                    
                    for item in results_list[:max_results]:
                        pub_num = item.get('patent', {}).get('publication_number')
                        if pub_num:
                            url_patent = f"https://patents.google.com/patent/{pub_num}/en"
                            try:
                                p = self.get_patent_details(url_patent)
                                if p and p.title:
                                    patents.append(p)
                                time.sleep(random.uniform(1, 2))
                            except Exception as e:
                                logger.error(f"Erro ao processar patente {pub_num}: {e}")
            
            # Se ainda não encontramos nada, tenta parsing básico do HTML
            if not patents:
                logger.warning("XHR não retornou resultados. Tentando parsing HTML básico...")
                # ... existing logic or skip
                
        except Exception as e:
            logger.error(f"Erro na busca Google Patents XHR: {e}")
            
        return patents
