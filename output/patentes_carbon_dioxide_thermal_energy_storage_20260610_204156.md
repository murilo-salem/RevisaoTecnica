# 📋 Relatório de Análise de Patentes

**Data:** 10/06/2026 20:41:56
**Busca:** `carbon dioxide thermal energy storage`
**Total de patentes encontradas:** 2
**Modelo de avaliação:** gemma3:27b

---

## 🧭 Protocolo Metodológico

- **Versão:** 1.0
- **Fontes:** Google Patents, Patentscope
- **Etapas:** identification, deduplication, screening, manual_review, full_extraction, synthesis
- **Threshold inclusão:** 7.0
- **Threshold revisão:** 4.5
- **Máximo em revisão manual:** 20

**Critérios de inclusão**
- Alinhamento claro com a query ou seus sinônimos técnicos.
- Documento com título, resumo ou snippet suficientes para análise.
- Potencial técnico relevante para o domínio pesquisado.

**Critérios de exclusão**
- Documentos sem relação técnica com a query.
- Duplicatas de outra fonte ou publicação equivalente.
- Registro sem metadados mínimos para avaliação.

## 📐 Cobertura e Seleção

- **Total bruto coletado:** 2
- **Patentes únicas:** 2
- **Duplicatas removidas:** 0
- **Triadas:** 2
- **Incluídas:** 0
- **Em revisão manual:** 1
- **Excluídas:** 1
- **Extrações completas:** 1
- **Sem abstract/snippet:** 0
- **Sem ID:** 0
- **Identidade por conteúdo:** 0
- **Identidade fallback:** 0
- **Duplicatas por família removidas:** 0
- **Falhas de triagem LLM:** 0
- **Falhas totais LLM:** 0

## 🧭 Fluxo PRISMA-Like

- **Identificação:** 2 bruto(s), 2 único(s), 0 duplicata(s) removida(s)
- **Triagem:** 2 triado(s), 0 incluído(s), 1 em revisão, 1 excluído(s)
- **Elegibilidade:** 1 extração(ões) completa(s), 1 revisão(ões) manual(is), 0 adiada(s)
- **Cobertura:** 0 sem abstract/snippet, 0 sem ID
- **Síntese:** 1 registro(s) analisado(s)

## 🧠 Contexto Compartilhado

- **Top patentes no contexto:** 0
- **Clusters no contexto:** 0
- **Roteamento agregado:** 2 rota(s)
- **Slots ativos:** N/A

## ⏱️ Métricas por Etapa

| Etapa | Status | Duração | Itens | Detalhes |
|---|---|---:|---:|---|
| setup | ok | 6.66s | 1 | Verificação do modelo Ollama |
| search | ok | 33.01s | 2 | 2 patentes únicas após dedupe |
| screening | ok | 726.39s | 2 | 0 incluídas, 1 revisão |
| comparative_analysis | ok | 503.25s | 2 | Síntese comparativa gerada |
| whitespace_analysis | ok | 0.00s | 2 | Whitespace analysis estruturada gerada |
| reporting | ok | 0.00s | 2 | Relatórios Markdown e JSON |
| finalization | ok | 0.00s | 8 | Persistência de artefatos e estado |

## 🌐 Diagnósticos de Coleta

### GooglePatents

- Nenhum sinal relevante detectado.

### Patentscope

- **discovery_empty**: DuckDuckGo não retornou links para Patentscope.
- **layout_break**: Não foi possível extrair o título da página de detalhe do Patentscope.
- **layout_break**: Não foi possível extrair o título da página de detalhe do Patentscope.

## 📡 Telemetria do LLM

- **Degradado:** não
- **Falhas totais:** 0
- **Falhas consecutivas:** 0

### healthcheck

- **Chamadas:** 1
- **Sucessos:** 1
- **Falhas:** 0
- **Retries:** 0
- **Cache hits:** 0
- **Pulos por degradação:** 0
- **Latência média:** 6.66s
- **Latência máxima:** 6.66s

### screening

- **Chamadas:** 2
- **Sucessos:** 2
- **Falhas:** 0
- **Retries:** 0
- **Cache hits:** 0
- **Pulos por degradação:** 0
- **Latência média:** 154.714s
- **Latência máxima:** 162.386s

### rerank

- **Chamadas:** 1
- **Sucessos:** 1
- **Falhas:** 0
- **Retries:** 0
- **Cache hits:** 0
- **Pulos por degradação:** 0
- **Latência média:** 127.135s
- **Latência máxima:** 127.135s

### evaluation

- **Chamadas:** 1
- **Sucessos:** 1
- **Falhas:** 0
- **Retries:** 0
- **Cache hits:** 0
- **Pulos por degradação:** 0
- **Latência média:** 289.829s
- **Latência máxima:** 289.829s

### comparative

