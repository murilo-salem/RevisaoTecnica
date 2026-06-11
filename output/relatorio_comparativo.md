# Relatório Técnico Comparativo

**Projeto:** Revisão Técnica de Patentes  
**Data de consolidação:** 02/04/2026  
**Objetivo:** explicar o que foi implementado no modelo atual, por que as mudanças foram feitas e como ele se compara ao modelo antigo.

## 1. Resumo Executivo

O sistema evoluiu de um pipeline simples de busca, avaliação e relatório para uma arquitetura mais auditável, modular e comparável.  
As principais melhorias foram:

- protocolo metodológico versionado;
- triagem em duas fases;
- extração estruturada com evidências;
- fluxo PRISMA-like;
- clusterização temática;
- memória operacional em sidecar;
- roteamento por tema/profundidade;
- cache persistente de LLM;
- métricas estruturadas por etapa;
- ablation harness para comparação de variantes;
- testes de regressão arquitetural.

Na comparação com o modelo antigo, o modelo atual é mais conservador, mais rastreável e mais adequado para revisão técnica séria.  
O modelo antigo produzia um relatório narrativo mais direto, mas com pouca instrumentação e baixa capacidade de auditoria.

## 2. O Que Foi Feito No Modelo Atual

### 2.1 Protocolo metodológico versionado

Foi criado um protocolo explícito para cada execução, com:

- fontes utilizadas;
- etapas do pipeline;
- critérios de inclusão e exclusão;
- thresholds de triagem e revisão;
- versão do protocolo.

**Por que isso foi feito:**  
para tornar a execução reproduzível e para permitir comparação consistente entre runs. Em revisão técnica, a metodologia precisa ficar explícita para que o resultado seja defensável.

### 2.2 Triagem em duas fases

O processo passou a separar:

- triagem rápida;
- extração detalhada.

**Por que isso foi feito:**  
para reduzir custo de processamento, evitar gasto de LLM com itens pouco relevantes e aumentar a precisão da seleção.

### 2.3 Extração estruturada com evidência

Cada patente avaliada passou a gerar campos mais organizados:

- problema;
- solução;
- vantagens;
- limitações;
- maturidade;
- domínio técnico;
- cluster temático;
- evidências citadas;
- confiança.

**Por que isso foi feito:**  
para que o relatório não dependa apenas de resumo livre. Isso melhora auditoria, interpretação e comparação entre itens.

### 2.4 Fluxo PRISMA-like

O pipeline foi organizado em termos próximos de uma revisão sistemática:

- identificação;
- deduplicação;
- triagem;
- revisão manual;
- extração;
- síntese.

**Por que isso foi feito:**  
para trazer rastreabilidade metodológica e facilitar a justificativa do corpus final.

### 2.5 Clusterização temática

As patentes passaram a ser agrupadas por temas técnicos próximos.

**Por que isso foi feito:**  
porque a síntese temática é mais útil do que uma lista plana de patentes. Isso ajuda a enxergar tendências, lacunas e sobreposição técnica.

### 2.6 Memória operacional e router

O sistema ganhou:

- memória operacional em sidecar;
- journal append-only;
- roteamento por tema;
- contexto compartilhado para o escritor do relatório.

**Por que isso foi feito:**  
para separar estado operacional de síntese, facilitar retomada, melhorar auditoria e permitir um futuro multiagente mais sólido.

### 2.7 Cache persistente de LLM

Foi adicionado cache em disco para respostas do modelo.

**Por que isso foi feito:**  
para reduzir custo, acelerar reexecuções e dar suporte a ablation e testes repetidos.

### 2.8 Métricas estruturadas por etapa

O sistema agora registra duração e contagem por etapa:

- setup;
- search;
- screening;
- comparative_analysis;
- reporting;
- finalization.

**Por que isso foi feito:**  
para medir onde o tempo está sendo gasto e identificar gargalos reais.

### 2.9 Ablation harness

Foi criada uma infraestrutura para ligar e desligar componentes do pipeline e comparar os resultados.

**Por que isso foi feito:**  
para responder, com dados, o que realmente melhora o sistema. Sem ablation, seria difícil separar ganho real de efeito de prompt, ruído de busca ou mudança de corpus.

### 2.10 Testes de regressão

Foram adicionados testes para:

- cache LLM;
- memória;
- router;
- relatório;
- gate de rascunho vazio.

**Por que isso foi feito:**  
para evitar regressões quando o pipeline continuar evoluindo.

## 3. Comparação Entre Modelo Atual e Modelo Antigo

Os dois modelos foram executados com a mesma query:

- `carbon dioxide thermal energy storage`
- `max_results=5`

### 3.1 Comparativo métrico

