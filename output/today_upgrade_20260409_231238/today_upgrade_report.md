# Relatório Completo das Atualizações Técnicas de 9 de abril de 2026

- **Gerado em:** 2026-04-09T23:15:10
- **Query de referência:** `carbon dioxide thermal energy storage`
- **Modelo avaliado no benchmark A/B:** `gemma3:27b`
- **Corpus congelado usado na comparação:** [run_state_latest.json](/home/murilo/Documentos/RevisaoTecnica/output/smoke_whitespace_20260409/run_state_latest.json)
- **Resumo estruturado deste relatório:** [today_upgrade_summary.json](/home/murilo/Documentos/RevisaoTecnica/output/today_upgrade_20260409_231238/today_upgrade_summary.json)
- **Comparação entre modelos usada para a recomendação do default:** [model_comparison_summary.json](/home/murilo/Documentos/RevisaoTecnica/output/model_compare_20260409_captured/model_comparison_summary.json)

## 1. Objetivo Deste Ciclo

O trabalho de hoje teve três objetivos práticos:

1. aumentar a profundidade técnica da leitura do pipeline, para distinguir melhor quando o CO2 é de fato o meio armazenado, quando é apenas fluido de trabalho, e quando o documento é só adjacente;
2. melhorar a geração de hipóteses de `whitespace`, para que o sistema passe a sugerir brechas tecnológicas com base em matriz de cobertura, e não apenas em texto livre;
3. consolidar uma recomendação operacional de modelo local, comparando custo e qualidade entre o `gemma3:27b` e um candidato mais pesado, `qwen2.5:32b`.

Em termos simples: o pipeline anterior já funcionava, mas ainda era relativamente permissivo em casos limítrofes e pouco estruturado para explicar por que um documento estava perto ou longe do núcleo técnico da query.

## 2. Escopo Exato do Benchmark

O benchmark A/B deste relatório não compara scraping nem muda o corpus entre execuções. Ele isola as melhorias técnicas ligadas a:

- papéis estruturados do CO2 e do armazenamento;
- rerank de triagem na zona cinzenta;
- whitespace estruturado em JSON.

Isso foi feito para evitar ruído. O mesmo conjunto de 4 patentes foi usado nas duas variantes.

As duas variantes foram:

| Variante | O que fica desligado | O que isso representa |
|---|---|---|
| `pre_today_baseline` | `enable_structural_roles=false`, `enable_screening_rerank=false`, `enable_whitespace_analysis=false` | comportamento equivalente ao pipeline sem as melhorias técnicas implementadas hoje |
| `today_updates` | tudo ligado | pipeline com as atualizações de hoje |

Observação importante: duas mudanças de infraestrutura entram no relatório qualitativo, mas não foram desligadas nesse A/B:

- pivot do default para `gemma3:27b`;
- detecção robusta e resolução de alias do modelo no Ollama.

## 3. O Que Foi Implementado Hoje

### 3.1 Pivot do modelo padrão para `gemma3:27b`

Arquivos:

- [config.py](/home/murilo/Documentos/RevisaoTecnica/config.py)
- [main.py](/home/murilo/Documentos/RevisaoTecnica/main.py)
- [README.md](/home/murilo/Documentos/RevisaoTecnica/README.md)

Motivo:

- o `gemma3:4b` era leve demais para triagem técnica fina;
- o objetivo era subir profundidade local sem depender de API externa;
- o `27b` é pesado, mas ainda viável no ambiente local e melhor alinhado ao problema.

### 3.2 Detecção robusta do modelo ativo

Arquivo:

- [evaluator/llm_evaluator.py](/home/murilo/Documentos/RevisaoTecnica/evaluator/llm_evaluator.py)

Motivo:

- o Ollama pode expor variantes compatíveis do mesmo modelo;
- antes disso, era possível falhar na conexão por diferença de nome, não por indisponibilidade real;
- agora o evaluator distingue `requested_model` do modelo efetivamente ativado e resolve aliases compatíveis.

### 3.3 Schema técnico estruturado

Arquivos:

