"""
Interface Streamlit — Revisão Técnica de Patentes.
Comunica-se com o backend via REST API (API_BASE_URL).

Modos:
  - Busca por Query: fluxo original (query texto → patentes → LLM screening)
  - Análise de Artigo: upload PDF/texto + descrição → claims → busca → extração → whitespace
"""

import io
import os
import time
from typing import Optional

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import streamlit as st

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
_DEFAULT_MODEL = os.getenv("OLLAMA_MODEL", "gemma3:27b")
_DEFAULT_EXTRACT_MODEL = os.getenv("OLLAMA_EXTRACTION_MODEL", "gemma3:12b")
_POLL_INTERVAL = 2  # segundos entre polls durante execução

st.set_page_config(
    page_title="Revisão Técnica de Patentes",
    page_icon="🔬",
    layout="wide",
)

# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------
_DEFAULTS = {
    # Modo
    "mode": "query",  # "query" | "article"
    # Query mode
    "running": False,
    "run_id": None,
    "run_data": None,
    "live_data": {},
    "error": None,
    "selected_decisions": ["include", "review", "exclude"],
    "selected_sources": [],
    # Article mode (also used for query+innovation)
    "article_running": False,
    "article_run_id": None,
    "article_run_data": None,
    "article_live_data": {},
    "article_error": None,
}
for _k, _v in _DEFAULTS.items():
    if _k not in st.session_state:
        st.session_state[_k] = _v

# ---------------------------------------------------------------------------
# API helpers — query mode
# ---------------------------------------------------------------------------

@st.cache_data(ttl=60)
def _fetch_models() -> list[str]:
    try:
        r = requests.get(f"{API_BASE_URL}/models", timeout=5)
        return r.json().get("models", [_DEFAULT_MODEL]) if r.ok else [_DEFAULT_MODEL]
    except Exception:
        return [_DEFAULT_MODEL]


@st.cache_data(ttl=10)
def _fetch_runs() -> list[dict]:
    try:
        r = requests.get(f"{API_BASE_URL}/runs", timeout=5)
        return r.json() if r.ok else []
    except Exception:
        return []


def _poll_run(run_id: str) -> dict:
    try:
        r = requests.get(f"{API_BASE_URL}/runs/{run_id}", timeout=10)
        return r.json() if r.ok else {}
    except Exception:
        return {}


def _start_run(payload: dict) -> Optional[str]:
    try:
        r = requests.post(f"{API_BASE_URL}/runs", json=payload, timeout=10)
        r.raise_for_status()
        return r.json()["run_id"]
    except Exception as exc:
        st.session_state.error = f"Falha ao iniciar: {exc}"
        return None


# ---------------------------------------------------------------------------
# API helpers — article mode
# ---------------------------------------------------------------------------

def _start_article_run(payload: dict) -> Optional[str]:
    try:
        r = requests.post(f"{API_BASE_URL}/article-runs", json=payload, timeout=10)
        r.raise_for_status()
        return r.json()["run_id"]
    except Exception as exc:
        st.session_state.article_error = f"Falha ao iniciar análise de artigo: {exc}"
        return None


def _poll_article_run(run_id: str) -> dict:
    try:
        r = requests.get(f"{API_BASE_URL}/article-runs/{run_id}", timeout=10)
        return r.json() if r.ok else {}
    except Exception:
        return {}


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

_PIPELINE_STAGES = [
    ("setup",                "🔧 Setup"),
    ("search",               "🔍 Busca"),
    ("screening",            "🧬 Triagem LLM"),
    ("comparative_analysis", "📊 Análise Comparativa"),
    ("whitespace_analysis",  "🗺️ Whitespace"),
    ("reporting",            "📄 Relatório"),
]
_STAGE_KEYS = [k for k, _ in _PIPELINE_STAGES]

_ARTICLE_STAGES = [
    ("article_analysis", "🧠 Análise do Artigo"),
    ("search",           "🔍 Busca de Patentes"),
    ("extraction",       "🔬 Extração de Pontos"),
    ("whitespace",       "📊 Confronto / Whitespace"),
]
_ARTICLE_STAGE_KEYS = [k for k, _ in _ARTICLE_STAGES]

DECISION_ICON = {"include": "🟢", "review": "🟡", "exclude": "🔴"}
SOURCE_ICON = {"GooglePatents": "🔍", "Patentscope": "🌐", "EPO": "🇪🇺"}

CLAIM_STATUS_BADGE = {
    "whitespace": "🔴 Whitespace",
    "partial":    "🟡 Parcial",
    "covered":    "🟢 Coberto",
}

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------

