# Comparativo Métrico: Modelo Atual vs Modelo Antigo

Data de referência: `2026-04-02`

## Contexto

As duas execuções usaram a mesma query (`carbon dioxide thermal energy storage`) e `max_results=5`.
A comparação é útil, mas não perfeitamente determinística porque as fontes externas de patente podem devolver corpora diferentes entre execuções.

## Métricas

| Métrica | Modelo Atual | Modelo Antigo | Delta |
|---|---:|---:|---:|
| Patentes únicas | 10 | 10 | 0 |
| Incluídas | 8 | 10 | -2 |
| Revisão manual | 1 | 0 | 1 |
| Excluídas | 1 | 0 | 1 |
| Score médio de relevância | 9.11 | 9.00 | +0.11 |
| Tempo total | 79.65s | 77.30s | +2.35s |
| Etapas registradas | 6 | 0 | 6 |
| Cache LLM | hits=0, misses=39, entradas=19 | inexistente | cache ativo |
| PRISMA-like | sim | não | + |
| Memória operacional | sim | não | + |
| Draft status | ready | não disponível | + |
| Tamanho do relatório Markdown | 48342 bytes | 38066 bytes | +10276 bytes |
| Análise comparativa gerada | fallback: ⚠️ Não foi possível gerar a análise comparativa. | texto longo em Markdown | diferente |

## Leitura Rápida

### Modelo Atual
- Mais seletivo: incluiu 8 patentes, mandou 1 para revisão manual e excluiu 1.
- Mais auditável: gravou `stage_metrics`, `memory_journal`, `memory_sidecar`, `snapshot` e `PRISMA-like flow`.
- Melhor controle de qualidade: `draft_status=ready` e cache LLM persistente.
- Limitação observada nesta execução: a análise comparativa caiu no fallback `⚠️ Não foi possível gerar a análise comparativa.` por erro 500 do Ollama.

### Modelo Antigo
- Mais permissivo: incluiu as 10 patentes da amostra e não abriu fila de revisão manual.
- Relatório narrativo mais simples, sem memória operacional nem métricas estruturadas.
- Comparativo em Markdown mais rico nesta execução, com 5.175 caracteres.
- Menos controle de rastreabilidade e menos sinais para regressão/ablation.

## Arquivos Gerados

- [Relatório bruto do modelo atual](/home/murilo/Documentos/RevisaoTecnica/output/modelo_atual_relatorio.md)
- [JSON bruto do modelo atual](/home/murilo/Documentos/RevisaoTecnica/output/modelo_atual_relatorio.json)
- [Relatório bruto do modelo antigo](/home/murilo/Documentos/RevisaoTecnica/output/modelo_antigo_relatorio.md)
- [JSON bruto do modelo antigo](/home/murilo/Documentos/RevisaoTecnica/output/modelo_antigo_relatorio.json)

## Observação Importante

As diferenças numéricas refletem não só a mudança de arquitetura, mas também a variabilidade da coleta externa. Para uma avaliação científica mais rígida, o próximo passo é fixar um benchmark de corpus/links já resolvidos e rodar ambas as versões sobre o mesmo conjunto congelado.