- [models/patent.py](/home/murilo/Documentos/RevisaoTecnica/models/patent.py)
- [evaluator/llm_evaluator.py](/home/murilo/Documentos/RevisaoTecnica/evaluator/llm_evaluator.py)
- [report/generator.py](/home/murilo/Documentos/RevisaoTecnica/report/generator.py)

Novos campos adicionados ao `PatentEvaluation`:

- `co2_role`
- `storage_role`
- `system_boundary`
- `cycle_type`
- `heat_source_sink`
- `claim_focus`
- `exclusion_category`
- `rerank_applied`
- `rerank_reason`

Motivo:

- reduzir ambiguidade semântica;
- permitir comparação por eixo técnico;
- deixar o `whitespace` baseado em estrutura, e não apenas em prosa.

### 3.4 Rerank para zona cinzenta

Arquivos:

- [config.py](/home/murilo/Documentos/RevisaoTecnica/config.py)
- [evaluator/llm_evaluator.py](/home/murilo/Documentos/RevisaoTecnica/evaluator/llm_evaluator.py)
- [pipeline/orchestrator.py](/home/murilo/Documentos/RevisaoTecnica/pipeline/orchestrator.py)

Parâmetros relevantes:

- `SCREEN_INCLUDE_THRESHOLD = 7.0`
- `SCREEN_REVIEW_THRESHOLD = 4.5`
- `SCREEN_RERANK_MIN_SCORE = 5.5`
- `SCREEN_RERANK_MAX_SCORE = 8.0`

Motivo:

- casos `review` e itens em faixa limítrofe merecem um segundo passe;
- a meta não é aumentar inclusão, e sim diminuir falso quase-incluir;
- o rerank também força o modelo a reafirmar ou rebaixar a interpretação técnica.

### 3.5 Whitespace estruturado em JSON

Arquivos:

- [evaluator/llm_evaluator.py](/home/murilo/Documentos/RevisaoTecnica/evaluator/llm_evaluator.py)
- [pipeline/state.py](/home/murilo/Documentos/RevisaoTecnica/pipeline/state.py)
- [pipeline/orchestrator.py](/home/murilo/Documentos/RevisaoTecnica/pipeline/orchestrator.py)
- [report/generator.py](/home/murilo/Documentos/RevisaoTecnica/report/generator.py)

Novo artefato gerado:

- [whitespace_analysis_20260409_231344.json](/home/murilo/Documentos/RevisaoTecnica/output/today_upgrade_20260409_231238/today_updates/whitespace_analysis_20260409_231344.json)

Motivo:

- `whitespace` real normalmente aparece entre o núcleo e a fronteira técnica;
- por isso a análise passou a consumir `include + review + excludes adjacentes`;
- o resultado agora é auditável como matriz, e não apenas como texto narrativo.

### 3.6 Benchmark reproduzível das melhorias do dia

Arquivos:

- [pipeline/features.py](/home/murilo/Documentos/RevisaoTecnica/pipeline/features.py)
- [pipeline/frozen_benchmark.py](/home/murilo/Documentos/RevisaoTecnica/pipeline/frozen_benchmark.py)
- [pipeline/upgrade_benchmark.py](/home/murilo/Documentos/RevisaoTecnica/pipeline/upgrade_benchmark.py)
- [main.py](/home/murilo/Documentos/RevisaoTecnica/main.py)

Motivo:

- não depender de script ad hoc para comparar antes/depois;
- permitir rerodar a análise com o mesmo corpus congelado;
- materializar a recomendação de modelo e de arquitetura em artefatos persistidos.

### 3.7 Testes de regressão

Arquivos:

- [tests/test_architecture.py](/home/murilo/Documentos/RevisaoTecnica/tests/test_architecture.py)
- [tests/test_frozen_pipeline.py](/home/murilo/Documentos/RevisaoTecnica/tests/test_frozen_pipeline.py)

Validação executada:

- `venv/bin/python -m unittest tests.test_architecture tests.test_frozen_pipeline`
- resultado: `39` testes, `OK`

## 4. Metodologia da Comparação

### 4.1 Corpus

Foram usadas exatamente 4 patentes do corpus congelado de hoje:

- `US20200182095A1`
- `CN118934113A`
- `AU244427549`
- `US433566429`

### 4.2 Regras mantidas iguais nas duas variantes