with st.sidebar:
    st.title("🔬 Patentes")

    mode = st.radio(
        "Modo",
        options=["Busca por Query", "Análise de Artigo"],
        index=0 if st.session_state.mode == "query" else 1,
        horizontal=True,
    )
    st.session_state.mode = "query" if mode == "Busca por Query" else "article"

    st.divider()

    if st.session_state.mode == "query":
        # ── Configuração de busca por query ──────────────────────────────────
        st.subheader("Nova busca")

        query = st.text_input(
            "Query *",
            placeholder="carbon dioxide thermal energy storage",
            disabled=st.session_state.running,
        )

        available_models = _fetch_models()
        default_idx = (
            available_models.index(_DEFAULT_MODEL)
            if _DEFAULT_MODEL in available_models
            else 0
        )

        ca, cb = st.columns(2)
        max_results = ca.number_input(
            "Máx. resultados", min_value=1, max_value=50,
            value=10, disabled=st.session_state.running,
        )
        model = cb.selectbox(
            "Modelo", options=available_models,
            index=default_idx, disabled=st.session_state.running,
        )

        with st.expander("Thresholds LLM"):
            cc, cd = st.columns(2)
            include_threshold = cc.number_input(
                "Incluir ≥", min_value=0.0, max_value=10.0,
                value=7.0, step=0.5, disabled=st.session_state.running,
            )
            review_threshold = cd.number_input(
                "Revisão ≥", min_value=0.0, max_value=10.0,
                value=4.5, step=0.5, disabled=st.session_state.running,
            )

        with st.expander("Features"):
            require_evidence   = st.checkbox("Evidências textuais",   value=True,  disabled=st.session_state.running)
            enable_clusters    = st.checkbox("Clusters temáticos",    value=True,  disabled=st.session_state.running)
            enable_struct      = st.checkbox("Papéis estruturais",    value=True,  disabled=st.session_state.running)
            enable_rerank      = st.checkbox("Rerank",                value=True,  disabled=st.session_state.running)
            enable_prisma      = st.checkbox("PRISMA",                value=True,  disabled=st.session_state.running)
            enable_snapshot    = st.checkbox("Snapshot",              value=True,  disabled=st.session_state.running)
            enable_comparative = st.checkbox("Análise comparativa",   value=True,  disabled=st.session_state.running)
            enable_whitespace  = st.checkbox("Whitespace analysis",   value=True,  disabled=st.session_state.running)
            enable_manual_rev  = st.checkbox("Fila revisão manual",   value=True,  disabled=st.session_state.running)

        with st.expander("💡 Whitespace por Inovação (opcional)"):
            query_innovation = st.text_area(
                "Descreva sua inovação",
                height=100,
                placeholder="Descreva brevemente o que é novo na sua pesquisa. Quando preenchido, o sistema usa o pipeline de claims + confronto para identificar whitespace real.",
                disabled=st.session_state.running or st.session_state.article_running,
            )

        run_btn = st.button(
            "🚀 Iniciar Análise", type="primary",
            use_container_width=True,
            disabled=st.session_state.running or st.session_state.article_running or not query,
        )

        # ── Histórico de runs ──────────────────────────────────────────────
        st.divider()
        st.subheader("Histórico")
        past_runs = _fetch_runs()
        for run in past_runs[:8]:
            rid = run["run_id"]
            status = run.get("status", "")
            icon = "✅" if status == "completed" else ("⏳" if status == "running" else "❌")
            label = f"{icon} {rid[9:]} — {run.get('query','')[:22]}"
            if st.button(label, key=f"hist_{rid}", use_container_width=True):
                data = _poll_run(rid)
                if data:
                    st.session_state.run_data = data
                    st.session_state.run_id = rid
                    st.session_state.running = False
                    st.session_state.error = None
                    st.rerun()

    else:
        # ── Análise de Artigo ─────────────────────────────────────────────
        st.subheader("Novo artigo")

        uploaded_file = st.file_uploader(
            "Upload do artigo (PDF ou TXT)",
            type=["pdf", "txt"],
            disabled=st.session_state.article_running,
            help="Carregue o PDF ou TXT do artigo alvo",
        )

        article_text_pasted = st.text_area(
            "— ou cole o texto do artigo —",
            height=120,
            placeholder="Abstract e texto principal do artigo...",
            disabled=st.session_state.article_running,
        )

        innovation_desc = st.text_area(
            "Descrição da inovação *",
            height=80,
            placeholder="Descreva brevemente o que é novo neste artigo...",
            disabled=st.session_state.article_running,
        )

        available_models = _fetch_models()
        with st.expander("Modelos LLM"):
            analysis_model_idx = (
                available_models.index(_DEFAULT_MODEL)
                if _DEFAULT_MODEL in available_models else 0
            )
            analysis_model = st.selectbox(
                "Modelo de análise (forte, 27B)",
                options=available_models,
                index=analysis_model_idx,
                disabled=st.session_state.article_running,
                help="Usado para analisar o artigo e gerar a narrativa de whitespace",
            )
            extract_model_opts = available_models
            extract_model_idx = (
                available_models.index(_DEFAULT_EXTRACT_MODEL)
                if _DEFAULT_EXTRACT_MODEL in available_models else 0
            )
            extraction_model = st.selectbox(
                "Modelo de extração (médio, 12B)",
                options=extract_model_opts,
                index=extract_model_idx,
                disabled=st.session_state.article_running,
                help="Usado para extrair pontos técnicos de cada patente encontrada",
            )

        with st.expander("Parâmetros de busca"):
            qa, qb = st.columns(2)
            max_results_per_query = qa.number_input(
                "Patentes/query", min_value=1, max_value=20,
                value=5, disabled=st.session_state.article_running,
            )
            max_queries = qb.number_input(
                "Máx. queries", min_value=1, max_value=8,
                value=4, disabled=st.session_state.article_running,
            )

        article_btn = st.button(
            "🧬 Analisar Artigo", type="primary",
            use_container_width=True,
            disabled=st.session_state.article_running or not innovation_desc,
        )

# ---------------------------------------------------------------------------
# Handle run button — Query mode
# ---------------------------------------------------------------------------

if st.session_state.mode == "query" and run_btn and query:
    if query_innovation and query_innovation.strip():
        # Rota: pipeline de artigo com query do usuário
        run_id = _start_article_run({
            "article_text": "",
            "innovation_description": query_innovation.strip(),
            "analysis_model": model,
            "extraction_model": _DEFAULT_EXTRACT_MODEL,
            "max_results_per_query": min(int(max_results), 20),
            "max_queries": 1,
            "user_queries": [query],
        })
        if run_id:
            st.session_state.article_run_id = run_id
            st.session_state.article_running = True
            st.session_state.article_run_data = None
            st.session_state.article_live_data = {}
            st.session_state.article_error = None
            st.session_state.run_data = None
            st.session_state.error = None
    else:
        # Rota: pipeline de query padrão
        run_id = _start_run({
            "query": query,
            "max_results": max_results,
            "model": model,
            "include_threshold": include_threshold,
            "review_threshold": review_threshold,
            "features": {
                "require_evidence":            require_evidence,
                "enable_thematic_clusters":    enable_clusters,
                "enable_structural_roles":     enable_struct,
                "enable_screening_rerank":     enable_rerank,
                "enable_prisma":               enable_prisma,
                "enable_snapshot":             enable_snapshot,
                "enable_comparative_analysis": enable_comparative,
                "enable_whitespace_analysis":  enable_whitespace,
                "enable_manual_review_queue":  enable_manual_rev,
            },
        })
        if run_id:
            st.session_state.run_id = run_id
            st.session_state.running = True
            st.session_state.run_data = None
            st.session_state.live_data = {}
            st.session_state.error = None
            st.session_state.article_run_data = None
            st.session_state.article_error = None
    st.rerun()

# ---------------------------------------------------------------------------
# Handle run button — Article mode
# ---------------------------------------------------------------------------

