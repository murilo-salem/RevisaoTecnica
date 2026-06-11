# Relatório das Implementações e Justificativas

Data de referência: `2026-04-02`

## Objetivo

O objetivo das mudanças foi transformar o sistema de revisão técnica de patentes em um pipeline mais:
- rastreável
- comparável
- reproduzível
- auditável
- útil para análise técnica real

## O Que Foi Feito

### 1. Triagem em duas fases
Arquivo principal: [`evaluator/llm_evaluator.py`](/home/murilo/Documentos/RevisaoTecnica/evaluator/llm_evaluator.py)

Foi implementada uma etapa de triagem rápida antes da extração completa.
Motivo:
- evitar custo desnecessário
- separar exclusão clara de casos ambíguos
- reduzir carga de LLM em documentos fora de escopo

### 2. Evidência obrigatória
Arquivo principal: [`evaluator/llm_evaluator.py`](/home/murilo/Documentos/RevisaoTecnica/evaluator/llm_evaluator.py)

As respostas do LLM passaram a carregar `evidence_snippets` e fallback automático quando a resposta vem fraca.
Motivo:
- reduzir alucinação
- melhorar explicabilidade
- deixar a decisão auditável

### 3. Roteamento explícito
Arquivos principais:
- [`pipeline/router.py`](/home/murilo/Documentos/RevisaoTecnica/pipeline/router.py)
- [`pipeline/orchestrator.py`](/home/murilo/Documentos/RevisaoTecnica/pipeline/orchestrator.py)

Foi adicionado um roteador que decide entre:
- `screen_only`
- `manual_review`
- `deep_extraction`
- `thematic_synthesis`

Motivo:
- tornar o fluxo adaptativo
- permitir políticas diferentes para casos diferentes
- abrir espaço para multiagente e ablation reais

### 4. Memória operacional separada
Arquivos principais:
- [`pipeline/memory.py`](/home/murilo/Documentos/RevisaoTecnica/pipeline/memory.py)
- [`pipeline/state.py`](/home/murilo/Documentos/RevisaoTecnica/pipeline/state.py)
- [`pipeline/orchestrator.py`](/home/murilo/Documentos/RevisaoTecnica/pipeline/orchestrator.py)

Foi criado um `MemorySidecar` com slots e journal append-only.
Motivo:
- preservar contexto entre etapas
- registrar quem decidiu o quê
- separar memória operacional do estado de relatório

### 5. Contexto compartilhado do writer
Arquivos principais:
- [`pipeline/orchestrator.py`](/home/murilo/Documentos/RevisaoTecnica/pipeline/orchestrator.py)
- [`report/generator.py`](/home/murilo/Documentos/RevisaoTecnica/report/generator.py)

O relatório agora consome `writing_context` com top patentes, clusters, roteamento e policy de slots.
Motivo:
- evitar relatório “cego”
- melhorar continuidade entre análise e escrita
- manter o resumo ancorado em contexto operacional

### 6. Gate de rascunho vazio
Arquivo principal: [`report/generator.py`](/home/murilo/Documentos/RevisaoTecnica/report/generator.py)

Foi adicionado um verificador interno que marca o relatório como `ready` ou `blocked`.
Motivo:
- impedir que uma execução sem substância pareça concluída com qualidade
- bloquear falso positivo de relatório útil

### 7. PRISMA-like e protocolo versionado
Arquivos principais:
- [`pipeline/protocol.py`](/home/murilo/Documentos/RevisaoTecnica/pipeline/protocol.py)
- [`pipeline/orchestrator.py`](/home/murilo/Documentos/RevisaoTecnica/pipeline/orchestrator.py)
- [`report/generator.py`](/home/murilo/Documentos/RevisaoTecnica/report/generator.py)

Foram adicionados protocolo, critérios, cobertura e fluxo de seleção.
Motivo:
- aumentar reprodutibilidade
- documentar o método
- facilitar comparação entre execuções

### 8. Clusterização temática
Arquivos principais:
- [`pipeline/orchestrator.py`](/home/murilo/Documentos/RevisaoTecnica/pipeline/orchestrator.py)
- [`report/generator.py`](/home/murilo/Documentos/RevisaoTecnica/report/generator.py)

As patentes passaram a ser agrupadas por tema para síntese.
Motivo:
- a revisão deixa de ser uma lista plana
- o relatório passa a mostrar tendências

### 9. Ablation comparável
Arquivos principais:
- [`pipeline/ablation.py`](/home/murilo/Documentos/RevisaoTecnica/pipeline/ablation.py)
- [`benchmarks/ablation_benchmark.json`](/home/murilo/Documentos/RevisaoTecnica/benchmarks/ablation_benchmark.json)

Foi criado um harness que executa variantes fixas e gera comparação automática.
Motivo:
- medir o ganho real de cada feature
- separar melhoria arquitetural de efeito casual

### 10. Cache persistente do LLM
Arquivos principais:
- [`evaluator/llm_evaluator.py`](/home/murilo/Documentos/RevisaoTecnica/evaluator/llm_evaluator.py)
- [`config.py`](/home/murilo/Documentos/RevisaoTecnica/config.py)

Foi adicionado cache em disco por modelo e prompt.
Motivo:
- reduzir chamadas repetidas
- acelerar reexecuções
- preservar respostas úteis entre runs

### 11. Métricas estruturadas por etapa
Arquivos principais:
- [`pipeline/orchestrator.py`](/home/murilo/Documentos/RevisaoTecnica/pipeline/orchestrator.py)
- [`report/generator.py`](/home/murilo/Documentos/RevisaoTecnica/report/generator.py)

O pipeline agora registra `stage_metrics` com duração, status e volume por etapa.
Motivo:
- dar visibilidade sobre gargalos
- permitir comparação quantitativa entre versões
- alimentar análise de ablation com dados mais fortes

### 12. Testes arquiteturais e de regressão
Arquivo principal: [`tests/test_architecture.py`](/home/murilo/Documentos/RevisaoTecnica/tests/test_architecture.py)

Foram adicionados testes para:
- contrato de features
- memória e slots
- roteador
- serialização do estado
- gate de rascunho vazio
- cache em disco
- relatório com métricas por etapa e cache

Motivo:
- evitar regressão em partes estruturais
- ter proteção mínima antes de rodar modelos caros

## O Que Ainda Faz Sentido Melhorar

### Prioridade alta
1. `Observabilidade mais rica`
- Expandir métricas por rota, por fonte e por tipo de falha.

### Prioridade média
2. `Benchmarks maiores e versionados`
- Mais casos do domínio e mais diversidade semântica.

3. `Logger estruturado no lugar de prints`
- Facilita debug, automação e observabilidade.

4. `Ablation paralelo`
- Rodar variantes em paralelo quando a infraestrutura permitir.

### Prioridade baixa
5. `Router mais sofisticado`
- Política baseada em utilidade/custo.

6. `Configuração por perfis`
- Expor presets completos para perfis de análise diferentes.

## Conclusão

O sistema já saiu da fase de fluxo único e passou a ter:
- método
- rastreabilidade
- memória operacional
- cache persistente
- métricas estruturadas
- comparação experimental
- proteção contra saída vazia

O próximo ganho relevante não é “mais um prompt”.
É melhorar:
- medição
- cache
- regressão
- observabilidade