- mesma query;
- mesmo corpus;
- mesmo modelo, `gemma3:27b`;
- mesmos thresholds de inclusão e revisão;
- mesmo pipeline de scraping congelado.

### 4.3 O que muda entre as variantes

Na baseline, o pipeline:

- não extrai papéis técnicos estruturados;
- não faz rerank na triagem;
- não gera `whitespace_analysis`.

Na versão atual, o pipeline:

- extrai e canonicaliza os papéis estruturados;
- faz rerank dos casos limítrofes;
- gera matriz estruturada de whitespace.

## 5. Resultado Quantitativo do Benchmark A/B

| Variante | Score médio | Tempo total | Incluídas | Review | Excluídas | Rerank | Fill estrutural | Whitespaces |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `pre_today_baseline` | 7.13 | 66.21s | 1 | 2 | 1 | 0 | 0.000 | 0 |
| `today_updates` | 6.80 | 85.38s | 1 | 2 | 1 | 2 | 1.000 | 1 |

Leitura correta desses números:

- o roteamento agregado não mudou;
- a versão nova ficou mais lenta;
- a versão nova ficou mais conservadora;
- a versão nova ficou muito mais explicável e estruturada.

### 5.1 Deltas principais

- **Delta de score médio:** `-0.33`
- **Delta de tempo total:** `+19.17s`
- **Delta de itens rerankeados:** `+2`
- **Delta de cobertura estrutural:** `+1.000`
- **Delta de candidatos de whitespace:** `+1`

O ponto central aqui é que a queda de score não indica piora de qualidade. Indica calibragem mais rígida em casos de borda técnica.

## 6. Interpretação do Antes vs Depois

### 6.1 O que melhorou de verdade

1. o pipeline deixou de tratar os casos limítrofes como “quase bons” sem explicação técnica explícita;
2. passou a classificar o papel do CO2 e do armazenamento em cada documento;
3. passou a gerar uma hipótese concreta de `whitespace` a partir da matriz de cobertura;
4. passou a registrar o custo adicional do rerank e a persistir esse efeito no estado da execução.

### 6.2 O que não mudou

1. o top patent continuou sendo `CN118934113A`;
2. o total agregado permaneceu `1 include`, `2 review`, `1 exclude`;
3. o pipeline continuou entendendo `US433566429` como documento fora do núcleo;
4. a fila manual permaneceu com 2 itens.

### 6.3 O que isso significa na prática

O ganho principal não foi “pegar mais patente”. Foi:

- reduzir excesso de confiança;
- separar melhor núcleo vs fronteira;
- transformar a leitura da borda técnica em insumo para whitespace.

## 7. Diferença por Patente

| Patente | Baseline | Atual | Score triagem | Relevância | Rerank | Leitura prática |
|---|---|---|---:|---:|---|---|
| `CN118934113A` | include | include | 9.2 -> 9.2 | 10.0 -> 10.0 | não | núcleo inequívoco, nenhuma mudança necessária |
| `US20200182095A1` | review | review | 6.8 -> 5.3 | 6.1 -> 5.1 | sim | rebaixamento de confiança em patente onde CO2 atua mais como working fluid do que como meio central de armazenamento |
| `AU244427549` | review | review | 6.2 -> 4.8 | 5.3 -> 5.3 | sim | caso de refrigeração transcrítica com storage acoplado, mas ainda de fronteira e não de núcleo |
| `US433566429` | exclude | exclude | 3.5 -> 3.5 | 0.0 -> 0.0 | não | genérico de TES industrial, sem centralidade de CO2 |

### 7.1 `CN118934113A`

Continua sendo o melhor documento do corpus.

Na versão atual, o pipeline o classifica como:

- `co2_role = stored_thermodynamic_medium`
- `storage_role = explicit_thermal_storage`
- `system_boundary = dedicated_storage_system`
- `cycle_type = supercritical_or_transcritical_co2`

Isso é exatamente o tipo de assinatura que o pipeline deveria reconhecer como núcleo.

### 7.2 `US20200182095A1`

Esse foi um dos casos mais úteis para mostrar o valor das mudanças.

Na baseline:

- o score de triagem ficou em `6.8`;
- o score de relevância ficou em `6.1`;
- faltava estrutura para explicar por que ele estava apenas perto do núcleo.

