# Ablation Summary

- **Gerado em:** 2026-04-04T23:46:48
- **Pasta raiz:** /home/murilo/Documentos/RevisaoTecnica/output/ablation_20260404_234648
- **Benchmark:** /home/murilo/Documentos/RevisaoTecnica/benchmarks/frozen_ablation_benchmark.json

## Variantes

### baseline

- Pipeline completo com todas as features habilitadas.

### no_evidence

- Remove a exigência de evidência textual.

### no_clusters

- Desliga a síntese temática por cluster.

### no_prisma

- Desliga os artefatos PRISMA-like.

### no_snapshot

- Desliga o snapshot versionado da execução.

### no_comparative_analysis

- Desliga a análise comparativa gerada pelo LLM.

### no_manual_review

- Desliga a fila de revisão manual.

## Resultados

## Comparação Geral

| Variante | Casos | Score médio | Δ Score | Tempo total | Δ Tempo | Inclusões | Revisão manual | Clusters |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| no_evidence | 1 | 8.65 | +0.00 | 0.00s | -0.01s | 2.00 | 0.00 | 2.00 |
| no_clusters | 1 | 8.65 | +0.00 | 0.00s | -0.01s | 2.00 | 0.00 | 0.00 |
| no_prisma | 1 | 8.65 | +0.00 | 0.00s | -0.01s | 2.00 | 0.00 | 2.00 |
| no_snapshot | 1 | 8.65 | +0.00 | 0.00s | -0.01s | 2.00 | 0.00 | 2.00 |
| no_comparative_analysis | 1 | 8.65 | +0.00 | 0.00s | -0.01s | 2.00 | 0.00 | 2.00 |
| no_manual_review | 1 | 8.65 | +0.00 | 0.00s | -0.01s | 2.00 | 0.00 | 2.00 |
| baseline | 1 | 8.65 | +0.00 | 0.01s | +0.00s | 2.00 | 0.00 | 2.00 |

- **Melhor qualidade média:** no_evidence
- **Mais rápido:** no_evidence

### Frozen CO2 thermal storage / baseline

- **Query:** carbon dioxide thermal energy storage
- **Score médio:** 8.65
- **Tempo total:** 0.01s
- **Incluídas:** 2
- **Revisão manual:** 0
- **Clusters:** 2
- **Métricas de etapa:** 6
- **Cache LLM:** hits=0, misses=0

### Frozen CO2 thermal storage / no_evidence

- **Query:** carbon dioxide thermal energy storage
- **Score médio:** 8.65
- **Tempo total:** 0.00s
- **Incluídas:** 2
- **Revisão manual:** 0
- **Clusters:** 2
- **Métricas de etapa:** 6
- **Cache LLM:** hits=0, misses=0

### Frozen CO2 thermal storage / no_clusters

- **Query:** carbon dioxide thermal energy storage
- **Score médio:** 8.65
- **Tempo total:** 0.00s
- **Incluídas:** 2
- **Revisão manual:** 0
- **Clusters:** 0
- **Métricas de etapa:** 6
- **Cache LLM:** hits=0, misses=0

### Frozen CO2 thermal storage / no_prisma

- **Query:** carbon dioxide thermal energy storage
- **Score médio:** 8.65
- **Tempo total:** 0.00s
- **Incluídas:** 2
- **Revisão manual:** 0
- **Clusters:** 2
- **Métricas de etapa:** 6
- **Cache LLM:** hits=0, misses=0

### Frozen CO2 thermal storage / no_snapshot

- **Query:** carbon dioxide thermal energy storage
- **Score médio:** 8.65
- **Tempo total:** 0.00s
- **Incluídas:** 2
- **Revisão manual:** 0
- **Clusters:** 2
- **Métricas de etapa:** 6
- **Cache LLM:** hits=0, misses=0

### Frozen CO2 thermal storage / no_comparative_analysis

- **Query:** carbon dioxide thermal energy storage
- **Score médio:** 8.65
- **Tempo total:** 0.00s
- **Incluídas:** 2
- **Revisão manual:** 0
- **Clusters:** 2
- **Métricas de etapa:** 6
- **Cache LLM:** hits=0, misses=0

### Frozen CO2 thermal storage / no_manual_review

- **Query:** carbon dioxide thermal energy storage
- **Score médio:** 8.65
- **Tempo total:** 0.00s
- **Incluídas:** 2
- **Revisão manual:** 0
- **Clusters:** 2
- **Métricas de etapa:** 6
- **Cache LLM:** hits=0, misses=0
