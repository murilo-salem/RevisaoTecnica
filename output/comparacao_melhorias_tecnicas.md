# Comparação das Melhorias do Sistema

Data de referência: `2026-04-02`

## Resumo

O sistema saiu de um fluxo linear de scraping + avaliação para uma arquitetura com:
- triagem em duas fases
- roteamento explícito por tema e profundidade
- memória operacional separada
- protocolo metodológico versionado
- ablation comparável
- relatório com evidência, contexto compartilhado e gate de rascunho vazio
- cache persistente do LLM
- métricas estruturadas por etapa
- testes arquiteturais e de regressão do relatório

## Tabela Comparativa

| Área | Antes | Agora | Impacto |
|---|---|---|---|
| Triagem | Avaliação direta no LLM | `include / review / exclude` com score e confiança | Reduz custo e melhora a precisão da etapa seguinte |
| Evidência | Trechos opcionais ou ausentes | Evidência obrigatória com fallback e auditoria | Diminui alucinação e melhora rastreabilidade |
| Roteamento | Fluxo único | `ThemeRouter` decide `screen_only`, `manual_review`, `deep_extraction` e `thematic_synthesis` | Permite análise por profundidade e política explícita |
| Memória | Estado em JSON + snapshot | `MemorySidecar` + `memory_journal` + slots | Melhora auditabilidade e retomada operacional |
| Writer | Relatório gerado com contexto indireto | `writing_context` compartilhado e `draft_status` | Evita relatório vazio ou sem substância |
| PRISMA-like | Inexistente | Fluxo de identificação, triagem, elegibilidade e síntese | Melhora transparência metodológica |
| Clusterização | Ausente | Síntese temática por grupo | Ajuda a interpretar tendências |
| Comparação | Manual/informal | `run_ablation_suite` com benchmark fixo | Permite provar ganho e custo de cada feature |
| Configuração | Misturada com código | `config.py` + snapshot + feature flags | Facilita tuning e reprodutibilidade |
| Cache LLM | Sem persistência | Cache em disco por modelo e prompt | Reduz custo e reusa respostas repetidas |
| Métricas | Soltas e implícitas | `stage_metrics` estruturado por etapa | Facilita análise de performance |
| Testes | Sem contrato arquitetural | Testes mínimos de memória, router, estado, cache e draft gate | Protege regressões estruturais |

## O Que Ainda Pode Melhorar

1. `Observabilidade estruturada`
- A base já existe, mas ainda pode ganhar métricas por rota, por fonte e por tipo de falha.

3. `Config externa do benchmark`
- O benchmark já existe, mas pode virar conjunto maior e versionado por domínio.

4. `Testes de regressão de saída`
- Os testes atuais validam contrato.
- Falta checar forma e conteúdo dos relatórios gerados.

5. `Execução por lotes paralelos`
- O ablation ainda roda em série.
- Dá para paralelizar por variante ou caso quando o custo do ambiente permitir.

6. `Política de router mais rica`
- O roteador atual é explícito e útil, mas ainda é heurístico.
- Pode evoluir para política baseada em utilidade, score e custo.

7. `Desacoplamento de impressão e núcleo`
- O fluxo principal ainda imprime bastante no console.
- Migrar isso para logger estruturado tornaria o núcleo mais testável.
