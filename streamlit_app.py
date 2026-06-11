"""
Interface Streamlit para o pipeline de Revisão Técnica de Patentes.
Comunica-se com o backend via REST API.
"""

import os
import time

import pandas as pd
import plotly.express as px
import requests
import streamlit as st

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

_DEFAULT_MODEL = os.getenv("OLLAMA_MODEL", "gemma3:27b")
_DEFAULT_MAX_RESULTS = 10
_DEFAULT_INCLUDE_THRESHOLD = 7.0
_DEFAULT_REVIEW_THRESHOLD = 4.5

st.set_page_config(
    page_title="Revisão Técnica de Patentes",
    page_icon="🔬",
    layout="wide",
)

# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------
_DEFAULTS = {
    "running": False,
    "run_id": None,
    "run_data": None,
    "live_data": {},
    "error": None,
}
for _k, _v in _DEFAULTS.items():
    if _k not in st.session_state:
        st.session_state[_k] = _v

# ---------------------------------------------------------------------------
# Sidebar — configuração
# ---------------------------------------------------------------------------
with st.sidebar:
    st.title("⚙️ Configurações")

    query = st.text_input(
        "Query *",
        placeholder="carbon dioxide thermal energy storage",
        disabled=st.session_state.running,
    )

    @st.cache_data(ttl=60)
    def _fetch_models() -> list[str]:
        try:
            resp = requests.get(f"{API_BASE_URL}/models", timeout=5)
            return resp.json().get("models", [_DEFAULT_MODEL]) if resp.ok else [_DEFAULT_MODEL]
        except Exception:
            return [_DEFAULT_MODEL]

    available_models = _fetch_models()
    default_index = available_models.index(_DEFAULT_MODEL) if _DEFAULT_MODEL in available_models else 0

    col_a, col_b = st.columns(2)
    max_results = col_a.number_input(
        "Máx. resultados",
        min_value=1,
        max_value=50,
        value=_DEFAULT_MAX_RESULTS,
        disabled=st.session_state.running,
    )
    model = col_b.selectbox(
        "Modelo Ollama",
        options=available_models,
        index=default_index,
        disabled=st.session_state.running,
    )

    col_c, col_d = st.columns(2)
    include_threshold = col_c.number_input(
        "Threshold inclusão",
        min_value=0.0,
        max_value=10.0,
        value=_DEFAULT_INCLUDE_THRESHOLD,
        step=0.5,
        disabled=st.session_state.running,
    )
    review_threshold = col_d.number_input(
        "Threshold revisão",
        min_value=0.0,
        max_value=10.0,
        value=_DEFAULT_REVIEW_THRESHOLD,
        step=0.5,
        disabled=st.session_state.running,
    )

    with st.expander("Feature Flags", expanded=False):
        require_evidence = st.checkbox(
            "Exigir evidências textuais", value=True, disabled=st.session_state.running
        )
        enable_clusters = st.checkbox(
            "Clusters temáticos", value=True, disabled=st.session_state.running
        )
        enable_structural_roles = st.checkbox(
            "Papéis estruturais (CO₂/storage)", value=True, disabled=st.session_state.running
        )
        enable_rerank = st.checkbox(
            "Re-triagem (rerank)", value=True, disabled=st.session_state.running
        )
        enable_prisma = st.checkbox(
            "Artefatos PRISMA", value=True, disabled=st.session_state.running
        )
        enable_snapshot = st.checkbox(
            "Snapshot de execução", value=True, disabled=st.session_state.running
        )
        enable_comparative = st.checkbox(
            "Análise comparativa", value=True, disabled=st.session_state.running
        )
        enable_whitespace = st.checkbox(
            "Whitespace analysis", value=True, disabled=st.session_state.running
        )
        enable_manual_review = st.checkbox(
            "Fila de revisão manual", value=True, disabled=st.session_state.running
        )

    run_btn = st.button(
        "🚀 Iniciar Análise",
        type="primary",
        use_container_width=True,
        disabled=st.session_state.running or not query,
    )

