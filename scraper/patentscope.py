"""
Scraper para Patentscope (WIPO).

Realiza busca direta no Patentscope com persistência de sessão.
"""

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

class PatentscopeScraper(BaseScraper):
    """Scraper para buscar patentes no Patentscope."""

    def __init__(self):
        super().__init__()
        self.session = requests.Session()
        self.ua = random.choice(config.USER_AGENTS)
        self._update_headers()

    def _update_headers(self):
        """Atualiza headers com User-Agent fixo."""
        self.session.headers.update({
            "User-Agent": self.ua,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        })

    def _make_request(self, url: str, params: dict = None) -> Optional[requests.Response]:
        """Faz request com retry e backoff exponencial."""
        for attempt in range(config.RETRY_ATTEMPTS):
            try:
                response = self.session.get(
                    url,
                    params=params,
                    timeout=config.REQUEST_TIMEOUT,
                    allow_redirects=True
                )
                response.raise_for_status()
                if self._contains_block_signal(response.text):
                    self._add_diagnostic(
                        "blocked_or_captcha",
                        "Sinal de bloqueio/CAPTCHA detectado no Patentscope.",
                        response.url,
                    )
                return response
            except requests.exceptions.HTTPError as e:
                status_code = e.response.status_code if e.response is not None else "N/A"
                if status_code in {403, 429}:
                    self._add_diagnostic(
                        "blocked_http",
                        f"HTTP {status_code} ao acessar a origem.",
                        url,
                    )
                wait_time = config.RETRY_DELAY * (2 ** attempt)
                self._log(
                    logging.WARNING,
                    "scraper_request_retry",
                    url=url,
                    attempt=attempt + 1,
                    max_attempts=config.RETRY_ATTEMPTS,
                    status_code=status_code,
                    wait_time_seconds=wait_time,
                    detail=str(e),
                )
                if attempt < config.RETRY_ATTEMPTS - 1:
                    time.sleep(wait_time)
                else:
                    self._log(
                        logging.ERROR,
                        "scraper_request_failed",
                        url=url,
                        attempt=attempt + 1,
                        max_attempts=config.RETRY_ATTEMPTS,
                        detail=str(e),
                    )
                    return None
            except requests.exceptions.RequestException as e:
                wait_time = config.RETRY_DELAY * (2 ** attempt)
                self._log(
                    logging.WARNING,
                    "scraper_request_retry",
                    url=url,
                    attempt=attempt + 1,
                    max_attempts=config.RETRY_ATTEMPTS,
                    wait_time_seconds=wait_time,
                    detail=str(e),
                )
                if attempt < config.RETRY_ATTEMPTS - 1:
                    time.sleep(wait_time)
                else:
                    self._log(
                        logging.ERROR,
                        "scraper_request_failed",
                        url=url,
                        attempt=attempt + 1,
                        max_attempts=config.RETRY_ATTEMPTS,
                        detail=str(e),
                    )
                    return None

    def search(self, query: str, max_results: int = 10) -> List[Patent]:
        """
        Busca patentes diretamente no Patentscope.
        Usa busca direta como primária para garantir persistência de sessão JSF.
        """
        patents = []
        self._log(
            logging.INFO,
            "scraper_search_started",
            query=query,
            max_results=max_results,
            strategy="duckduckgo_then_patentscope_direct",
        )

        # 1. Tenta DuckDuckGo primeiro (mais resiliente e menos chance de CAPTCHA imediato)
        links = self._search_duckduckgo(query, max_results)
        
        # 2. Se DDG falhar, tenta busca direta no Patentscope
        if not links:
            self._log(
                logging.WARNING,
                "scraper_search_fallback",
                query=query,
                reason="duckduckgo_empty",
                fallback="patentscope_direct",
            )
            self._add_diagnostic(
                "discovery_empty",
                "DuckDuckGo não retornou links para Patentscope.",
                "https://html.duckduckgo.com/html/",
            )
            links = self._search_direct(query, max_results)

        if not links:
            self._log(
                logging.WARNING,
                "scraper_search_empty",
                query=query,
                source="patentscope",
            )
            return []

        # 3. Visita cada link para obter detalhes (reusando a mesma sessão)
        for i, url in enumerate(links[:max_results]):
            self._log(
                logging.INFO,
                "scraper_detail_fetch_started",
                query=query,
                index=i + 1,
                total=min(len(links), max_results),
                url=url,
            )
            try:
                patent = self.get_patent_details(url)
                if patent and patent.title:
                    patents.append(patent)
                
                # Delay amigável
                time.sleep(random.uniform(2.0, 4.0))
            except Exception as e:
                self._log(
                    logging.ERROR,
                    "scraper_detail_fetch_error",
                    query=query,
                    url=url,
                    detail=str(e),
                )

        self._log(
            logging.INFO,
            "scraper_search_completed",
            query=query,
            max_results=max_results,
            patents_found=len(patents),
        )

        return patents

    def _search_direct(self, query: str, max_results: int) -> List[str]:
        """Busca URLs diretamente no Patentscope."""
        url = "https://patentscope.wipo.int/search/en/result.jsf"
        params = {"queryString": query}
        
        links = []
        try:
            response = self._make_request(url, params=params)
            if not response:
                return []
            
            soup = BeautifulSoup(response.text, "lxml")
            # Usa seletores que ignoram o jsessionid no meio do href
            results = soup.select('a[href*="detail.jsf"][href*="docId="]')
            if not results and self._contains_block_signal(response.text):
                self._add_diagnostic(
                    "blocked_or_captcha",
                    "Busca direta do Patentscope retornou página com sinal de bloqueio.",
                    response.url,
                )
            self._log(
                logging.INFO,
                "scraper_direct_results_found",
                query=query,
                results=len(results),
                url=url,
            )
            
            for res in results:
                href = res.get("href", "")
                if "docId=" in href:
                    if not href.startswith("http"):
                        # MANTÉM o jsessionid e o _cid se presentes, pois o JSF precisa deles
                        # para vincular a visita ao detalhe à sessão de busca anterior.
                        clean_url = "https://patentscope.wipo.int/search/en/" + href
                    else:
                        clean_url = href
                        
                    if clean_url not in links:
                        links.append(clean_url)
                        
                if len(links) >= max_results:
                    break
                    
        except Exception as e:
            self._log(
                logging.ERROR,
                "scraper_direct_search_error",
                query=query,
                url=url,
                detail=str(e),
            )
            self._add_diagnostic(
                "search_error",
                f"Erro na busca direta do Patentscope: {e}",
                url,
            )
            
        return links

    def _search_duckduckgo(self, query: str, max_results: int) -> List[str]:
        """Busca URLs de patentes via DuckDuckGo HTML Lite."""
        # Tenta sem aspas primeiro para maior abrangência
        search_query = f"site:patentscope.wipo.int {query}"
        links = self._fetch_ddg_links(search_query, max_results)
        
        # Se não encontrar nada, tenta com o termo exato
        if not links:
            search_query = f'site:patentscope.wipo.int "{query}"'
            links = self._fetch_ddg_links(search_query, max_results)
            
        return links

    def _fetch_ddg_links(self, search_query: str, max_results: int) -> List[str]:
        """Método auxiliar para buscar links no DDG."""
        url = "https://html.duckduckgo.com/html/"
        params = {"q": search_query}
        links = []
        try:
            # Usa a sessão para manter consistência se possível
            response = self.session.get(url, params=params, timeout=15)
            if not response or response.status_code != 200:
                return []
                
            soup = BeautifulSoup(response.text, "lxml")
            results = soup.select(".result__a")
            if not results and self._contains_block_signal(response.text):
                self._add_diagnostic(
                    "blocked_or_captcha",
                    "DuckDuckGo retornou página com sinal de bloqueio.",
                    response.url,
                )
            
            for res in results:
                href = res.get("href", "")
                if "uddg=" in href:
                    href = urllib.parse.unquote(href.split("uddg=")[1].split("&")[0])
                
                if "patentscope.wipo.int/search/en/" in href:
                    if href not in links:
                        links.append(href)
                        
                if len(links) >= max_results:
                    break
        except Exception as e:
            self._log(
                logging.ERROR,
                "scraper_duckduckgo_error",
                query=search_query,
                url=url,
                detail=str(e),
            )
        return links

    def get_patent_details(self, patent_url: str) -> Patent:
        """
        Obtém detalhes completos de uma patente específica no Patentscope.
        """
        patent = Patent(source="Patentscope", url=patent_url)

        response = self._make_request(patent_url)
        if response is None:
            return patent

        self._log(
            logging.DEBUG,
            "scraper_detail_response",
            url=patent_url,
            status_code=response.status_code,
            response_chars=len(response.text),
        )
        soup = BeautifulSoup(response.text, "lxml")

        # Extrai ID da URL se possível (como fallback)
        if "docId=" in patent_url:
            query_params = urllib.parse.parse_qs(urllib.parse.urlparse(patent_url).query)
            if "docId" in query_params:
                patent.patent_id = query_params["docId"][0]

        # Título - Patentscope tem seletores variados
        # Prioriza seletores que funcionam na página carregada com sessão
        title_elem = soup.select_one(".ps-biblio-data--title, [id*='biblio-title'], .patent-title, h1")
        if title_elem:
            patent.title = title_elem.get_text(strip=True).replace("(EN)", "").strip()
        else:
            self._add_diagnostic(
                "layout_break",
                "Não foi possível extrair o título da página de detalhe do Patentscope.",
                patent_url,
            )

        # Abstract
        abstract_elem = soup.select_one(".ps-biblio-data--abstract, .patent-abstract, [id*='abstract']")
        if abstract_elem:
            patent.abstract = abstract_elem.get_text(strip=True)

        # Função auxiliar para extrair dados baseados no label
        def get_value_by_label(labels: List[str]) -> Optional[str]:
            for label_text in labels:
                # Procura por texto que contenha o label exato
                label_el = soup.find(lambda tag: tag.name in ["span", "div", "b", "label"] and 
                                     label_text == tag.get_text(strip=True))
                if not label_el:
                    # Tenta busca parcial se exata falhar
                    label_el = soup.find(lambda tag: tag.name in ["span", "div", "b", "label"] and 
                                         label_text in tag.get_text())
                
                if label_el:
                    val_text = ""
                    # Estrutura moderna: .ps-biblio-field > .ps-field--value
                    container = label_el.find_parent(class_="ps-biblio-field")
                    if container:
                        val_el = container.select_one(".ps-field--value")
                        if val_el:
                            # Preserva quebras de linha para inventores
                            val_text = val_el.get_text("\n", strip=True)
                    
                    # Estrutura legada: próximo sibling
                    if not val_text:
                        next_el = label_el.find_next_sibling()
                        if next_el:
                            val_text = next_el.get_text("\n", strip=True)
                    
                    if val_text:
                        # Remove snippets de JavaScript comuns e normaliza espaços
                        val_text = re.sub(r'if\(typeof\(load_w_scripts\).*?\);?', '', val_text)
                        val_text = re.sub(r'load_w_scripts\(\);?', '', val_text)
                        # Remove a marcação (EN), (FR), etc. se estiver no início
                        val_text = re.sub(r'^\([A-Z]{2}\)\s*', '', val_text)
                        
                        # Limpa linhas vazias e espaços extras
                        lines = [line.strip() for line in val_text.split("\n") if line.strip()]
                        return "; ".join(lines) if lines else None
            return None

        # Inventores
        inventors_text = get_value_by_label(["Inventors", "Inventor"])
        if inventors_text:
            for inv in re.split(r'[;]', inventors_text):
                name = inv.strip()
                if name and name not in patent.inventors:
                    patent.inventors.append(name)

        # Assignee
        patent.assignee = get_value_by_label(["Applicants", "Applicant", "Assignee"]) or ""

        # Datas
        patent.publication_date = get_value_by_label(["Publication Date"]) or ""
        patent.filing_date = get_value_by_label(["Filing Date", "International Filing Date"]) or ""

        return patent