- **Chamadas:** 1
- **Sucessos:** 1
- **Falhas:** 0
- **Retries:** 0
- **Cache hits:** 0
- **Pulos por degradação:** 0
- **Latência média:** 503.25s
- **Latência máxima:** 503.25s

## 🔎 Observabilidade Estruturada

### Rotas

- **manual_review**: total=1, include=0, review=1, exclude=0, llm_errors=0
- **screen_only**: total=1, include=0, review=0, exclude=1, llm_errors=0

### Fontes

- **GooglePatents**: bruto=2, duração=6.66s, diagnósticos=nenhum
- **Patentscope**: bruto=0, duração=26.36s, diagnósticos=discovery_empty=1, layout_break=2

### Falhas

- **Erros de execução:** 0
- **Registros com erro de LLM:** 0
- **Falhas totais do LLM:** 0
- **LLM por operação:** comparative(falhas=0, retries=0, skips=0), evaluation(falhas=0, retries=0, skips=0), healthcheck(falhas=0, retries=0, skips=0), rerank(falhas=0, retries=0, skips=0), screening(falhas=0, retries=0, skips=0)
- **Scraper por tipo de sinal:** discovery_empty=1, layout_break=2

## 📊 Resumo Executivo

**Score médio de relevância:** 0.0/10