if st.session_state.mode == "article" and article_btn and innovation_desc:
    # Extract article text
    article_text = ""
    if uploaded_file is not None:
        if uploaded_file.name.endswith(".pdf"):
            try:
                import pypdf
                reader = pypdf.PdfReader(io.BytesIO(uploaded_file.read()))
                article_text = "\n".join(
                    page.extract_text() or "" for page in reader.pages
                )
            except Exception as exc:
                st.session_state.article_error = f"Erro ao ler PDF: {exc}"
        else:
            article_text = uploaded_file.read().decode("utf-8", errors="replace")
    elif article_text_pasted.strip():
        article_text = article_text_pasted.strip()

    if not article_text.strip():
        st.session_state.article_error = "Forneça o texto do artigo (upload ou cole o texto)."
    else:
        run_id = _start_article_run({
            "article_text": article_text,
            "innovation_description": innovation_desc,
            "analysis_model": analysis_model,
            "extraction_model": extraction_model,
            "max_results_per_query": int(max_results_per_query),
            "max_queries": int(max_queries),
        })
        if run_id:
            st.session_state.article_run_id = run_id
            st.session_state.article_running = True
            st.session_state.article_run_data = None
            st.session_state.article_live_data = {}
            st.session_state.article_error = None
    st.rerun()

# ---------------------------------------------------------------------------
# Poll while running — Query mode
# ---------------------------------------------------------------------------

if st.session_state.mode == "query" and st.session_state.running and st.session_state.run_id:
    live = _poll_run(st.session_state.run_id)
    if live:
        st.session_state.live_data = live
        status = live.get("status", "running")
        if status == "error":
            st.session_state.running = False
            st.session_state.error = live.get("error", "Erro desconhecido")
        elif status not in ("queued", "running"):
            st.session_state.running = False
            st.session_state.run_data = live
    else:
        st.session_state.error = "Sem resposta da API."
        st.session_state.running = False

# ---------------------------------------------------------------------------
# Poll while running — Article mode
# ---------------------------------------------------------------------------

if st.session_state.article_running and st.session_state.article_run_id:
    live = _poll_article_run(st.session_state.article_run_id)
    if live:
        st.session_state.article_live_data = live
        status = live.get("status", "running")
        if status == "error":
            st.session_state.article_running = False
            st.session_state.article_error = live.get("error", "Erro desconhecido")
        elif status not in ("queued", "running"):
            st.session_state.article_running = False
            st.session_state.article_run_data = live
    else:
        st.session_state.article_error = "Sem resposta da API."
        st.session_state.article_running = False

# ---------------------------------------------------------------------------
# Progress — Query mode
# ---------------------------------------------------------------------------

def _render_progress(live: dict) -> None:
    patents        = live.get("patents", [])
    cm             = live.get("coverage_metrics", {})
    stage_metrics  = live.get("stage_metrics", [])
    current_stage  = live.get("current_stage", "")
    screened_count = live.get("screened_count", 0)
    max_res        = live.get("max_results", 1)
    total_patents  = len(patents) or max_res

    completed = {m["stage"] for m in stage_metrics}
    n_done = sum(1 for k in _STAGE_KEYS if k in completed)

    if current_stage in _STAGE_KEYS and current_stage not in completed:
        partial = (screened_count / total_patents) if (current_stage == "screening" and total_patents) else 0.4
        prog = (n_done + partial) / len(_PIPELINE_STAGES)
    else:
        prog = n_done / len(_PIPELINE_STAGES)

    st.progress(min(prog, 1.0))
    cur_label = next((lbl for k, lbl in _PIPELINE_STAGES if k == current_stage), "Inicializando…")
    pct = int(min(prog, 1.0) * 100)
    st.markdown(f"**{pct}%** — etapa atual: **{cur_label}**")
    st.divider()

    stage_map = {m["stage"]: m for m in stage_metrics}
    for key, label in _PIPELINE_STAGES:
        if key in completed:
            m = stage_map[key]
            st.markdown(
                f"✅ **{label}** &nbsp; `{m.get('detail','')[:55]}` "
                f"*{m.get('duration_seconds', 0):.1f}s*"
            )
        elif key == current_stage:
            if key == "screening" and total_patents:
                pct_screen = int(screened_count / total_patents * 100)
                st.markdown(f"⏳ **{label}** — {screened_count}/{total_patents} triadas ({pct_screen}%)")
            else:
                st.markdown(f"⏳ **{label}** — em andamento…")
        else:
            st.markdown(f"<span style='color:gray'>⌛ {label}</span>", unsafe_allow_html=True)

    st.divider()

    by_source = live.get("patents_by_source", {})
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Coletadas", len(patents) or "—")
    c2.metric("Triadas",   screened_count or cm.get("screened", "—"))
    c3.metric("Incluídas", cm.get("included", "—"))
    c4.metric("Em revisão", cm.get("review", "—"))

    if by_source:
        st.caption("Por fonte: " + " &nbsp;·&nbsp; ".join(
            f"{SOURCE_ICON.get(src, '📄')} **{src}** {n}"
            for src, n in by_source.items()
        ))

# ---------------------------------------------------------------------------
# Progress — Article mode
# ---------------------------------------------------------------------------

def _render_article_progress(live: dict) -> None:
    stage_metrics  = live.get("stage_metrics", [])
    current_stage  = live.get("current_stage", "")
    extracted_count = live.get("extracted_count", 0)
    total_patents   = len(live.get("patents", [])) or 1

    completed = {m["stage"] for m in stage_metrics}
    n_done = sum(1 for k in _ARTICLE_STAGE_KEYS if k in completed)

    if current_stage in _ARTICLE_STAGE_KEYS and current_stage not in completed:
        if current_stage == "extraction" and total_patents:
            partial = extracted_count / total_patents
        else:
            partial = 0.4
        prog = (n_done + partial) / len(_ARTICLE_STAGES)
    else:
        prog = n_done / len(_ARTICLE_STAGES)

    st.progress(min(prog, 1.0))
    cur_label = next((lbl for k, lbl in _ARTICLE_STAGES if k == current_stage), "Inicializando…")
    pct = int(min(prog, 1.0) * 100)
    st.markdown(f"**{pct}%** — etapa atual: **{cur_label}**")
    st.divider()

    stage_map = {m["stage"]: m for m in stage_metrics}
    for key, label in _ARTICLE_STAGES:
        if key in completed:
            m = stage_map[key]
            st.markdown(
                f"✅ **{label}** &nbsp; `{m.get('detail','')[:60]}` "
                f"*{m.get('duration_seconds', 0):.1f}s*"
            )
        elif key == current_stage:
            if key == "extraction" and total_patents:
                pct_ext = int(extracted_count / total_patents * 100)
                st.markdown(f"⏳ **{label}** — {extracted_count}/{total_patents} ({pct_ext}%)")
            else:
                st.markdown(f"⏳ **{label}** — em andamento…")
        else:
            st.markdown(f"<span style='color:gray'>⌛ {label}</span>", unsafe_allow_html=True)

    st.divider()
    by_source = live.get("patents_by_source", {})
    if by_source:
        st.caption("Por fonte: " + " &nbsp;·&nbsp; ".join(
            f"{SOURCE_ICON.get(src, '📄')} **{src}** {n}"
            for src, n in by_source.items()
        ))

    analysis = live.get("article_analysis")
    if analysis:
        st.markdown(f"**Artigo:** {analysis.get('article_title','—')}")
        queries = analysis.get("search_queries", [])
        if queries:
            st.caption("Queries geradas: " + " · ".join(f"`{q}`" for q in queries))

