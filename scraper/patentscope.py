"""
Scraper para Patentscope (WIPO).

Busca direta em result.jsf (com _cid e sessão JSF) como caminho primário;
DuckDuckGo como fallback.
"""

import logging
import random
import re
import ssl
import time
import urllib.parse
from typing import Dict, List, Optional

import requests
from bs4 import BeautifulSoup

import config
from models.patent import Patent
from scraper.base import BaseScraper


class _PatentscopeHTTPAdapter(requests.adapters.HTTPAdapter):
    """Força ALPN http/1.1; sem isso PatentScope responde com CAPTCHA ou timeout."""

    def init_poolmanager(self, *args, **kwargs):
        ctx = ssl.create_default_context()
        ctx.set_alpn_protocols(["http/1.1"])
        kwargs["ssl_context"] = ctx
        super().init_poolmanager(*args, **kwargs)


class PatentscopeScraper(BaseScraper):
    """Scraper para buscar patentes no Patentscope."""

    _BASE = "https://patentscope.wipo.int/search/en"
    _RESULT_URL = f"{_BASE}/result.jsf"
    _DETAIL_URL = f"{_BASE}/detail.jsf"

    def __init__(self):
        super().__init__()
        self.session = requests.Session()
        self.session.mount("https://", _PatentscopeHTTPAdapter())
        self._current_cid: Optional[str] = None
        self.ua = random.choice(config.USER_AGENTS)
        self._update_headers()

    def _update_headers(self):
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
                    allow_redirects=True,
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
                    self._add_diagnostic("blocked_http", f"HTTP {status_code} ao acessar a origem.", url)
                wait_time = config.RETRY_DELAY * (2 ** attempt)
                self._log(logging.WARNING, "scraper_request_retry", url=url, attempt=attempt + 1,
                          max_attempts=config.RETRY_ATTEMPTS, status_code=status_code,
                          wait_time_seconds=wait_time, detail=str(e))
                if attempt < config.RETRY_ATTEMPTS - 1:
                    time.sleep(wait_time)
                else:
                    self._log(logging.ERROR, "scraper_request_failed", url=url,
                              attempt=attempt + 1, max_attempts=config.RETRY_ATTEMPTS, detail=str(e))
                    return None
            except requests.exceptions.RequestException as e:
                wait_time = config.RETRY_DELAY * (2 ** attempt)
                self._log(logging.WARNING, "scraper_request_retry", url=url, attempt=attempt + 1,
                          max_attempts=config.RETRY_ATTEMPTS, wait_time_seconds=wait_time, detail=str(e))
                if attempt < config.RETRY_ATTEMPTS - 1:
                    time.sleep(wait_time)
                else:
                    self._log(logging.ERROR, "scraper_request_failed", url=url,
                              attempt=attempt + 1, max_attempts=config.RETRY_ATTEMPTS, detail=str(e))
                    return None

    # -------------------------------------------------------------------------
    # Public interface
    # -------------------------------------------------------------------------

    def search(self, query: str, max_results: int = 10) -> List[Patent]:
        """Busca patentes no Patentscope: JSF direto → DuckDuckGo como fallback."""
        self._log(logging.INFO, "scraper_search_started", query=query, max_results=max_results,
                  strategy="jsf_direct_then_duckduckgo")

        patents = self._search_jsf_direct(query, max_results)

        if not patents:
            self._log(logging.WARNING, "scraper_search_fallback", query=query,
                      reason="jsf_direct_empty", fallback="duckduckgo")
            patents = self._search_via_duckduckgo(query, max_results)

        self._log(logging.INFO, "scraper_search_completed", query=query,
                  max_results=max_results, patents_found=len(patents))
        return patents

    def get_patent_details(self, patent_url: str) -> Patent:
        """Obtém detalhes completos de uma patente específica no Patentscope."""
        patent = Patent(source="Patentscope", url=patent_url)

        parsed = urllib.parse.urlparse(patent_url)
        qs = urllib.parse.parse_qs(parsed.query)
        if "docId" in qs:
            patent.patent_id = qs["docId"][0]

        response = self._make_request(patent_url)
        if response is None:
            return patent

        self._log(logging.DEBUG, "scraper_detail_response", url=patent_url,
                  status_code=response.status_code, response_chars=len(response.text))

        soup = BeautifulSoup(response.text, "lxml")

        if not self._is_session_valid(soup):
            self._add_diagnostic(
                "detail_session_expired",
                "Página de detalhe sem campos biblio — sessão/cid pode ter expirado.",
                patent_url,
            )
            return patent

        return self._parse_detail_page(soup, patent_url, base_patent=patent)

    # -------------------------------------------------------------------------
    # Primary path: JSF direct
    # -------------------------------------------------------------------------

    def _search_jsf_direct(self, query: str, max_results: int) -> List[Patent]:
        """Busca direta em result.jsf, extrai _cid e lista de stubs."""
        response = self._fetch_jsf_page(query, min(max_results, config.PATENTSCOPE_PAGE_SIZE))
        if response is None:
            return []

        soup = BeautifulSoup(response.text, "lxml")
        stubs = self._parse_result_list(soup)

        if not stubs:
            self._add_diagnostic(
                "jsf_empty_results",
                f"Nenhum resultado em result.jsf para query: {query}",
                self._RESULT_URL,
            )
            return []

        if not self._current_cid:
            self._add_diagnostic(
                "cid_not_found",
                "_cid ausente nos hrefs — sessão JSF pode estar inativa.",
                self._RESULT_URL,
            )

        return self._enrich_with_details(stubs, max_results)

    def _fetch_jsf_page(self, query: str, page_size: int) -> Optional[requests.Response]:
        """GET result.jsf, armazena self._current_cid a partir dos hrefs retornados."""
        response = self._make_request(
            self._RESULT_URL,
            params={"queryString": query, "pageSize": page_size},
        )
        if response is None:
            return None

        soup = BeautifulSoup(response.text, "lxml")
        first_link = soup.select_one('a[href*="detail.jsf"][href*="_cid="]')
        if first_link:
            cid_match = re.search(r'[?&]_cid=([^&]+)', first_link.get("href", ""))
            if cid_match:
                self._current_cid = cid_match.group(1)

        return response

    def _parse_result_list(self, soup: BeautifulSoup) -> List[Dict]:
        """Extrai lista de stubs [{doc_id, title, pub_date}] da página de resultados."""
        stubs = []
        seen_ids: set = set()

        for link in soup.select('a[href*="detail.jsf"][href*="docId="]'):
            href = link.get("href", "")
            qs = urllib.parse.parse_qs(urllib.parse.urlparse(href).query)
            doc_id = qs.get("docId", [None])[0]
            if not doc_id or doc_id in seen_ids:
                continue
            seen_ids.add(doc_id)

            title_span = (
                link.select_one("span.trans-section")
                or link.select_one("span.ps-patent-result--title--title")
            )
            title = (title_span or link).get_text(strip=True)
            title = re.sub(r'^\([A-Z]{2}\)\s*', '', title).strip()

            pub_date = ""
            row = link.find_parent("tr") or link.find_parent(
                class_=re.compile(r"ps-patent-result")
            )
            if row:
                date_el = row.select_one('[id*="PubDate"], [id*="pubDate"], [class*="pubDate"]')
                if date_el:
                    pub_date = date_el.get_text(strip=True)

            stubs.append({"doc_id": doc_id, "title": title, "pub_date": pub_date})

        return stubs

    def _enrich_with_details(self, stubs: List[Dict], max_results: int) -> List[Patent]:
        """Visita detail.jsf para cada stub e retorna Patents completos."""
        patents = []
        delay_min, delay_max = config.PATENTSCOPE_DETAIL_DELAY

        for stub in stubs[:max_results]:
            url = self._build_detail_url(stub["doc_id"])
            self._log(logging.INFO, "scraper_detail_fetch_started", doc_id=stub["doc_id"], url=url)
            try:
                patent = self.get_patent_details(url)

                if not self._is_session_valid(BeautifulSoup("", "lxml")) and not patent.title:
                    # Sessão expirou: renova _cid e retenta uma vez
                    self._log(logging.WARNING, "scraper_session_renew", doc_id=stub["doc_id"])
                    renewed = self._fetch_jsf_page(stub.get("title", ""), 1)
                    if renewed and self._current_cid:
                        url = self._build_detail_url(stub["doc_id"])
                        patent = self.get_patent_details(url)

                if not patent.title and stub["title"]:
                    patent.title = stub["title"]
                if not patent.publication_date and stub["pub_date"]:
                    patent.publication_date = stub["pub_date"]

                if patent.title:
                    patents.append(patent)
            except Exception as e:
                self._log(logging.ERROR, "scraper_detail_fetch_error",
                          doc_id=stub["doc_id"], url=url, detail=str(e))

            time.sleep(random.uniform(delay_min, delay_max))

        return patents

    # -------------------------------------------------------------------------
    # Detail page parsing
    # -------------------------------------------------------------------------

    def _parse_detail_page(
        self,
        soup: BeautifulSoup,
        patent_url: str,
        base_patent: Optional[Patent] = None,
    ) -> Patent:
        """Extrai Patent de uma soup de detail.jsf."""
        patent = base_patent or Patent(source="Patentscope", url=patent_url)

        title_raw = self._get_biblio_field(soup, "Title")
        if title_raw:
            patent.title = re.sub(r'^\([A-Z]{2}\)\s*', '', title_raw).strip()
        else:
            self._add_diagnostic("layout_break", "Título não encontrado na página de detalhe.", patent_url)

        pub_number = self._get_biblio_field(soup, "Publication Number")
        if pub_number:
            patent.patent_id = pub_number.strip()

        abstract_el = soup.select_one(".patent-abstract")
        if abstract_el:
            patent.abstract = abstract_el.get_text(strip=True)

        patent.publication_date = self._get_biblio_field(soup, "Publication Date") or ""
        patent.filing_date = (
            self._get_biblio_field(soup, "Application Date", "Filing Date", "International Filing Date")
            or ""
        )
        patent.assignee = self._get_biblio_field(soup, "Applicants", "Applicant", "Assignee") or ""

        inventors_raw = self._get_biblio_field(soup, "Inventors", "Inventor")
        if inventors_raw:
            patent.inventors = [
                name.strip()
                for name in re.split(r'[\n;]', inventors_raw)
                if name.strip()
            ]

        return patent

    def _get_biblio_field(self, soup: BeautifulSoup, *labels: str) -> Optional[str]:
        """Busca .ps-biblio-field cujo label bate com qualquer dos labels fornecidos."""
        for field in soup.select(".ps-biblio-field"):
            # Label: primeiro filho direto que não seja .ps-field--value
            label_el = None
            for child in field.children:
                if not hasattr(child, "name") or not child.name:
                    continue
                if "ps-field--value" not in (child.get("class") or []):
                    label_el = child
                    break

            if not label_el or label_el.get_text(strip=True) not in labels:
                continue

            # Value: .ps-field--value ou próximo sibling do label
            val_el = field.select_one(".ps-field--value") or label_el.find_next_sibling()
            if not val_el:
                continue

            raw = val_el.get_text("\n", strip=True)
            raw = re.sub(r'if\(typeof\(load_w_scripts\).*?\);?', '', raw, flags=re.DOTALL)
            raw = re.sub(r'load_w_scripts\(\);?', '', raw)
            lines = [line.strip() for line in raw.split("\n") if line.strip()]
            return "\n".join(lines) if lines else None

        return None

    def _build_detail_url(self, doc_id: str) -> str:
        """Constrói URL de detalhe com docId e _cid da sessão atual."""
        params: Dict[str, str] = {"docId": doc_id}
        if self._current_cid:
            params["_cid"] = self._current_cid
        return f"{self._DETAIL_URL}?{urllib.parse.urlencode(params)}"

    def _is_session_valid(self, soup: BeautifulSoup) -> bool:
        """True se a página retornou ao menos um campo biblio."""
        return bool(soup.select(".ps-biblio-field"))

    # -------------------------------------------------------------------------
    # Fallback path: DuckDuckGo
    # -------------------------------------------------------------------------

    def _search_via_duckduckgo(self, query: str, max_results: int) -> List[Patent]:
        """Fallback: descobre URLs via DuckDuckGo e visita cada detail.jsf."""
        links = self._search_duckduckgo(query, max_results)
        if not links:
            self._add_diagnostic(
                "discovery_empty",
                "DuckDuckGo não retornou links para Patentscope.",
                "https://html.duckduckgo.com/html/",
            )
            return []

        patents = []
        delay_min, delay_max = config.PATENTSCOPE_DETAIL_DELAY
        for url in links[:max_results]:
            try:
                patent = self.get_patent_details(url)
                if patent and patent.title:
                    patents.append(patent)
                time.sleep(random.uniform(delay_min, delay_max))
            except Exception as e:
                self._log(logging.ERROR, "scraper_detail_fetch_error", url=url, detail=str(e))
        return patents

    def _search_duckduckgo(self, query: str, max_results: int) -> List[str]:
        """Busca URLs de patentes via DuckDuckGo HTML Lite."""
        links = self._fetch_ddg_links(f"site:patentscope.wipo.int {query}", max_results)
        if not links:
            links = self._fetch_ddg_links(f'site:patentscope.wipo.int "{query}"', max_results)
        return links

    def _fetch_ddg_links(self, search_query: str, max_results: int) -> List[str]:
        links = []
        try:
            response = self.session.get(
                "https://html.duckduckgo.com/html/",
                params={"q": search_query},
                timeout=15,
            )
            if not response or response.status_code != 200:
                return []

            soup = BeautifulSoup(response.text, "lxml")
            if self._contains_block_signal(response.text):
                self._add_diagnostic(
                    "blocked_or_captcha",
                    "DuckDuckGo retornou página com sinal de bloqueio.",
                    response.url,
                )

            for res in soup.select(".result__a"):
                href = res.get("href", "")
                if "uddg=" in href:
                    href = urllib.parse.unquote(href.split("uddg=")[1].split("&")[0])
                if "patentscope.wipo.int/search/en/" in href and href not in links:
                    links.append(href)
                if len(links) >= max_results:
                    break
        except Exception as e:
            self._log(logging.ERROR, "scraper_duckduckgo_error", query=search_query, detail=str(e))
        return links
