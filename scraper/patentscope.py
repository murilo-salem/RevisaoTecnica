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

logger = logging.getLogger(__name__)


class PatentscopeScraper(BaseScraper):
    """Scraper para buscar patentes no Patentscope."""

    def __init__(self):
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
                return response
            except requests.exceptions.RequestException as e:
                wait_time = config.RETRY_DELAY * (2 ** attempt)
                logger.warning(
                    f"Tentativa {attempt + 1}/{config.RETRY_ATTEMPTS} falhou para {url}: {e}. "
                    f"Aguardando {wait_time}s..."
                )
                if attempt < config.RETRY_ATTEMPTS - 1:
                    time.sleep(wait_time)
                else:
                    logger.error(f"Todas as tentativas falharam para URL: {url}")
                    return None

    def search(self, query: str, max_results: int = 10) -> List[Patent]:
        """
        Busca patentes diretamente no Patentscope.
        Usa busca direta como primária para garantir persistência de sessão JSF.
        """
        patents = []
        logger.info(f"Buscando patentes no Patentscope para: '{query}'")

        # 1. Tenta DuckDuckGo primeiro (mais resiliente e menos chance de CAPTCHA imediato)
        links = self._search_duckduckgo(query, max_results)
        
        # 2. Se DDG falhar, tenta busca direta no Patentscope
        if not links:
            logger.warning("DuckDuckGo não retornou resultados. Tentando busca direta no Patentscope...")
            links = self._search_direct(query, max_results)

        if not links:
            logger.warning("Nenhum link do Patentscope encontrado por nenhum método.")
            return []

        # 3. Visita cada link para obter detalhes (reusando a mesma sessão)
        for i, url in enumerate(links[:max_results]):
            logger.info(f"Processando Patentscope {i+1}/{len(links[:max_results])}: {url}")
            try:
                patent = self.get_patent_details(url)
                if patent and patent.title:
                    patents.append(patent)
                
                # Delay amigável
                time.sleep(random.uniform(2.0, 4.0))
            except Exception as e:
                logger.error(f"Erro ao obter detalhes de {url}: {e}")

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
            logger.info(f"Encontrados {len(results)} links de resultados via busca direta")
            
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
            logger.error(f"Erro na busca direta Patentscope: {e}")
            
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
            logger.error(f"Erro na busca DuckDuckGo: {e}")
        return links

    def get_patent_details(self, patent_url: str) -> Patent:
        """
        Obtém detalhes completos de uma patente específica no Patentscope.
        """
        patent = Patent(source="Patentscope", url=patent_url)

        response = self._make_request(patent_url)
        if response is None:
            return patent

        logger.debug(f"Detail status: {response.status_code}, tamanho: {len(response.text)}")
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