# ---------------------------------------------------------------------------
# Results helpers — Query mode
# ---------------------------------------------------------------------------

def _icon(decision: str) -> str:
    return DECISION_ICON.get((decision or "").lower(), "⚪")


def _build_df(patents: list, evaluations: list) -> pd.DataFrame:
    by_rec = {e.get("record_id", ""): e for e in evaluations}
    rows = []
    for p in patents:
        rid = p.get("record_id", "")
        ev  = by_rec.get(rid, {})
        dec = ev.get("screening_decision", "")
        rows.append({
            "Decisão":  f"{_icon(dec)} {dec}",
            "_dec":     dec,
            "Score":    ev.get("screening_score") or ev.get("relevance_score") or 0.0,
            "Título":   p.get("title", ""),
            "ID":       p.get("patent_id") or rid,
            "Assignee": p.get("assignee", ""),
            "Data":     p.get("publication_date", ""),
            "Fonte":    p.get("source", ""),
            "Cluster":  ev.get("thematic_cluster", ""),
            "Domínio":  ev.get("technical_domain", ""),
            "Inovação": ev.get("innovation_level", ""),
            "Conf.":    ev.get("confidence", 0.0),
            "_record_id": rid,
            "_patent":  p,
            "_eval":    ev,
        })
    return pd.DataFrame(rows)


def _patent_card(patent: dict, ev: dict) -> None:
    dec   = ev.get("screening_decision", "")
    score = ev.get("relevance_score") or ev.get("screening_score") or 0.0

    col_main, col_meta = st.columns([3, 1])

    with col_main:
        if patent.get("abstract"):
            st.markdown("**Resumo**")
            st.write(patent["abstract"])
        elif patent.get("snippet"):
            st.write(patent["snippet"])

        if ev.get("summary"):
            st.markdown("**Avaliação LLM**")
            st.write(ev["summary"])

        if ev.get("key_findings"):
            st.markdown("**Achados-chave**")
            for kf in ev["key_findings"]:
                st.markdown(f"- {kf}")

        cols_ev = []
        if ev.get("problem_statement"):
            cols_ev.append(("Problema", ev["problem_statement"]))
        if ev.get("solution_summary"):
            cols_ev.append(("Solução", ev["solution_summary"]))
        if cols_ev:
            for label, text in cols_ev:
                with st.expander(label):
                    st.write(text)

        if ev.get("evidence_snippets"):
            with st.expander(f"Evidências ({len(ev['evidence_snippets'])})"):
                for snip in ev["evidence_snippets"]:
                    st.markdown(f"> {snip}")

        if ev.get("claimed_advantages"):
            with st.expander("Vantagens declaradas"):
                for adv in ev["claimed_advantages"]:
                    st.markdown(f"- {adv}")

    with col_meta:
        st.markdown(f"**Score:** `{score:.1f}`")
        st.markdown(f"**Decisão:** {_icon(dec)} `{dec}`")
        for lbl, val in [
            ("ID",         patent.get("patent_id", "—")),
            ("Assignee",   patent.get("assignee", "—")),
            ("Depósito",   patent.get("filing_date", "—")),
            ("Publicação", patent.get("publication_date", "—")),
            ("Fonte",      patent.get("source", "—")),
        ]:
            st.markdown(f"**{lbl}:** {val}")

        inventors = (patent.get("inventors") or [])[:3]
        if inventors:
            st.markdown(f"**Inventores:** {', '.join(inventors)}")

        for lbl, val in [
            ("Cluster",    ev.get("thematic_cluster")),
            ("Domínio",    ev.get("technical_domain")),
            ("Inovação",   ev.get("innovation_level")),
            ("Maturidade", ev.get("maturity_level")),
            ("Confiança",  f"{ev.get('confidence', 0):.2f}" if ev.get("confidence") else None),
        ]:
            if val:
                st.markdown(f"**{lbl}:** {val}")

        if patent.get("url"):
            st.link_button("Abrir patente ↗", patent["url"])

    if ev.get("screening_reason"):
        st.caption(f"*Motivo: {ev['screening_reason']}*")
    if ev.get("llm_error"):
        st.warning(f"Erro LLM: {ev['llm_error']}")


def _render_metrics(cm: dict, by_source: dict, dur: Optional[float], run_id: str) -> None:
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("Coletadas (raw)", cm.get("raw_scraped",      "—"))
    c2.metric("Únicas",          cm.get("unique_patents",    "—"))
    c3.metric("Triadas",         cm.get("screened",          "—"))
    c4.metric("Incluídas",       cm.get("included",          "—"))
    c5.metric("Em revisão",      cm.get("review",            "—"))
    c6.metric("Excluídas",       cm.get("excluded",          "—"))

    c7, c8, c9, c10 = st.columns(4)
    c7.metric("Duplicatas",        cm.get("duplicates_removed", "—"))
    c8.metric("Extração completa", cm.get("full_extractions",   "—"))
    c9.metric("Revisão manual",    cm.get("manual_review_required", "—"))
    c10.metric("Duração total",    f"{dur:.0f}s" if dur else "—")

    if by_source:
        parts = [
            f"{SOURCE_ICON.get(src,'📄')} **{src}** {n}"
            for src, n in by_source.items()
        ]
        st.caption("Fontes: " + " &nbsp;·&nbsp; ".join(parts))