# ---------------------------------------------------------------------------
# Handle "Iniciar Análise" click — POST /runs
# ---------------------------------------------------------------------------
if run_btn and query:
    payload = {
        "query": query,
        "max_results": max_results,
        "model": model,
        "include_threshold": include_threshold,
        "review_threshold": review_threshold,
        "features": {
            "require_evidence": require_evidence,
            "enable_thematic_clusters": enable_clusters,
            "enable_structural_roles": enable_structural_roles,
            "enable_screening_rerank": enable_rerank,
            "enable_prisma": enable_prisma,
            "enable_snapshot": enable_snapshot,
            "enable_comparative_analysis": enable_comparative,
            "enable_whitespace_analysis": enable_whitespace,
            "enable_manual_review_queue": enable_manual_review,
        },
    }
    try:
        resp = requests.post(f"{API_BASE_URL}/runs", json=payload, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        st.session_state.run_id = data["run_id"]
        st.session_state.running = True
        st.session_state.run_data = None
        st.session_state.live_data = {}
        st.session_state.error = None
    except Exception as exc:
        st.session_state.error = f"Falha ao iniciar análise: {exc}"
    st.rerun()

# ---------------------------------------------------------------------------
# Poll running job — GET /runs/{run_id}
# ---------------------------------------------------------------------------
if st.session_state.running and st.session_state.run_id:
    try:
        resp = requests.get(
            f"{API_BASE_URL}/runs/{st.session_state.run_id}", timeout=10
        )
        live = resp.json() if resp.ok else {}
    except Exception as exc:
        live = {}
        st.session_state.error = f"Erro ao consultar status: {exc}"
        st.session_state.running = False

    if live:
        st.session_state.live_data = live
        status = live.get("status", "running")
        if status == "error":
            st.session_state.running = False
            st.session_state.error = live.get("error", "Erro desconhecido")
        elif status not in ("queued", "running"):
            st.session_state.running = False
            st.session_state.run_data = live

# ---------------------------------------------------------------------------
# Helpers para renderizar resultados
# ---------------------------------------------------------------------------

DECISION_COLOR = {
    "include": "🟢",
    "review": "🟡",
    "exclude": "🔴",
}


def _decision_icon(decision: str) -> str:
    return DECISION_COLOR.get((decision or "").lower(), "⚪")


def _build_patents_df(patents: list, evaluations: list) -> pd.DataFrame:
    eval_by_record = {e.get("record_id", ""): e for e in evaluations}
    rows = []
    for p in patents:
        rid = p.get("record_id", "")
        ev = eval_by_record.get(rid, {})
        decision = ev.get("screening_decision", "")
        rows.append(
            {
                "Decisão": f"{_decision_icon(decision)} {decision}",
                "Score": ev.get("screening_score") or ev.get("relevance_score") or 0.0,
                "Título": p.get("title", ""),
                "ID": p.get("patent_id") or rid,
                "Assignee": p.get("assignee", ""),
                "Data Pub.": p.get("publication_date", ""),
                "Fonte": p.get("source", ""),
                "Cluster": ev.get("thematic_cluster", ""),
                "Domínio": ev.get("technical_domain", ""),
                "Inovação": ev.get("innovation_level", ""),
                "Confiança": ev.get("confidence", 0.0),
                "_record_id": rid,
                "_patent_full": p,
                "_eval_full": ev,
            }
        )
    return pd.DataFrame(rows)


def _render_patent_card(patent: dict, evaluation: dict) -> None:
    decision = evaluation.get("screening_decision", "")
    score = evaluation.get("relevance_score") or evaluation.get("screening_score") or 0.0
    st.markdown(
        f"**{patent.get('title', 'Sem título')}** &nbsp; {_decision_icon(decision)} `{decision}` &nbsp; Score: `{score:.1f}`"
    )

    col1, col2 = st.columns([2, 1])
    with col1:
        if patent.get("abstract"):
            st.caption("**Resumo**")
            st.write(patent["abstract"])
        elif patent.get("snippet"):
            st.caption("**Trecho**")
            st.write(patent["snippet"])

        if evaluation.get("summary"):
            st.caption("**Avaliação do LLM**")
            st.write(evaluation["summary"])

        if evaluation.get("key_findings"):
            st.caption("**Achados-chave**")
            for kf in evaluation["key_findings"]:
                st.markdown(f"- {kf}")

        if evaluation.get("evidence_snippets"):
            with st.expander("Evidências textuais"):
                for snip in evaluation["evidence_snippets"]:
                    st.markdown(f"> {snip}")

    with col2:
        meta = {
            "ID": patent.get("patent_id", "—"),
            "Assignee": patent.get("assignee", "—"),
            "Inventores": ", ".join((patent.get("inventors") or [])[:3]) or "—",
            "Depósito": patent.get("filing_date", "—"),
            "Publicação": patent.get("publication_date", "—"),
            "Fonte": patent.get("source", "—"),
        }
        for label, val in meta.items():
            st.markdown(f"**{label}:** {val}")

        if evaluation.get("thematic_cluster"):
            st.markdown(f"**Cluster:** {evaluation['thematic_cluster']}")
        if evaluation.get("technical_domain"):
            st.markdown(f"**Domínio:** {evaluation['technical_domain']}")
        if evaluation.get("innovation_level"):
            st.markdown(f"**Inovação:** {evaluation['innovation_level']}")
        if evaluation.get("maturity_level"):
            st.markdown(f"**Maturidade:** {evaluation['maturity_level']}")

        if patent.get("url"):
            st.link_button("Abrir patente", patent["url"])

    if evaluation.get("screening_reason"):
        st.caption(f"Motivo da triagem: *{evaluation['screening_reason']}*")
    if evaluation.get("llm_error"):
        st.warning(f"Erro LLM: {evaluation['llm_error']}")


def _render_coverage_metrics(cm: dict, total_duration: float | None = None) -> None:
    cols = st.columns(6)
    cols[0].metric("Coletadas (raw)", cm.get("raw_scraped", "—"))
    cols[1].metric("Únicas", cm.get("unique_patents", "—"))
    cols[2].metric("Triadas", cm.get("screened", "—"))
    cols[3].metric("Incluídas", cm.get("included", "—"))
    cols[4].metric("Em revisão", cm.get("review", "—"))
    cols[5].metric("Excluídas", cm.get("excluded", "—"))

    col2 = st.columns(4)
    col2[0].metric("Duplicatas removidas", cm.get("duplicates_removed", "—"))
    col2[1].metric("Extrações completas", cm.get("full_extractions", "—"))
    col2[2].metric("Fila rev. manual", cm.get("manual_review_required", "—"))
    if total_duration:
        col2[3].metric("Duração total", f"{total_duration:.0f}s")


def _render_prisma(prisma: dict) -> None:
    flow = prisma.get("flow", {})
    if not flow:
        st.info("Dados PRISMA não disponíveis.")
        return

    ident = flow.get("identification", {})
    screen = flow.get("screening", {})
    elig = flow.get("eligibility", {})
    synth = flow.get("synthesis", {})

    st.markdown("#### Fluxo PRISMA")
    rows = [
        ("Identificação", "Registros brutos coletados", ident.get("raw_records", "—")),
        ("Identificação", "Registros únicos após dedupe", ident.get("unique_records", "—")),
        ("Identificação", "Duplicatas removidas", ident.get("duplicates_removed", "—")),
        ("Triagem", "Triados pelo LLM", screen.get("screened", "—")),
        ("Triagem", "Incluídos", screen.get("included", "—")),
        ("Triagem", "Em revisão", screen.get("review", "—")),
        ("Triagem", "Excluídos", screen.get("excluded", "—")),
        ("Elegibilidade", "Extrações detalhadas", elig.get("full_extractions", "—")),
        ("Elegibilidade", "Revisão manual obrigatória", elig.get("manual_review_required", "—")),
        ("Síntese", "Registros analisados", synth.get("analyzed_records", "—")),
        (
            "Síntese",
            "Análise comparativa gerada",
            "Sim" if synth.get("comparative_analysis_generated") else "Não",
        ),
    ]
    df = pd.DataFrame(rows, columns=["Fase", "Etapa", "Valor"])
    st.dataframe(df, hide_index=True, use_container_width=True)


def _render_clusters(clusters_data: dict) -> None:
    clusters = clusters_data.get("clusters", [])
    if not clusters:
        st.info("Nenhum cluster temático gerado.")
        return

    df = pd.DataFrame(
        [
            {
                "Cluster": c["cluster"],
                "Patentes": c["count"],
                "Score médio": round(c.get("average_score", 0), 2),
                "Confiança média": round(c.get("average_confidence", 0), 2),
                "Evidências": c.get("evidence_count", 0),
            }
            for c in clusters
        ]
    )

    fig = px.bar(
        df,
        x="Patentes",
        y="Cluster",
        orientation="h",
        color="Score médio",
        color_continuous_scale="Blues",
        text="Patentes",
        title="Clusters temáticos — quantidade de patentes",
    )
    fig.update_layout(yaxis={"categoryorder": "total ascending"}, height=350)
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(df, hide_index=True, use_container_width=True)


def _render_whitespace(ws: dict) -> None:
    if not ws or ws.get("status") != "ok":
        st.info("Whitespace analysis não disponível ou não gerada.")
        return

    candidates = ws.get("whitespace_candidates", [])
    if candidates:
        st.markdown("#### Candidatos de whitespace")
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
        df_matrix = pd.DataFrame(matrix)
        st.dataframe(df_matrix, hide_index=True, use_container_width=True)

    corpus = ws.get("corpus_summary", {})
    if corpus:
        st.markdown("#### Sumário do corpus")
        st.json(corpus)


def _render_output_files(output_paths: dict) -> None:
    if not output_paths:
        st.info("Nenhum arquivo de saída registrado.")
        return
    for label, path in output_paths.items():
        if os.path.isfile(path):
            st.markdown(f"**{label}:** `{path}`")
        else:
            st.markdown(f"**{label}:** ~~`{path}`~~ *(não encontrado)*")


def _render_results(d: dict) -> None:
    query_label = d.get("query", "—")
    total_dur = d.get("total_duration_seconds")
    patents = d.get("patents", [])
    evaluations = d.get("evaluations", [])
    cm = d.get("coverage_metrics", {})
    clusters_data = d.get("thematic_clusters", {})
    comparative = d.get("comparative_analysis", "")
    whitespace = d.get("whitespace_analysis", {})
    prisma = d.get("prisma_flow", {})
    output_paths = d.get("output_paths", {})
    errors = d.get("errors", [])
    manual_review = d.get("manual_review_queue", [])

    st.success(
        f"Análise concluída — **{query_label}** &nbsp;|&nbsp; "
        f"{len(patents)} patentes &nbsp;|&nbsp; "
        f"{total_dur:.0f}s" if total_dur else f"Análise concluída — **{query_label}**"
    )
    if errors:
        with st.expander(f"⚠️ {len(errors)} erro(s) durante a execução"):
            for err in errors:
                st.warning(err)

    st.markdown("### Métricas de cobertura")
    _render_coverage_metrics(cm, total_dur)

    st.divider()

    tab_patents, tab_clusters, tab_comparative, tab_whitespace, tab_prisma, tab_files = st.tabs(
        ["Patentes", "Clusters", "Análise Comparativa", "Whitespace", "PRISMA", "Arquivos"]
    )

    with tab_patents:
        df = _build_patents_df(patents, evaluations)
        if df.empty:
            st.info("Nenhuma patente encontrada.")
        else:
            display_cols = [
                "Decisão", "Score", "Título", "ID", "Assignee", "Data Pub.", "Cluster", "Fonte",
            ]
            st.dataframe(
                df[display_cols],
                hide_index=True,
                use_container_width=True,
                column_config={
                    "Score": st.column_config.NumberColumn(format="%.1f"),
                    "Título": st.column_config.TextColumn(width="large"),
                },
            )

            if manual_review:
                with st.expander(f"Fila de revisão manual ({len(manual_review)} patentes)"):
                    for item in manual_review:
                        st.markdown(
                            f"- **{item.get('title', item.get('patent_id', '—'))}** "
                            f"— Score: `{item.get('screening_score', '—')}` "
                            f"— {item.get('reason', '')}"
                        )

            st.markdown("---")
            st.markdown("#### Detalhes por patente")
            eval_by_record = {e.get("record_id", ""): e for e in evaluations}
            for patent in patents:
                rid = patent.get("record_id", "")
                ev = eval_by_record.get(rid, {})
                title = patent.get("title") or patent.get("patent_id") or rid
                with st.expander(
                    f"{_decision_icon(ev.get('screening_decision', ''))} {title[:90]}"
                ):
                    _render_patent_card(patent, ev)

    with tab_clusters:
        _render_clusters(clusters_data)

    with tab_comparative:
        if comparative and comparative.strip() and not comparative.startswith("⚠️"):
            st.markdown(comparative)
        else:
            st.info(comparative or "Análise comparativa não gerada para esta execução.")

    with tab_whitespace:
        _render_whitespace(whitespace)

    with tab_prisma:
        _render_prisma(prisma)

    with tab_files:
        _render_output_files(output_paths)
        md_path = output_paths.get("markdown", "")
        if md_path and os.path.isfile(md_path):
            with open(md_path, encoding="utf-8") as f:
                md_content = f.read()
            st.download_button(
                "⬇️ Baixar relatório Markdown",
                data=md_content,
                file_name=os.path.basename(md_path),
                mime="text/markdown",
            )
        json_path = output_paths.get("json", "")
        if json_path and os.path.isfile(json_path):
            with open(json_path, encoding="utf-8") as f:
                json_content = f.read()
            st.download_button(
                "⬇️ Baixar relatório JSON",
                data=json_content,
                file_name=os.path.basename(json_path),
                mime="application/json",
            )


# ---------------------------------------------------------------------------
# Main rendering
# ---------------------------------------------------------------------------
st.title("🔬 Revisão Técnica de Patentes")

if st.session_state.running:
    live = st.session_state.live_data

    with st.status("⏳ Executando pipeline...", expanded=True, state="running"):
        if live:
            cm_live = live.get("coverage_metrics", {})
            c1, c2, c3, c4, c5 = st.columns(5)
            c1.metric("Coletadas", len(live.get("patents", [])) or "—")
            c2.metric("Únicas", cm_live.get("unique_patents", "—"))
            c3.metric("Triadas", cm_live.get("screened", "—"))
            c4.metric("Incluídas", cm_live.get("included", "—"))
            c5.metric("Em revisão", cm_live.get("review", "—"))

            stages = live.get("stage_metrics", [])
            if stages:
                last_stage = stages[-1]
                st.write(
                    f"**Etapa:** `{last_stage.get('stage', '')}` — "
                    f"{last_stage.get('detail', '')} "
                    f"({last_stage.get('duration_seconds', 0):.1f}s)"
                )
        else:
            st.write("Iniciando pipeline...")

    time.sleep(3)
    st.rerun()

elif st.session_state.error:
    st.error(f"Erro na execução: {st.session_state.error}")

elif st.session_state.run_data is not None:
    _render_results(st.session_state.run_data)

else:
    st.info(
        "Configure a busca no painel lateral e clique em **🚀 Iniciar Análise**.\n\n"
        "O pipeline irá buscar patentes no Google Patents e Patentscope, "
        "avaliar com o modelo Ollama selecionado e gerar relatórios automáticos."
    )