Na versão atual:

- o rerank foi aplicado;
- o score de triagem caiu para `5.3`;
- o score de relevância caiu para `5.1`;
- o documento passou a ser lido explicitamente como `working_fluid`.

Interpretação:

- ele continua tecnicamente relacionado;
- mas fica mais claro que seu centro é ciclo/produção de trabalho, não armazenamento térmico centrado em CO2 como inventário.

### 7.3 `AU244427549`

Esse é um caso clássico de borda técnica.

Na versão atual:

- `co2_role = refrigerant_loop`
- `storage_role = explicit_thermal_storage`
- `system_boundary = process_integration`
- `screening_score = 4.8`

Interpretação:

- existe storage;
- existe CO2;
- mas o sistema está mais próximo de refrigeração/subcooling com integração de armazenamento do que do núcleo exato da query.

Esse tipo de caso é precisamente útil para `whitespace`, porque mostra uma combinação parcial com alto valor exploratório.

### 7.4 `US433566429`

Permanece como exclusão correta.

Na versão atual:

- `co2_role = co2_not_central`
- `exclusion_category = generic_tes`

Interpretação:

- o sistema trata corretamente um TES industrial amplo como adjacente ou fora do núcleo, mesmo quando compartilha linguagem de energia térmica.

## 8. Análise de Whitespaces

Artefato:

- [whitespace_analysis_20260409_231344.json](/home/murilo/Documentos/RevisaoTecnica/output/today_upgrade_20260409_231238/today_updates/whitespace_analysis_20260409_231344.json)

### 8.1 Resumo do corpus de whitespace

- patentes consideradas: `4`
- patentes selecionadas para a matriz: `3`
- núcleo (`core`): `1`
- fronteira (`frontier`): `2`
- adjacentes (`adjacent`): `0`

### 8.2 Estrutura observada

O núcleo e a fronteira se distribuíram assim:

- `stored_thermodynamic_medium` aparece só no núcleo;
- `refrigerant_loop` aparece na fronteira;
- `working_fluid` aparece na fronteira;
- `explicit_thermal_storage` aparece tanto no núcleo quanto na fronteira.

Essa combinação é importante porque mostra um padrão:

- o armazenamento explícito já existe nos três documentos selecionados;
- o que muda é o papel do CO2 e o limite sistêmico;
- portanto, o espaço em branco não está em “ter storage” ou “ter CO2”, mas em como esses dois papéis são amarrados na arquitetura reivindicada.

### 8.3 Candidato principal de whitespace

O candidato gerado foi:

- `hybrid_cycle_storage_architecture`

Racional do sistema:

- combinar arquiteturas de ciclo/transferência com CO2 e armazenamento térmico explicitamente reivindicado ainda aparece fragmentado entre núcleo e borda técnica.

Leitura prática:

- o núcleo forte já existe para `CO2 + storage` explícito;
- a fronteira já existe para `CO2 como working fluid` e `CO2 como refrigerant loop`;
- a oportunidade está em reivindicações que integrem esses papéis de forma arquiteturalmente mais fechada, sem cair nem no TES genérico nem no ciclo genérico.

### 8.4 O que o whitespace atual ainda não faz perfeitamente

Dois pontos apareceram no artefato:

1. `claim_focus` colapsou demais em `system_architecture`;
2. surgiu valor não canonicalizado em `heat_source_sink` para `AU244427549` (`ambiente/carga térmica`), o que mostra que a canonicalização ainda pode ser endurecida.

Isso não invalida a análise. Só indica que o schema já é útil, mas ainda não está totalmente estabilizado.

## 9. Comparação do Modelo `gemma3:27b` com `qwen2.5:32b`

Fonte:

- [model_comparison_summary.json](/home/murilo/Documentos/RevisaoTecnica/output/model_compare_20260409_captured/model_comparison_summary.json)

Resultado observado no mesmo corpus capturado:

| Modelo | Tempo total | Include | Review | Exclude | Manual review | Top patent |
|---|---:|---:|---:|---:|---:|---|
| `gemma3:27b` | 83.363s | 1 | 2 | 1 | 2 | `CN118934113A` |
| `qwen2.5:32b` | 134.017s | 1 | 2 | 1 | 2 | `CN118934113A` |