def _render_patents_tab(patents: list, evaluations: list, manual_review: list) -> None:
    df = _build_df(patents, evaluations)
    if df.empty:
        st.info("Nenhuma patente encontrada.")
        return

    f1, f2, f3 = st.columns([2, 2, 1])
    with f1:
        all_decisions = ["include", "review", "exclude"]
        selected_dec = st.multiselect(
            "Filtrar por decisão",
            options=all_decisions,
            default=all_decisions,
            format_func=lambda d: f"{_icon(d)} {d}",
        )
    with f2:
        all_sources = sorted(df["Fonte"].unique().tolist())
        selected_src = st.multiselect("Filtrar por fonte", options=all_sources, default=all_sources)
    with f3:
        sort_by = st.selectbox("Ordenar por", ["Score ↓", "Score ↑", "Data ↓", "Título"])

    mask = df["_dec"].isin(selected_dec if selected_dec else all_decisions)
    if selected_src:
        mask &= df["Fonte"].isin(selected_src)
    df_filt = df[mask].copy()

    if sort_by == "Score ↓":
        df_filt = df_filt.sort_values("Score", ascending=False)
    elif sort_by == "Score ↑":
        df_filt = df_filt.sort_values("Score", ascending=True)
    elif sort_by == "Data ↓":
        df_filt = df_filt.sort_values("Data", ascending=False)
    else:
        df_filt = df_filt.sort_values("Título")

    st.caption(f"{len(df_filt)} de {len(df)} patentes")

    display_cols = ["Decisão", "Score", "Título", "ID", "Assignee", "Data", "Fonte", "Cluster"]
    st.dataframe(
        df_filt[display_cols],
        hide_index=True,
        use_container_width=True,
        column_config={
            "Score":  st.column_config.NumberColumn(format="%.1f"),
            "Título": st.column_config.TextColumn(width="large"),
        },
    )

    if manual_review:
        with st.expander(f"📋 Fila de revisão manual ({len(manual_review)})"):
            for item in manual_review:
                st.markdown(
                    f"- **{item.get('title', item.get('patent_id','—'))}**"
                    f" — Score `{item.get('screening_score','—')}`"
                    f" — {item.get('reason','')}"
                )

    st.markdown("---")
    st.markdown("#### Detalhes")
    by_rec = {e.get("record_id", ""): e for e in evaluations}
    visible_ids = set(df_filt["_record_id"].tolist())
    for p in patents:
        rid = p.get("record_id", "")
        if rid not in visible_ids:
            continue
        ev    = by_rec.get(rid, {})
        title = p.get("title") or p.get("patent_id") or rid
        dec   = ev.get("screening_decision", "")
        with st.expander(f"{_icon(dec)} {title[:90]}"):
            _patent_card(p, ev)


def _render_clusters_tab(clusters_data: dict) -> None:
    clusters = clusters_data.get("clusters", [])
    if not clusters:
        st.info("Nenhum cluster temático.")
        return

    df = pd.DataFrame([
        {
            "Cluster":         c["cluster"],
            "Patentes":        c["count"],
            "Score médio":     round(c.get("average_score", 0), 2),
            "Confiança média": round(c.get("average_confidence", 0), 2),
            "Evidências":      c.get("evidence_count", 0),
        }
        for c in clusters
    ])

    fig = px.bar(
        df, x="Patentes", y="Cluster", orientation="h",
        color="Score médio", color_continuous_scale="Blues",
        text="Patentes",
        title=f"Clusters temáticos ({clusters_data.get('total_clusters', len(clusters))} total)",
    )
    fig.update_layout(yaxis={"categoryorder": "total ascending"}, height=max(300, len(clusters) * 45))
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(df, hide_index=True, use_container_width=True)


def _render_whitespace_tab(ws: dict) -> None:
    if not ws or ws.get("status") != "ok":
        st.info("Whitespace analysis não gerada.")
        return

    candidates = ws.get("whitespace_candidates", [])
    if candidates:
        st.markdown("#### Lacunas identificadas")
        for c in candidates:
            with st.expander(c.get("gap_label", "—")):
                st.write(c.get("rationale", ""))
                if c.get("suggested_queries"):
                    st.markdown("**Queries sugeridas:**")
                    for sq in c["suggested_queries"]:
                        st.code(sq)

    matrix = ws.get("coverage_matrix", [])
    if matrix:
        st.markdown("#### Matriz de cobertura")
        st.dataframe(pd.DataFrame(matrix), hide_index=True, use_container_width=True)

    corpus = ws.get("corpus_summary", {})
    if corpus:
        with st.expander("Sumário do corpus"):
            st.json(corpus)


def _render_prisma_tab(prisma: dict) -> None:
    flow = prisma.get("flow", {})
    if not flow:
        st.info("Dados PRISMA não disponíveis.")
        return

    ident  = flow.get("identification", {})
    screen = flow.get("screening", {})
    elig   = flow.get("eligibility", {})
    synth  = flow.get("synthesis", {})

    labels = ["Coletados", "Únicos", "Triados", "Incluídos + Revisão", "Síntese"]
    values = [
        ident.get("raw_records", 0),
        ident.get("unique_records", 0),
        screen.get("screened", 0),
        (screen.get("included", 0) or 0) + (screen.get("review", 0) or 0),
        synth.get("analyzed_records", 0),
    ]
    try:
        values = [int(v) for v in values]
        fig = go.Figure(go.Funnel(y=labels, x=values, textinfo="value+percent initial"))
        fig.update_layout(title="Fluxo PRISMA", height=320)
        st.plotly_chart(fig, use_container_width=True)
    except Exception:
        pass

    rows = [
        ("Identificação", "Registros brutos",       ident.get("raw_records",          "—")),
        ("Identificação", "Únicos após dedupe",      ident.get("unique_records",        "—")),
        ("Identificação", "Duplicatas removidas",    ident.get("duplicates_removed",    "—")),
        ("Triagem",       "Triados pelo LLM",        screen.get("screened",             "—")),
        ("Triagem",       "Incluídos",               screen.get("included",             "—")),
        ("Triagem",       "Em revisão",              screen.get("review",               "—")),
        ("Triagem",       "Excluídos",               screen.get("excluded",             "—")),
        ("Elegibilidade", "Extrações detalhadas",    elig.get("full_extractions",       "—")),
        ("Elegibilidade", "Revisão manual obrig.",   elig.get("manual_review_required", "—")),
        ("Síntese",       "Registros analisados",    synth.get("analyzed_records",      "—")),
        ("Síntese",       "Análise comparativa",     "Sim" if synth.get("comparative_analysis_generated") else "Não"),
    ]
    st.dataframe(
        pd.DataFrame(rows, columns=["Fase", "Etapa", "Valor"]),
        hide_index=True, use_container_width=True,
    )