| # | Patente | Score | Inovação | Domínio |
|---|---------|-------|----------|---------|
| 1 | [WO2024040002A1](https://patents.google.com/patent/WO2024040002A1/en) — System and method of co2 thermal swing adsorption with wet r... | 🟡 4.9 (review) | Incremental | Separação e Captura de Gases |
| 2 | [US20250122779A1](https://patents.google.com/patent/US20250122779A1/en) — Multi-well pad storage of h2 and/or nh3 with simultaneous co... | 🔴 0.0 (exclude) | N/A | Armazenamento Geológico, Produção de Hidrogênio |

---

## 🔍 Análise Detalhada das Patentes

### 1. Multi-well pad storage of h2 and/or nh3 with simultaneous co2 sequestration

| Campo | Valor |
|-------|-------|
| **Record ID** | `rec_4fd359f22bee` |
| **Family ID** | `family:2a17b7a90959b2781bfcd521c9358339a9e2c1a7` |
| **ID** | `US20250122779A1` |
| **Inventores** | Mariel Taylor Schottenfeld |
| **Titular** | Air Products and Chemicals Inc |
| **Data** | 2025-04-17 |
| **Fonte** | Google Patents |
| **URL** | [US20250122779A1](https://patents.google.com/patent/US20250122779A1/en) |
| **Triagem** | exclude |
| **Rota** | screen_only |
| **Motivo da rota** | Patente excluída na triagem. |
| **Score de Triagem** | 2.8/10 |
| **Score de Relevância** | 0.0/10 |
| **Nível de Inovação** | N/A |
| **Domínio Técnico** | Armazenamento Geológico, Produção de Hidrogênio |
| **Cluster Temático** | Sequestro de CO2 e Armazenamento Subterrâneo de Hidrogênio |
| **Papel do CO2** | capture_process_stream |
| **Papel do Armazenamento** | implicit_or_support_storage |
| **Limite Sistêmico** | process_integration |
| **Tipo de Ciclo** | not_clear |
| **Fonte/Sumidouro Térmico** | not_clear |
| **Foco das Claims** | process_integration |
| **Categoria de Exclusão** | industrial_heat_adjacent |
| **Confiança** | 0.73 |
| **Rerank Aplicado** | Não |
| **Motivo do Rerank** | N/A |
| **Revisão Manual** | Não |
| **Erro LLM** | N/A |

**Abstract:**
> AbstractDisclosed herein are systems and methods of gas sequestration of carbon dioxide from a fossil-fueled hydrogen production plant. The method includes producing at least hydrogen and carbon dioxide above ground from a fossil-fueled hydrogen production plant, injecting at least a portion of the hydrogen and carbon dioxide produced from the fossil-fueled hydrogen production plant into a geological hydrogen storage unit and a geological carbon dioxide storage unit, respectively, wherein the portion of the carbon dioxide is injected concurrently with the portion of the hydrogen. The injection of the portion of carbon dioxide and hydrogen underground are performed through carbon dioxide injection well(s) and hydrogen injection well(s), respectively, wherein a hydrogen injection wellhead(s) and a carbon dioxide injection wellhead(s) are located on a multi-well pad proximate the fossil-fueled hydrogen production plant.

**Evidências citadas:**
> “producing at least hydrogen and carbon dioxide above ground from a fossil-fueled hydrogen production plant”
> “injecting at least a portion of the hydrogen and carbon dioxide produced from the fossil-fueled hydrogen production plant into a geological hydrogen storage unit and a geological carbon dioxide storage unit, respectively”

---

### 2. System and method of co2 thermal swing adsorption with wet regeneration and hot drying

| Campo | Valor |
|-------|-------|
| **Record ID** | `rec_5383df610488` |
| **Family ID** | `family:a031c3f758b89c7bee7020508162b0caf2dead4e` |
| **ID** | `WO2024040002A1` |
| **Inventores** | Paul M. Dunn |
| **Titular** | Enhanced Energy Group LLC |
| **Data** | 2024-02-22 |
| **Fonte** | Google Patents |
| **URL** | [WO2024040002A1](https://patents.google.com/patent/WO2024040002A1/en) |
| **Triagem** | review |
| **Rota** | manual_review |
| **Motivo da rota** | Triagem indicou revisão humana. |
| **Score de Triagem** | 5.0/10 |
| **Score de Relevância** | 4.9/10 |
| **Nível de Inovação** | Incremental |
| **Domínio Técnico** | Separação e Captura de Gases |
| **Cluster Temático** | Adsorção Térmica de CO2 com Regeneração Otimizada |
| **Papel do CO2** | capture_process_stream |
| **Papel do Armazenamento** | implicit_or_support_storage |
| **Limite Sistêmico** | process_integration |
| **Tipo de Ciclo** | thermal_swing_adsorption |
| **Fonte/Sumidouro Térmico** | general_thermal_management |
| **Foco das Claims** | process_integration |
| **Categoria de Exclusão** | None |
| **Confiança** | 0.65 |
| **Rerank Aplicado** | Sim |
| **Motivo do Rerank** | reranked:decision_confirmed |
| **Revisão Manual** | Sim |
| **Erro LLM** | N/A |

**Abstract:**
> AbstractA capture vessel is provided that is configured to capture carbon dioxide (CO2) according to a thermal swing adsorption (TSA) process. The capture vessel includes capture media that are configured to adsorb CO2from an exhaust gas during a CO2capture stage to produce a first N2gas that exits the capture vessel, receive a mixed stream of CO2and water vapor during a wet regeneration stage, adsorb water from the mixed stream of CO2and water vapor and release adsorbed CO2during the wet regeneration stage to produce a CO2stream, receive a first heated N2gas and release adsorbed water due to evaporation caused by the first heated N2gas during a drying stage, and receive a cooled gas during a cooling stage such that an absorption capacity of the capture media for CO2capture is increased for a next CO2capture stage.

**Avaliação do LLM:**
Esta patente descreve um sistema e método de adsorção térmica de CO2 (TSA) com regeneração úmida e secagem a quente. O sistema utiliza um leito de captura para adsorver CO2 de um gás de exaustão, regenerando o material adsorvente através de um processo que envolve etapas úmidas e secas com diferentes temperaturas.

**Extração Estruturada:**
- **Problema:** A eficiência da captura de CO2 por adsorção térmica é limitada pela necessidade de regenerar o material adsorvente, o que requer energia e pode levar à degradação do material.
- **Solução:** A patente propõe um processo TSA que combina regeneração úmida e secagem a quente para otimizar a regeneração do material adsorvente, reduzir o consumo de energia e aumentar a capacidade de absorção de CO2.
- **Maturidade:** Intermediária

**Achados-chave:**
- O uso de regeneração úmida permite a adsorção de água do fluxo de CO2, liberando CO2 e reduzindo a carga térmica na etapa de secagem.
- A secagem com gás N2 aquecido evapora a água adsorvida, regenerando o material adsorvente.
- O resfriamento do leito de captura aumenta a capacidade de absorção de CO2 para o próximo ciclo.

**Vantagens alegadas:**
- Maior eficiência na captura de CO2.
- Redução do consumo de energia no processo de regeneração.
- Aumento da capacidade de absorção do material adsorvente.

**Limitações:**
- O sistema pode ser complexo devido à necessidade de controlar diferentes etapas de temperatura e umidade.
- A eficiência do processo pode depender das características do gás de exaustão e do material adsorvente.

**Aplicações potenciais:**
- Captura de CO2 de fontes industriais.
- Remoção de CO2 de gases de combustão.
- Sistemas de purificação de gás.

**Evidências citadas:**
> “capture media that are configured to adsorb CO2from an exhaust gas during a CO2capture stage”
> “receive a mixed stream of CO2and water vapor during a wet regeneration stage, adsorb water from the mixed stream of CO2and water vapor and release adsorbed CO2during the wet regeneration stage”

---

## 🧾 Fila de Revisão Manual

- rec_5383df610488 (WO2024040002A1) | rota=manual_review | motivo=Triagem indicou revisão humana. | erro_llm=N/A

---

## 🔬 Análise Comparativa

### 1. Panorama Geral

- O conjunto comparativo agrega 2 patente(s) e nao deve ser tratado como bloco homogeneo: ha um nucleo direto, fronteiras tecnicas em revisao e adjacencias uteis apenas para delimitar whitespace [IDs: WO2024040002A1, US20250122779A1]
- O subgrupo mais diretamente alinhado ao núcleo da query é WO2024040002A1, com foco em armazenamento de CO2, compressão/expansão e controle termodinâmico do meio armazenado [IDs: WO2024040002A1]
- WO2024040002A1 formam a fronteira tecnica: sao casos proximos do problema, mas ainda ambiguos quanto ao papel exato do CO2 no armazenamento ou na funcao arquitetural central [IDs: WO2024040002A1]
- WO2024040002A1, US20250122779A1 entram como adjacencia exploratoria: tratam CO2 principalmente como fluido de trabalho em transferencia termica ou distribuicao de energia, de modo que ajudam a delimitar combinacoes pouco cobertas sem virar evidencia de cobertura consolidada [IDs: WO2024040002A1, US20250122779A1]
- A mencao a armazenamento subterraneo ou subaquatico aparece apenas em US20250122779A1 e nao deve ser generalizada para todo o conjunto comparativo [IDs: US20250122779A1]

## Análise Comparativa de Patentes: Armazenamento de Energia Térmica com Dióxido de Carbono

### 2. Tendências Identificadas

*   Integração de CO2 em processos de captura e regeneração com ciclos térmicos, visando otimizar a eficiência energética. [IDs: WO2024040002A1]
*   Utilização de CO2 como subproduto em sistemas de armazenamento de hidrogênio, com foco no sequestro e não no armazenamento térmico. [IDs: US20250122779A1]
*   Ênfase em sistemas de processamento integrados, onde o CO2 desempenha um papel em múltiplos estágios do processo. [IDs: WO2024040002A1, US20250122779A1]

### 3. Whitespaces e Oportunidades

- Gestao termica transiente, subresfriamento e acoplamentos com captura/reatores aparecem de forma lateral; isso sugere oportunidade em claims de controle, operacao multi-regime e integracao de processo ainda pouco amarradas ao armazenamento central [IDs: WO2024040002A1]
- As patentes em review delimitam fronteiras tecnicas onde o papel do CO2 ainda esta ambiguo entre meio armazenado, fluido de trabalho e interface de troca termica; esse tipo de ambiguidade costuma ser um bom proxy para whitespace exploravel com recorte arquitetural mais especifico [IDs: WO2024040002A1, US20250122779A1]

### 4. Recomendações

- Priorizar arquiteturas centradas em armazenamento explícito de CO2 e controle termodinâmico rigoroso [IDs: WO2024040002A1]

### 5. Ranking Final

1. **WO2024040002A1** — armazenamento aparece mais como subsistema de apoio; ênfase em refrigeração/sub-resfriamento, mais adjacente ao núcleo da query; score 4.9/10 [IDs: WO2024040002A1]
2. **US20250122779A1** — armazenamento aparece mais como subsistema de apoio; armazenamento subterrâneo aparece como subsistema de suporte; score 0.0/10 [IDs: US20250122779A1]

### 6. Mapa de Evidências por ID

- **Adsorção Térmica de CO2 com Regeneração Otimizada** [IDs: WO2024040002A1]
- **Sequestro de CO2 e Armazenamento Subterrâneo de Hidrogênio** [IDs: US20250122779A1]

### 7. Ranking por ID

1. **WO2024040002A1** — score 4.9/10 [IDs: WO2024040002A1]
2. **US20250122779A1** — score 0.0/10 [IDs: US20250122779A1]

---

## 🧭 Matriz de Whitespaces

- **Patentes selecionadas:** 2
- **Núcleo:** 0
- **Fronteira:** 1
- **Adjacência:** 1


---

## ℹ️ Informações do Sistema

- **Gerado por:** Agente de Web Scraping de Patentes
- **Modelo LLM:** gemma3:27b
- **Data de geração:** 10/06/2026 20:41:56
- **Query de busca:** `carbon dioxide thermal energy storage`
- **Status da execução:** completed
- **Tempo total:** 1269.3s
- **LLM disponível:** sim
- **Fila de revisão manual:** 1 itens
- **Snapshot hash:** `a7167985873b4e2d3f21cdc1113b2a89f79eb0b1cbb69da78a2d655e0b39b7d2`
- **Features habilitadas:** require_evidence, enable_thematic_clusters, enable_structural_roles, enable_screening_rerank, enable_prisma, enable_snapshot, enable_comparative_analysis, enable_whitespace_analysis, enable_manual_review_queue
- **Features desabilitadas:** nenhum
- **Versão do pipeline:** 1.1
- **Thresholds snapshot:** include=7.0, review=4.5
- **Cache LLM:** 0 hits, 5 misses, 5 entradas
- **Status do rascunho:** ready