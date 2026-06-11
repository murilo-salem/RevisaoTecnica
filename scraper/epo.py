"""
Scraper para EPO Open Patent Services (OPS) API v3.2.

Autenticação OAuth2 com Consumer Key/Secret.
Configuração via variáveis de ambiente: EPO_CONSUMER_KEY, EPO_CONSUMER_SECRET.
"""

import base64
import logging
import re
import time
from typing import Any, Dict, List, Optional

import requests

import config
from models.patent import Patent
from scraper.base import BaseScraper


class EPOScraper(BaseScraper):
    """Scraper para buscar patentes via EPO Open Patent Services (OPS)."""

    _AUTH_URL = "https://ops.epo.org/3.2/auth/accesstoken"
    _SEARCH_URL = "https://ops.epo.org/3.2/rest-services/published-data/search"
    _BIBLIO_URL = "https://ops.epo.org/3.2/rest-services/published-data/publication/epodoc/{epodoc}/biblio"
    _ABSTRACT_URL = "https://ops.epo.org/3.2/rest-services/published-data/publication/epodoc/{epodoc}/abstract"
    _ESPACENET_URL = "https://worldwide.espacenet.com/patent/search?q=pn%3D{epodoc}"

    def __init__(self):
        super().__init__()
        self.consumer_key = config.EPO_CONSUMER_KEY
        self.consumer_secret = config.EPO_CONSUMER_SECRET
        self.session = requests.Session()
        self._token: Optional[str] = None
        self._token_expires_at: float = 0.0

    # ------------------------------------------------------------------
    # Auth
    # ------------------------------------------------------------------

    def _get_token(self) -> Optional[str]:
        if self._token and time.time() < self._token_expires_at - 60:
            return self._token

        credentials = base64.b64encode(
            f"{self.consumer_key}:{self.consumer_secret}".encode()
        ).decode()
        try:
            resp = requests.post(
                self._AUTH_URL,
                headers={
                    "Authorization": f"Basic {credentials}",
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                data="grant_type=client_credentials",
                timeout=15,
            )
            resp.raise_for_status()
            data = resp.json()
            self._token = data["access_token"]
            self._token_expires_at = time.time() + int(data.get("expires_in", 1200))
            self._log(logging.INFO, "epo_auth_ok", expires_in=data.get("expires_in"))
            return self._token
        except Exception as exc:
            self._log(logging.ERROR, "epo_auth_error", detail=str(exc))
            return None

    def _auth_headers(self) -> dict:
        token = self._get_token()
        return {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
        }

    # ------------------------------------------------------------------
    # Search
    # ------------------------------------------------------------------

    def search(self, query: str, max_results: int = 10) -> List[Patent]:
        self._log(logging.INFO, "scraper_search_started", query=query, max_results=max_results)

        if not self.consumer_key or not self.consumer_secret:
            self._add_diagnostic(
                "config_missing",
                "EPO_CONSUMER_KEY ou EPO_CONSUMER_SECRET não configurados.",
            )
            return []

        if not self._get_token():
            self._add_diagnostic("auth_failed", "Falha na autenticação com a API do EPO.")
            return []

        cap = min(max_results, 25)  # EPO OPS max por request é 25
        cql_query = f'ta any "{query}"'

        try:
            resp = self.session.get(
                self._SEARCH_URL,
                headers={
                    **self._auth_headers(),
                    "X-OPS-Range": f"1-{cap}",
                },
                params={"q": cql_query},
                timeout=config.REQUEST_TIMEOUT,
            )
            resp.raise_for_status()
            data = resp.json()
        except requests.HTTPError as exc:
            status = exc.response.status_code if exc.response is not None else "N/A"
            self._log(logging.ERROR, "epo_search_http_error", status=status, query=query)
            self._add_diagnostic("search_failed", f"HTTP {status} na busca EPO.")
            return []
        except Exception as exc:
            self._log(logging.ERROR, "epo_search_error", query=query, detail=str(exc))
            self._add_diagnostic("search_failed", f"Erro na busca EPO: {exc}")
            return []

        epodocs = self._extract_epodocs(data)
        total = self._extract_total(data)
        self._log(
            logging.INFO,
            "epo_search_results",
            total_available=total,
            fetching=len(epodocs),
            query=query,
        )

        if not epodocs:
            self._add_diagnostic("search_empty", f"EPO OPS não retornou resultados para: {query}")
            return []

        patents: List[Patent] = []
        for epodoc in epodocs[:max_results]:
            try:
                patent = self._fetch_patent(epodoc)
                if patent and patent.title:
                    patents.append(patent)
                time.sleep(0.4)  # respeita rate limit EPO (4 req/s)
            except Exception as exc:
                self._log(logging.ERROR, "epo_biblio_error", epodoc=epodoc, detail=str(exc))

        self._log(
            logging.INFO,
            "scraper_search_completed",
            query=query,
            patents_found=len(patents),
        )
        return patents

    # ------------------------------------------------------------------
    # Parsers de resposta
    # ------------------------------------------------------------------

    @staticmethod
    def _str_field(node: Any) -> str:
        if isinstance(node, dict):
            return node.get("$", "")
        return str(node) if node else ""

    @staticmethod
    def _format_date(raw: str) -> str:
        raw = raw.strip()
        if len(raw) == 8 and raw.isdigit():
            return f"{raw[:4]}-{raw[4:6]}-{raw[6:]}"
        return raw

    def _extract_epodocs(self, data: dict) -> List[str]:
        try:
            world = data.get("ops:world-patent-data", {})
            search = world.get("ops:biblio-search", {})
            result = search.get("ops:search-result", {})
            refs = result.get("ops:publication-reference", [])
            if isinstance(refs, dict):
                refs = [refs]

            epodocs = []
            for ref in refs:
                doc_id = ref.get("document-id", {})
                # pode vir como lista (múltiplos formatos) ou dict
                if isinstance(doc_id, list):
                    doc_id = next(
                        (d for d in doc_id if d.get("@document-id-type") == "epodoc"),
                        doc_id[0] if doc_id else {},
                    )
                country = self._str_field(doc_id.get("country", ""))
                doc_num = self._str_field(doc_id.get("doc-number", ""))
                kind = self._str_field(doc_id.get("kind", ""))
                if country and doc_num:
                    epodoc = f"{country}{doc_num}"
                    if kind:
                        epodoc += f".{kind}"
                    epodocs.append(epodoc)
            return epodocs
        except Exception as exc:
            self._log(logging.WARNING, "epo_parse_refs_error", detail=str(exc))
            return []

    @staticmethod
    def _extract_total(data: dict) -> int:
        try:
            world = data.get("ops:world-patent-data", {})
            search = world.get("ops:biblio-search", {})
            return int(search.get("@total-result-count", 0))
        except Exception:
            return 0

    # ------------------------------------------------------------------
    # Busca de dados de uma patente individual
    # ------------------------------------------------------------------

    def _fetch_patent(self, epodoc: str) -> Optional[Patent]:
        patent = Patent(
            source="EPO",
            patent_id=epodoc,
            url=self._ESPACENET_URL.format(epodoc=epodoc),
        )
        self._fetch_biblio_into(epodoc, patent)
        if patent.title:
            patent.abstract = self._fetch_abstract(epodoc)
        return patent

    def _fetch_biblio_into(self, epodoc: str, patent: Patent) -> None:
        url = self._BIBLIO_URL.format(epodoc=epodoc)
        try:
            resp = self.session.get(url, headers=self._auth_headers(), timeout=config.REQUEST_TIMEOUT)
            resp.raise_for_status()
            data = resp.json()
        except Exception as exc:
            self._log(logging.WARNING, "epo_biblio_fetch_error", epodoc=epodoc, detail=str(exc))
            return

        try:
            world = data.get("ops:world-patent-data", {})
            docs = world.get("exchange-documents", {}).get("exchange-document", {})
            if isinstance(docs, list):
                docs = docs[0]
            bib: Dict[str, Any] = docs.get("bibliographic-data", {})

            # Título — prefere inglês
            titles = bib.get("invention-title", [])
            if isinstance(titles, dict):
                titles = [titles]
            en_title = next(
                (self._str_field(t.get("$", t)) for t in titles if t.get("@lang") == "en"),
                "",
            )
            patent.title = en_title or (
                self._str_field(titles[0].get("$", titles[0])) if titles else ""
            )

            # Inventores
            inv_list = bib.get("parties", {}).get("inventors", {}).get("inventor", [])
            if isinstance(inv_list, dict):
                inv_list = [inv_list]
            for inv in inv_list:
                name = self._str_field(
                    inv.get("inventor-name", {}).get("name", {})
                )
                if name and name not in patent.inventors:
                    patent.inventors.append(name)

            # Requerente (assignee)
            app_list = bib.get("parties", {}).get("applicants", {}).get("applicant", [])
            if isinstance(app_list, dict):
                app_list = [app_list]
            if app_list:
                patent.assignee = self._str_field(
                    app_list[0].get("applicant-name", {}).get("name", {})
                )

            # Data de publicação
            pub_ref = bib.get("publication-reference", {})
            if isinstance(pub_ref, list):
                pub_ref = pub_ref[0]
            pub_doc_ids = pub_ref.get("document-id", [])
            if isinstance(pub_doc_ids, dict):
                pub_doc_ids = [pub_doc_ids]
            for doc_id in pub_doc_ids:
                raw_date = self._str_field(doc_id.get("date", ""))
                if raw_date:
                    patent.publication_date = self._format_date(raw_date)
                    break

            # Data de depósito
            app_ref = bib.get("application-reference", {})
            if isinstance(app_ref, list):
                app_ref = app_ref[0]
            app_doc_ids = app_ref.get("document-id", [])
            if isinstance(app_doc_ids, dict):
                app_doc_ids = [app_doc_ids]
            for doc_id in app_doc_ids:
                raw_date = self._str_field(doc_id.get("date", ""))
                if raw_date:
                    patent.filing_date = self._format_date(raw_date)
                    break

        except Exception as exc:
            self._log(logging.WARNING, "epo_biblio_parse_error", epodoc=epodoc, detail=str(exc))

    def _fetch_abstract(self, epodoc: str) -> str:
        url = self._ABSTRACT_URL.format(epodoc=epodoc)
        try:
            resp = self.session.get(url, headers=self._auth_headers(), timeout=config.REQUEST_TIMEOUT)
            if resp.status_code == 404:
                return ""
            resp.raise_for_status()
            data = resp.json()

            world = data.get("ops:world-patent-data", {})
            docs = world.get("exchange-documents", {}).get("exchange-document", {})
            if isinstance(docs, list):
                docs = docs[0]

            abstracts = docs.get("abstract", [])
            if isinstance(abstracts, dict):
                abstracts = [abstracts]

            # Prefere inglês
            en_abs = next(
                (a for a in abstracts if a.get("@lang") == "en"),
                abstracts[0] if abstracts else {},
            )
            paras = en_abs.get("p", [])
            if isinstance(paras, str):
                return paras
            if isinstance(paras, dict):
                paras = [paras]
            return " ".join(
                self._str_field(p.get("$", p)) if isinstance(p, dict) else str(p)
                for p in paras
            ).strip()
        except Exception as exc:
            self._log(logging.WARNING, "epo_abstract_fetch_error", epodoc=epodoc, detail=str(exc))
            return ""

    # ------------------------------------------------------------------
    # get_patent_details (interface do BaseScraper)
    # ------------------------------------------------------------------

    def get_patent_details(self, patent_url: str) -> Patent:
        match = re.search(r'pn%3D([A-Z]{2}[\dA-Z]+(?:\.[A-Z]\d*)?)', patent_url)
        if not match:
            match = re.search(r'/([A-Z]{2}\d+[A-Z]\d*)', patent_url)
        if match:
            epodoc = match.group(1)
            result = self._fetch_patent(epodoc)
            if result:
                return result
        return Patent(source="EPO", url=patent_url)