def _render_exec_tab(d: dict) -> None:
    stage_metrics = d.get("stage_metrics", [])
    scraper_durs  = d.get("scraper_durations", {})
    llm_telemetry = d.get("llm_telemetry", {})
    obs           = d.get("observability_metrics", {})
    errors        = d.get("errors", [])

    if stage_metrics:
        st.markdown("#### Tempo por etapa")
        stage_labels = {k: lbl for k, lbl in _PIPELINE_STAGES}
        df_s = pd.DataFrame([
            {
                "Etapa":       stage_labels.get(m["stage"], m["stage"]),
                "Duração (s)": round(m.get("duration_seconds", 0), 1),
                "Status":      m.get("status", "ok"),
                "Detalhe":     m.get("detail", ""),
            }
            for m in stage_metrics if m.get("stage") in stage_labels
        ])
        if not df_s.empty:
            color_map = {"ok": "#2ecc71", "degraded": "#f39c12", "skipped": "#95a5a6", "disabled_or_skipped": "#95a5a6"}
            fig = px.bar(
                df_s, x="Duração (s)", y="Etapa", orientation="h",
                color="Status", color_discrete_map=color_map,
                text="Duração (s)", title="Duração das etapas",
            )
            fig.update_layout(yaxis={"categoryorder": "total ascending"}, height=300, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

    if scraper_durs:
        st.markdown("#### Scrapers")
        by_source = d.get("patents_by_source", {})
        rows_sc = []
        for src, dur in scraper_durs.items():
            rows_sc.append({
                "Fonte":     f"{SOURCE_ICON.get(src,'📄')} {src}",
                "Patentes":  by_source.get(src, "—"),
                "Tempo (s)": round(dur, 1),
            })
        st.dataframe(pd.DataFrame(rows_sc), hide_index=True, use_container_width=True)

    ops = llm_telemetry.get("operations", {})
    if ops:
        st.markdown("#### LLM Telemetria")
        rows_llm = []
        for op, stats in ops.items():
            rows_llm.append({
                "Operação":        op,
                "Chamadas":        stats.get("calls", 0),
                "Cache hits":      stats.get("cache_hits", 0),
                "Falhas":          stats.get("failures", 0),
                "Tempo total (s)": round(stats.get("total_duration_seconds", 0), 1),
            })
        st.dataframe(pd.DataFrame(rows_llm), hide_index=True, use_container_width=True)

    routes = obs.get("routes", {})
    if routes:
        st.markdown("#### Rotas de análise")
        route_counts = {k: v.get("count", 0) if isinstance(v, dict) else v for k, v in routes.items()}
        fig_r = px.pie(
            names=list(route_counts.keys()),
            values=list(route_counts.values()),
            title="Distribuição de rotas",
            hole=0.4,
        )
        fig_r.update_layout(height=280)
        st.plotly_chart(fig_r, use_container_width=True)

    diag = d.get("scraper_diagnostics", {})
    all_diags = [(src, e) for src, evts in diag.items() for e in evts]
    if all_diags:
        with st.expander(f"Diagnósticos de scraping ({len(all_diags)})"):
            for src, e in all_diags:
                st.markdown(f"**{src}** · `{e.get('kind','')}` — {e.get('detail','')}")
                if e.get("url"):
                    st.caption(e["url"])

    if errors:
        with st.expander(f"⚠️ {len(errors)} erro(s) de execução"):
            for err in errors:
                st.error(err)


def _render_files_tab(output_paths: dict) -> None:
    if not output_paths:
        st.info("Nenhum arquivo de saída.")
        return

    downloadable = {
        "markdown": ("⬇️ Relatório Markdown", "text/markdown"),
        "json":     ("⬇️ Relatório JSON",     "application/json"),
    }
    for key, (label, mime) in downloadable.items():
        path = output_paths.get(key, "")
        if path and os.path.isfile(path):
            with open(path, encoding="utf-8") as f:
                content = f.read()
            st.download_button(label, data=content, file_name=os.path.basename(path), mime=mime)

    st.markdown("#### Arquivos gerados")
    for label, path in output_paths.items():
        exists = os.path.isfile(path)
        icon = "✅" if exists else "❌"
        st.markdown(f"{icon} **{label}:** `{path}`")


def _render_results(d: dict) -> None:
    query_label  = d.get("query", "—")
    total_dur    = d.get("total_duration_seconds")
    patents      = d.get("patents", [])
    evaluations  = d.get("evaluations", [])
    cm           = d.get("coverage_metrics", {})
    by_source    = d.get("patents_by_source", {})
    clusters_data= d.get("thematic_clusters", {})
    comparative  = d.get("comparative_analysis", "")
    whitespace   = d.get("whitespace_analysis", {})
    prisma       = d.get("prisma_flow", {})
    output_paths = d.get("output_paths", {})
    manual_rev   = d.get("manual_review_queue", [])

    col_h, col_dl = st.columns([4, 1])
    with col_h:
        dur_str = f" · {total_dur:.0f}s" if total_dur else ""
        st.success(f"**{query_label}** — {len(patents)} patentes{dur_str}")
    with col_dl:
        md_path = output_paths.get("markdown", "")
        if md_path and os.path.isfile(md_path):
            with open(md_path, encoding="utf-8") as f:
                st.download_button(
                    "⬇️ Markdown", data=f.read(),
                    file_name=os.path.basename(md_path),
                    mime="text/markdown", use_container_width=True,
                )

    _render_metrics(cm, by_source, total_dur, d.get("run_id", ""))
    st.divider()

    tabs = st.tabs(["📋 Patentes", "🔵 Clusters", "📊 Comparativa", "🗺️ Whitespace", "📐 PRISMA", "⚙️ Execução", "💾 Arquivos"])

    with tabs[0]: _render_patents_tab(patents, evaluations, manual_rev)
    with tabs[1]: _render_clusters_tab(clusters_data)
    with tabs[2]:
        if comparative and comparative.strip() and not comparative.startswith("⚠️"):
            st.markdown(comparative)
        else:
            st.info(comparative or "Análise comparativa não gerada.")
    with tabs[3]: _render_whitespace_tab(whitespace)
    with tabs[4]: _render_prisma_tab(prisma)
    with tabs[5]: _render_exec_tab(d)
    with tabs[6]: _render_files_tab(output_paths)


# ---------------------------------------------------------------------------
# Results helpers — Article mode
# ---------------------------------------------------------------------------

def _render_claim_coverage(whitespace_report: dict) -> None:
    coverage = whitespace_report.get("claim_coverage", [])
    if not coverage:
        st.info("Dados de cobertura não disponíveis.")
        return

    ws_score = whitespace_report.get("whitespace_score", 0.0)
    ws_count = len(whitespace_report.get("whitespace_claims", []))
    total    = len(coverage)

    # Score indicator
    score_color = "#e74c3c" if ws_score >= 0.6 else ("#f39c12" if ws_score >= 0.3 else "#2ecc71")
    st.markdown(
        f"<div style='padding:12px;background:{score_color}22;border-left:4px solid {score_color};border-radius:4px;'>"
        f"<b>Score de whitespace: {ws_score*100:.0f}%</b> — "
        f"{ws_count} de {total} reivindicações sem cobertura em patentes existentes"
        f"</div>",
        unsafe_allow_html=True,
    )
    st.markdown("")

    for cov in coverage:
        status  = cov.get("status", "whitespace")
        badge   = CLAIM_STATUS_BADGE.get(status, "⚪")
        claim_id = cov.get("claim_id", "?")
        text    = cov.get("claim_text", "")
        covering = cov.get("covering_patents", [])
        partial  = cov.get("partial_patents", [])

        with st.expander(f"{badge} — Reivindicação {claim_id}: {text[:80]}{'…' if len(text) > 80 else ''}"):
            st.write(text)
            if covering:
                st.markdown(f"**Coberto por ({len(covering)} patente{'s' if len(covering)>1 else ''}):**")
                for pid in covering[:5]:
                    st.markdown(f"  - `{pid}`")
            if partial:
                st.markdown("**Cobertura parcial:**")
                for pp in partial[:4]:
                    aspect = pp.get("aspect", "")
                    st.markdown(f"  - `{pp.get('patent_id', '?')}` — {aspect}")
            if not covering and not partial:
                st.markdown("*Nenhuma patente encontrada cobre esta reivindicação.*")


def _render_article_patents_tab(patents: list, extractions: list) -> None:
    if not patents:
        st.info(
            "Nenhuma patente encontrada para as queries geradas.\n\n"
            "Isso indica que a área de inovação pode não ter prior art em patentes — "
            "todas as reivindicações aparecem como **whitespace**."
        )
        return

    ext_by_id = {e.get("record_id", ""): e for e in extractions}

    rows = []
    for p in patents:
        rid = p.get("record_id", "")
        ext = ext_by_id.get(rid, {})
        covers = ext.get("covers_claims", [])
        similarity = ext.get("similarity", "—")
        sim_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(similarity, "⚪")
        rows.append({
            "Sim.":     f"{sim_icon} {similarity}",
            "Claims cobertos": str(covers) if covers else "—",
            "Título":   p.get("title", ""),
            "ID":       p.get("patent_id") or rid,
            "Fonte":    p.get("source", ""),
            "_rid":     rid,
        })

    df = pd.DataFrame(rows)
    st.caption(f"{len(df)} patentes encontradas")
    st.dataframe(
        df[["Sim.", "Claims cobertos", "Título", "ID", "Fonte"]],
        hide_index=True,
        use_container_width=True,
        column_config={"Título": st.column_config.TextColumn(width="large")},
    )

    st.markdown("---")
    st.markdown("#### Detalhes das patentes")
    for p in patents:
        rid = p.get("record_id", "")
        ext = ext_by_id.get(rid, {})
        title = p.get("title") or p.get("patent_id") or rid
        with st.expander(f"{title[:90]}"):
            col_main, col_meta = st.columns([3, 1])
            with col_main:
                if p.get("abstract"):
                    st.markdown("**Resumo**")
                    st.write(p["abstract"][:800])
                elif p.get("snippet"):
                    st.write(p["snippet"][:400])
                if ext.get("core_contribution"):
                    st.markdown("**Contribuição central (extraída pelo LLM)**")
                    st.write(ext["core_contribution"])
                if ext.get("distinguishing_factors"):
                    st.markdown("**Diferenças em relação ao artigo alvo**")
                    st.write(ext["distinguishing_factors"])
                covers = ext.get("covers_claims", [])
                partial = ext.get("partial_coverage", [])
                if covers:
                    st.markdown(f"**Cobre reivindicações:** {covers}")
                if partial:
                    st.markdown("**Cobertura parcial:**")
                    for pp in partial:
                        st.markdown(f"- Reivindicação {pp.get('claim_id','?')}: {pp.get('aspect','')}")
            with col_meta:
                sim = ext.get("similarity", "—")
                st.markdown(f"**Similaridade:** `{sim}`")
                for lbl, val in [
                    ("ID",         p.get("patent_id", "—")),
                    ("Assignee",   p.get("assignee", "—")),
                    ("Publicação", p.get("publication_date", "—")),
                    ("Fonte",      p.get("source", "—")),
                ]:
                    st.markdown(f"**{lbl}:** {val}")
                if p.get("url"):
                    st.link_button("Abrir patente ↗", p["url"])


def _render_article_exec_tab(d: dict) -> None:
    stage_metrics = d.get("stage_metrics", [])
    errors        = d.get("errors", [])
    by_source     = d.get("patents_by_source", {})

    if stage_metrics:
        st.markdown("#### Tempo por etapa")
        stage_labels = {k: lbl for k, lbl in _ARTICLE_STAGES}
        df_s = pd.DataFrame([
            {
                "Etapa":       stage_labels.get(m["stage"], m["stage"]),
                "Duração (s)": round(m.get("duration_seconds", 0), 1),
                "Status":      m.get("status", "ok"),
                "Detalhe":     m.get("detail", ""),
            }
            for m in stage_metrics
        ])
        if not df_s.empty:
            color_map = {"ok": "#2ecc71", "error": "#e74c3c", "empty": "#f39c12"}
            fig = px.bar(
                df_s, x="Duração (s)", y="Etapa", orientation="h",
                color="Status", color_discrete_map=color_map,
                text="Duração (s)", title="Duração das etapas",
            )
            fig.update_layout(yaxis={"categoryorder": "total ascending"}, height=280, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

    if by_source:
        st.markdown("#### Patentes por fonte")
        rows_src = [
            {"Fonte": f"{SOURCE_ICON.get(s, '📄')} {s}", "Patentes": n}
            for s, n in by_source.items()
        ]
        st.dataframe(pd.DataFrame(rows_src), hide_index=True, use_container_width=True)

    analysis = d.get("article_analysis")
    if analysis:
        st.markdown("#### Análise do artigo (LLM)")
        st.markdown(f"**Título:** {analysis.get('article_title','—')}")
        st.markdown(f"**Inovação central:** {analysis.get('core_innovation','—')}")
        st.markdown(f"**Hipótese de novidade:** {analysis.get('novelty_hypothesis','—')}")

        queries = analysis.get("search_queries", [])
        if queries:
            st.markdown("**Queries geradas:**")
            for q in queries:
                st.code(q)

        dims = analysis.get("technical_dimensions", [])
        if dims:
            st.markdown("**Dimensões técnicas:** " + " · ".join(f"`{d}`" for d in dims))

    if errors:
        with st.expander(f"⚠️ {len(errors)} erro(s) de execução"):
            for err in errors:
                st.error(err)


def _render_article_results(d: dict) -> None:
    article_title = d.get("article_title", "—")
    total_dur     = d.get("total_duration_seconds")
    patents       = d.get("patents", [])
    extractions   = d.get("patent_extractions", [])
    whitespace    = d.get("whitespace_report", {})
    by_source     = d.get("patents_by_source", {})

    # Header
    dur_str = f" · {total_dur:.0f}s" if total_dur else ""
    ws_score = (whitespace or {}).get("whitespace_score", None)
    ws_str = f" · whitespace {ws_score*100:.0f}%" if ws_score is not None else ""
    patent_str = f"{len(patents)} patentes" if patents else "0 patentes (whitespace total)"
    st.success(f"**{article_title}** — {patent_str}{ws_str}{dur_str}")

    # Source breakdown
    if by_source:
        parts = [
            f"{SOURCE_ICON.get(src,'📄')} **{src}** {n}"
            for src, n in by_source.items()
        ]
        st.caption("Fontes: " + " &nbsp;·&nbsp; ".join(parts))

    st.divider()

    tabs = st.tabs(["📊 Whitespace", "📋 Patentes", "⚙️ Execução"])

    with tabs[0]:
        if whitespace and whitespace.get("status") == "ok":
            # Narrative
            narrative = whitespace.get("narrative", "")
            if narrative:
                st.markdown("#### Narrativa")
                st.markdown(narrative)
                st.divider()

            # Claim coverage
            st.markdown("#### Cobertura das Reivindicações")
            _render_claim_coverage(whitespace)

            # Recommended queries
            rec_queries = whitespace.get("recommended_queries", [])
            if rec_queries:
                st.divider()
                st.markdown("#### Queries para aprofundar busca nos gaps")
                for q in rec_queries:
                    st.code(q)
        else:
            st.info("Análise de whitespace não disponível.")

    with tabs[1]:
        _render_article_patents_tab(patents, extractions)

    with tabs[2]:
        _render_article_exec_tab(d)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

st.title("🔬 Revisão Técnica de Patentes")

mode = st.session_state.mode

if mode == "query":
    if st.session_state.running:
        live = st.session_state.live_data
        with st.status("⏳ Executando pipeline…", expanded=True, state="running"):
            if live and live.get("current_stage"):
                _render_progress(live)
            else:
                st.write("Inicializando…")
        time.sleep(_POLL_INTERVAL)
        st.rerun()

    elif st.session_state.article_running:
        live = st.session_state.article_live_data
        with st.status("⏳ Analisando whitespace por inovação…", expanded=True, state="running"):
            if live and live.get("current_stage"):
                _render_article_progress(live)
            else:
                st.write("Inicializando análise de inovação…")
        time.sleep(_POLL_INTERVAL)
        st.rerun()

    elif st.session_state.error:
        st.error(f"Erro: {st.session_state.error}")
        if st.button("Limpar"):
            st.session_state.error = None
            st.rerun()

    elif st.session_state.article_error:
        st.error(f"Erro: {st.session_state.article_error}")
        if st.button("Limpar"):
            st.session_state.article_error = None
            st.rerun()

    elif st.session_state.article_run_data is not None:
        _render_article_results(st.session_state.article_run_data)

    elif st.session_state.run_data is not None:
        _render_results(st.session_state.run_data)

    else:
        st.info(
            "Configure a busca no painel lateral e clique em **🚀 Iniciar Análise**.\n\n"
            "Fontes: Google Patents · Patentscope · EPO Open Patent Services"
        )

else:  # article mode
    if st.session_state.article_running:
        live = st.session_state.article_live_data
        with st.status("⏳ Analisando artigo…", expanded=True, state="running"):
            if live and live.get("current_stage"):
                _render_article_progress(live)
            else:
                st.write("Inicializando análise de artigo…")
        time.sleep(_POLL_INTERVAL)
        st.rerun()

    elif st.session_state.article_error:
        st.error(f"Erro: {st.session_state.article_error}")
        if st.button("Limpar"):
            st.session_state.article_error = None
            st.rerun()

    elif st.session_state.article_run_data is not None:
        _render_article_results(st.session_state.article_run_data)

    else:
        st.info(
            "**Modo: Análise de Artigo**\n\n"
            "Faça upload do artigo (PDF ou TXT) ou cole o texto, forneça a descrição da inovação "
            "e clique em **🧬 Analisar Artigo**.\n\n"
            "O sistema irá:\n"
            "1. 🧠 Analisar o artigo e extrair reivindicações técnicas (LLM 27B)\n"
            "2. 🔍 Buscar patentes relevantes nas 3 fontes\n"
            "3. 🔬 Extrair pontos técnicos de cada patente (LLM 12B)\n"
            "4. 📊 Identificar whitespace: o que você propõe que ainda não existe em patentes"
        )