Conclusão operacional:

- o roteamento agregado foi o mesmo;
- o top patent foi o mesmo;
- o `qwen2.5:32b` foi mais lento;
- portanto, hoje não há evidência suficiente para trocar o default.

## 10. Recomendação Final Sobre o Modelo

### Recomendação

**Manter `gemma3:27b` como modelo padrão.**

### Justificativa

1. no corpus comparado ele entregou o mesmo resultado agregado do `qwen2.5:32b`;
2. foi significativamente mais rápido;
3. após as melhorias de hoje, ele já consegue produzir papéis estruturados, rerank e whitespace útil;
4. o gargalo que ainda resta é mais de schema/canonicalização do que de parâmetro puro.

## 11. Custos e Tradeoffs das Atualizações de Hoje

### Ganhos

- explicabilidade muito maior;
- melhor separação entre núcleo e fronteira;
- geração de whitespace baseada em estrutura;
- benchmark reproduzível;
- melhor auditabilidade do pipeline.

### Custos

- `+19.17s` no benchmark A/B local;
- maior custo de inferência por causa do rerank;
- maior complexidade de schema e manutenção.

### Avaliação do tradeoff

Para este caso de uso, o tradeoff é favorável. O projeto não está otimizando apenas throughput; está otimizando entendimento técnico e exploração de brechas.

## 12. Limitações Atuais

As principais limitações depois deste ciclo são:

1. `claim_focus` ainda está pouco discriminativo;
2. alguns valores retornados pelo modelo ainda escapam da canonicalização ideal;
3. o benchmark A/B de hoje isolou apenas as melhorias técnicas principais, não toda a história acumulada do sistema;
4. o corpus usado para o comparativo é pequeno, com apenas 4 patentes.

## 13. Próximos Passos Recomendados

Ordem sugerida:

1. endurecer a canonicalização de `claim_focus` e `heat_source_sink`;
2. criar mais categorias para `exclusion_category`, distinguindo melhor adjacência de refrigeração, processo e working-fluid-only;
3. ampliar o benchmark congelado com mais consultas do domínio;
4. separar `whitespace` em um estágio ainda mais rígido, com schema próprio de oportunidade, risco e evidência.

## 14. Artefatos Gerados

Relatório completo desta comparação:

- [today_upgrade_report.md](/home/murilo/Documentos/RevisaoTecnica/output/today_upgrade_20260409_231238/today_upgrade_report.md)

Resumo estruturado:

- [today_upgrade_summary.json](/home/murilo/Documentos/RevisaoTecnica/output/today_upgrade_20260409_231238/today_upgrade_summary.json)

Execução baseline:

- [patentes_carbon_dioxide_thermal_energy_storage_20260409_231344.md](/home/murilo/Documentos/RevisaoTecnica/output/today_upgrade_20260409_231238/pre_today_baseline/patentes_carbon_dioxide_thermal_energy_storage_20260409_231344.md)

Execução atual com as melhorias:

- [patentes_carbon_dioxide_thermal_energy_storage_20260409_231510.md](/home/murilo/Documentos/RevisaoTecnica/output/today_upgrade_20260409_231238/today_updates/patentes_carbon_dioxide_thermal_energy_storage_20260409_231510.md)

Whitespace estruturado:

- [whitespace_analysis_20260409_231344.json](/home/murilo/Documentos/RevisaoTecnica/output/today_upgrade_20260409_231238/today_updates/whitespace_analysis_20260409_231344.json)

Comparação entre modelos:

- [model_comparison_summary.json](/home/murilo/Documentos/RevisaoTecnica/output/model_compare_20260409_captured/model_comparison_summary.json)

## 15. Conclusão

As atualizações de hoje não serviram para “inflar score” nem para “incluir mais patentes”. Serviram para deixar o pipeline tecnicamente mais disciplinado.

O efeito observado foi consistente:

- a confiança em casos de borda caiu;
- a estrutura explicativa subiu muito;
- o whitespace passou a existir como artefato real;
- o `gemma3:27b` continua sendo a melhor escolha local padrão no estado atual do projeto.