| Métrica | Modelo Atual | Modelo Antigo | Leitura |
|---|---:|---:|---|
| Patentes únicas | 10 | 10 | Igual |
| Incluídas | 8 | 10 | O atual é mais seletivo |
| Em revisão manual | 1 | 0 | O atual tem gate de qualidade |
| Excluídas | 1 | 0 | O atual aplica triagem mais estrita |
| Score médio de relevância | 9.11 | 9.00 | O atual ficou ligeiramente acima |
| Tempo total | 79.65s | 77.30s | O atual é um pouco mais lento |
| Etapas registradas | 6 | 0 | O atual tem rastreabilidade operacional |
| Cache LLM | ativo | inexistente | O atual é mais eficiente em reexecuções |
| PRISMA-like | sim | não | O atual é metodologicamente superior |
| Memória operacional | sim | não | O atual suporta retomada e auditoria |
| Draft status | ready | não disponível | O atual controla qualidade do texto |
| Tamanho do relatório | 48.3 KB | 38.1 KB | O atual é mais detalhado |

### 3.2 Leitura qualitativa do modelo antigo

O modelo antigo gerava um relatório mais simples e direto, com:

- lista de patentes;
- scores;
- resumo executivo;
- narrativa comparativa mais solta.

**Pontos fortes do modelo antigo:**

- menor complexidade;
- leitura mais rápida;
- saída mais enxuta;
- análise comparativa textual mais longa nesta execução específica.

**Limitações do modelo antigo:**

- pouca auditabilidade;
- ausência de métricas por etapa;
- sem memória operacional;
- sem protocolo explícito;
- sem clusterização sistemática;
- sem fila de revisão manual;
- sem cache persistente;
- sem suporte claro a ablation.

### 3.3 Leitura qualitativa do modelo atual

O modelo atual ficou mais robusto e mais adequado para revisão técnica séria.

**Pontos fortes do modelo atual:**

- seleção mais conservadora;
- evidência citada por item;
- clusters temáticos;
- rastreabilidade do fluxo;
- métricas de execução;
- cache;
- suporte a comparação experimental;
- maior transparência metodológica.

**Limitação observada nesta execução:**

- a análise comparativa textual do LLM caiu em fallback e retornou uma mensagem curta de erro em vez de uma narrativa longa.

Isso não invalida a arquitetura nova. Apenas mostra que a camada de geração comparativa ainda depende da estabilidade do modelo externo e precisa de mais robustez ou fallback melhor.

## 4. O Que Mudou Na Prática

### Antes

- pipeline mais linear;
- relatório mais narrativo;
- pouca instrumentação;
- seleção menos conservadora;
- menor capacidade de auditoria;
- sem comparação formal de versões.

### Agora

- pipeline modular;
- seleção em etapas;
- evidência obrigatória;
- memória e router;
- comparação por ablation;
- métricas por etapa;
- relatórios mais completos;
- estado persistido;
- suporte a benchmarking.

## 5. Interpretação do Resultado

O modelo atual não é apenas uma “nova versão” do antigo. Ele é uma mudança de abordagem:

- sai de uma lógica de relatório manual/narrativa;
- entra em uma lógica de revisão técnica auditável e reprodutível.

Isso é importante porque o ganho principal não está apenas no score final das patentes.  
O ganho está em:

- saber por que uma patente entrou ou saiu;
- conseguir refazer a execução;
- comparar rodadas;
- medir custo e tempo;
- justificar decisões metodologicamente.

## 6. Recomendações Para Uso No Projeto

Para apresentação ao orientador, a leitura mais correta é:

1. o modelo antigo é útil como baseline funcional;
2. o modelo atual é a versão recomendada para evolução do projeto;
3. o diferencial do novo sistema está em rastreabilidade, modularidade e capacidade de comparação;
4. a próxima etapa ideal é rodar benchmark congelado para comparar versões em um corpus fixo.

## 7. Conclusão

A evolução do sistema foi feita para torná-lo mais científico, auditável e comparável.  
O modelo antigo cumpre o papel de baseline, mas o modelo atual oferece uma base muito mais forte para análise técnica, revisão sistemática e expansão futura para cenários multiagente.

Em resumo:

- **modelo antigo:** mais simples, menos rastreável;
- **modelo atual:** mais estruturado, mais defensável e mais útil para o objetivo do projeto.

## 8. Arquivos De Apoio

- [Relatório bruto do modelo atual](/home/murilo/Documentos/RevisaoTecnica/output/modelo_atual_relatorio.md)
- [JSON bruto do modelo atual](/home/murilo/Documentos/RevisaoTecnica/output/modelo_atual_relatorio.json)
- [Relatório bruto do modelo antigo](/home/murilo/Documentos/RevisaoTecnica/output/modelo_antigo_relatorio.md)
- [JSON bruto do modelo antigo](/home/murilo/Documentos/RevisaoTecnica/output/modelo_antigo_relatorio.json)
- [Comparativo métrico](/home/murilo/Documentos/RevisaoTecnica/output/comparacao_modelos_atual_vs_antigo.md)
