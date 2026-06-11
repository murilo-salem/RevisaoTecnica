# 📋 Relatório de Análise de Patentes

**Data:** 11/06/2026 10:44:14
**Busca:** `carbon dioxide`
**Total de patentes encontradas:** 9
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

- **Total bruto coletado:** 9
- **Patentes únicas:** 9
- **Duplicatas removidas:** 0
- **Triadas:** 0
- **Incluídas:** 0
- **Em revisão manual:** 9
- **Excluídas:** 0
- **Extrações completas:** 0
- **Sem abstract/snippet:** 0
- **Sem ID:** 0
- **Identidade por conteúdo:** 0
- **Identidade fallback:** 0
- **Duplicatas por família removidas:** 0
- **Falhas de triagem LLM:** 9
- **Falhas totais LLM:** 0

## 🧭 Fluxo PRISMA-Like

- **Identificação:** 9 bruto(s), 9 único(s), 0 duplicata(s) removida(s)
- **Triagem:** 0 triado(s), 0 incluído(s), 9 em revisão, 0 excluído(s)
- **Elegibilidade:** 0 extração(ões) completa(s), 9 revisão(ões) manual(is), 0 adiada(s)
- **Cobertura:** 0 sem abstract/snippet, 0 sem ID
- **Síntese:** 0 registro(s) analisado(s)

## 🧠 Contexto Compartilhado

- **Top patentes no contexto:** 0
- **Clusters no contexto:** 0
- **Roteamento agregado:** 1 rota(s)
- **Slots ativos:** N/A

## ⏱️ Métricas por Etapa

| Etapa | Status | Duração | Itens | Detalhes |
|---|---|---:|---:|---|
| setup | degraded | 30.04s | 1 | Verificação do modelo Ollama |
| search | ok | 36.69s | 9 | 9 patentes únicas após dedupe |
| screening | skipped | 0.00s | 9 | LLM indisponível |
| comparative_analysis | skipped | 0.00s | 9 | LLM indisponível para síntese comparativa |
| whitespace_analysis | skipped | 0.00s | 0 | Whitespace analysis sem corpus elegível |
| reporting | ok | 0.00s | 9 | Relatórios Markdown e JSON |
| finalization | ok | 0.00s | 8 | Persistência de artefatos e estado |

## 🌐 Diagnósticos de Coleta

### GooglePatents

- Nenhum sinal relevante detectado.

### Patentscope

- **blocked_or_captcha**: Sinal de bloqueio/CAPTCHA detectado no Patentscope.
- **jsf_empty_results**: Nenhum resultado em result.jsf para query: carbon dioxide
- **discovery_empty**: DuckDuckGo não retornou links para Patentscope.

## 📡 Telemetria do LLM

- **Degradado:** não
- **Falhas totais:** 0
- **Falhas consecutivas:** 0

### healthcheck

- **Chamadas:** 1
- **Sucessos:** 0
- **Falhas:** 1
- **Retries:** 0
- **Cache hits:** 0
- **Pulos por degradação:** 0
- **Latência média:** 30.03s
- **Latência máxima:** 30.03s

## 🔎 Observabilidade Estruturada

### Rotas

- **unrouted**: total=9, include=0, review=9, exclude=0, llm_errors=9

### Fontes

- **GooglePatents**: bruto=9, duração=28.64s, diagnósticos=nenhum
- **Patentscope**: bruto=0, duração=8.03s, diagnósticos=blocked_or_captcha=1, discovery_empty=1, jsf_empty_results=1

### Falhas

- **Erros de execução:** 0
- **Registros com erro de LLM:** 9
- **Falhas totais do LLM:** 0
- **LLM por operação:** healthcheck(falhas=1, retries=0, skips=0)
- **Scraper por tipo de sinal:** blocked_or_captcha=1, discovery_empty=1, jsf_empty_results=1

## 📊 Resumo Executivo

**Score médio de relevância:** 0.0/10

| # | Patente | Score | Inovação | Domínio |
|---|---------|-------|----------|---------|
| 1 | [US20220072471A1](https://patents.google.com/patent/US20220072471A1/en) — Direct carbon dioxide capture from air | 🔴 0.0 (review) | N/A | N/A |
| 2 | [WO2025230882A1](https://patents.google.com/patent/WO2025230882A1/en) — Capture and release of carbon dioxide using electrogenerated... | 🔴 0.0 (review) | N/A | N/A |
| 3 | [US7132090B2](https://patents.google.com/patent/US7132090B2/en) — Sequestration of carbon dioxide | 🔴 0.0 (review) | N/A | N/A |
| 4 | [US8119091B2](https://patents.google.com/patent/US8119091B2/en) — Carbon dioxide capture | 🔴 0.0 (review) | N/A | N/A |
| 5 | [US20240228419A1](https://patents.google.com/patent/US20240228419A1/en) — The production of formic acid or formaldehyde from carbon di... | 🔴 0.0 (review) | N/A | N/A |
| 6 | [US8500855B2](https://patents.google.com/patent/US8500855B2/en) — System and method for carbon dioxide capture and sequestrati... | 🔴 0.0 (review) | N/A | N/A |
| 7 | [US20260008008A1](https://patents.google.com/patent/US20260008008A1/en) — Method and apparatus for carbon dioxide sequestration | 🔴 0.0 (review) | N/A | N/A |
| 8 | [US20240252980A1](https://patents.google.com/patent/US20240252980A1/en) — Direct air capture reactor systems and related methods of tr... | 🔴 0.0 (review) | N/A | N/A |
| 9 | [WO2022235708A1](https://patents.google.com/patent/WO2022235708A1/en) — Systems and methods for capturing carbon dioxide and regener... | 🔴 0.0 (review) | N/A | N/A |

---

## 🔍 Análise Detalhada das Patentes

### 1. Direct carbon dioxide capture from air

| Campo | Valor |
|-------|-------|
| **Record ID** | `rec_bf9199489578` |
| **Family ID** | `family:450006d06fd5358f368f1f6d3359139d138f6a20` |
| **ID** | `US20220072471A1` |
| **Inventores** | Hans De Neve, Wilhelmus Jozef SOPPE, Johannis Alouisius Zacharias Pieterse, Gerard Douwe Elzinga, Cornelis Hendrikus Frijters, Catharina Henriette Maria Van Der Werf |
| **Titular** | Nederlandse Organisatie voor Toegepast Natuurwetenschappelijk Onderzoek TNO |
| **Data** | 2022-03-10 |
| **Fonte** | Google Patents |
| **URL** | [US20220072471A1](https://patents.google.com/patent/US20220072471A1/en) |
| **Triagem** | review |
| **Rota** | N/A |
| **Motivo da rota** | N/A |
| **Score de Triagem** | 0.0/10 |
| **Score de Relevância** | 0.0/10 |
| **Nível de Inovação** | N/A |
| **Domínio Técnico** | N/A |
| **Cluster Temático** | N/A |
| **Papel do CO2** | N/A |
| **Papel do Armazenamento** | N/A |
| **Limite Sistêmico** | N/A |
| **Tipo de Ciclo** | N/A |
| **Fonte/Sumidouro Térmico** | N/A |
| **Foco das Claims** | N/A |
| **Categoria de Exclusão** | N/A |
| **Confiança** | 0.00 |
| **Rerank Aplicado** | Não |
| **Motivo do Rerank** | N/A |
| **Revisão Manual** | Sim |
| **Erro LLM** | LLM indisponível. |

**Abstract:**
> AbstractThe present invention concerns a device and process for capturing CO2 from air. The device comprises (a) a membrane at least partly permeable for air comprising a solid state CO2 sorbent; (b) at least one sorption chamber; (c) at least one regeneration chamber; (d) means for transporting the membrane from the sorption chamber to the regeneration chamber and back; (e) an inlet for receiving air located on one end of the membrane and an outlet for discharging air depleted in CO2 located on the other end of the membrane in the sorption chamber, wherein the device is configured to allow air to flow from the inlet to the outlet through the membrane; (f) means for flowing stripping gas through the membrane into the regeneration chamber; (g) at least one outlet for discharging CO2, located in the regeneration chamber; and (h) heating means for heating the regeneration chamber. The device according to the invention provides an efficient and low-cost solution for capturing CO2 directly from air.

---

### 2. Capture and release of carbon dioxide using electrogenerated acids and bases

| Campo | Valor |
|-------|-------|
| **Record ID** | `rec_42a3a58fa795` |
| **Family ID** | `family:65f05e58692d724dbc3cdc7c4eac16fbfed6302c` |
| **ID** | `WO2025230882A1` |
| **Inventores** | Ian Robinson, David KOSHY, Sahag Voskian, Kyle Weldon SELF |
| **Titular** | Eleryc Inc |
| **Data** | 2025-11-06 |
| **Fonte** | Google Patents |
| **URL** | [WO2025230882A1](https://patents.google.com/patent/WO2025230882A1/en) |
| **Triagem** | review |
| **Rota** | N/A |
| **Motivo da rota** | N/A |
| **Score de Triagem** | 0.0/10 |
| **Score de Relevância** | 0.0/10 |
| **Nível de Inovação** | N/A |
| **Domínio Técnico** | N/A |
| **Cluster Temático** | N/A |
| **Papel do CO2** | N/A |
| **Papel do Armazenamento** | N/A |
| **Limite Sistêmico** | N/A |
| **Tipo de Ciclo** | N/A |
| **Fonte/Sumidouro Térmico** | N/A |
| **Foco das Claims** | N/A |
| **Categoria de Exclusão** | N/A |
| **Confiança** | 0.00 |
| **Rerank Aplicado** | Não |
| **Motivo do Rerank** | N/A |
| **Revisão Manual** | Sim |
| **Erro LLM** | LLM indisponível. |

**Abstract:**
> AbstractSystems and methods for capturing and releasing carbon dioxide at least in part via the electrochemical production of acids and/or bases are generally described. An aqueous input stream that includes a dissolved salt such as sodium chloride may be input into an electrolysis assembly to produce acidic and/or basic species. The basic species may promote capture of carbon dioxide (e.g., via direct air capture or from a point source). The acidic species may promote subsequent release of the carbon dioxide to form a carbon dioxide-rich stream. In some instances, at least some streams are concentrated and/or recycled, thereby improving overall system performance and/or efficiency.

---

### 3. Sequestration of carbon dioxide

| Campo | Valor |
|-------|-------|
| **Record ID** | `rec_654cb5b98f3f` |
| **Family ID** | `family:d8d73f30d3b0b6095a48f49ad10e337bea609922` |
| **ID** | `US7132090B2` |
| **Inventores** | Daniel Dziedzic, Kenneth B Gross, Robert A Gorski, John T Johnson |
| **Titular** | General Motors Corp |
| **Data** | 2006-11-07 |
| **Fonte** | Google Patents |
| **URL** | [US7132090B2](https://patents.google.com/patent/US7132090B2/en) |
| **Triagem** | review |
| **Rota** | N/A |
| **Motivo da rota** | N/A |
| **Score de Triagem** | 0.0/10 |
| **Score de Relevância** | 0.0/10 |
| **Nível de Inovação** | N/A |
| **Domínio Técnico** | N/A |
| **Cluster Temático** | N/A |
| **Papel do CO2** | N/A |
| **Papel do Armazenamento** | N/A |
| **Limite Sistêmico** | N/A |
| **Tipo de Ciclo** | N/A |
| **Fonte/Sumidouro Térmico** | N/A |
| **Foco das Claims** | N/A |
| **Categoria de Exclusão** | N/A |
| **Confiança** | 0.00 |
| **Rerank Aplicado** | Não |
| **Motivo do Rerank** | N/A |
| **Revisão Manual** | Sim |
| **Erro LLM** | LLM indisponível. |

**Abstract:**
> AbstractA process for selectively removing carbon dioxide from a gaseous stream by converting the carbon dioxide to a solid, stable form is provided. In a sequestration process, carbon dioxide enriched air is passed through a gas diffusion membrane to transfer the carbon dioxide to a fluid medium. The carbon dioxide rich fluid is then passed through a matrix containing a catalyst specific for carbon dioxide, which accelerates the conversion of the carbon dioxide to carbonic acid. In the final step, a mineral ion is added to the reaction so that a precipitate of carbonate salt is formed. This solid mineral precipitate can be safely stored for extended periods of time, such as by burying the precipitate in the ground or depositing the precipitate into storage sites either on land or into a body of water. An apparatus for removing carbon dioxide from a gaseous stream is also provided.

---

### 4. Carbon dioxide capture

| Campo | Valor |
|-------|-------|
| **Record ID** | `rec_bb7ef455d20e` |
| **Family ID** | `family:d74518704aba3dd93362781918a1db8751e01815` |
| **ID** | `US8119091B2` |
| **Inventores** | David Keith, Maryam Mahmoudkhani |
| **Titular** | Carbon Engineering Ltd |
| **Data** | 2012-02-21 |
| **Fonte** | Google Patents |
| **URL** | [US8119091B2](https://patents.google.com/patent/US8119091B2/en) |
| **Triagem** | review |
| **Rota** | N/A |
| **Motivo da rota** | N/A |
| **Score de Triagem** | 0.0/10 |
| **Score de Relevância** | 0.0/10 |
| **Nível de Inovação** | N/A |
| **Domínio Técnico** | N/A |
| **Cluster Temático** | N/A |
| **Papel do CO2** | N/A |
| **Papel do Armazenamento** | N/A |
| **Limite Sistêmico** | N/A |
| **Tipo de Ciclo** | N/A |
| **Fonte/Sumidouro Térmico** | N/A |
| **Foco das Claims** | N/A |
| **Categoria de Exclusão** | N/A |
| **Confiança** | 0.00 |
| **Rerank Aplicado** | Não |
| **Motivo do Rerank** | N/A |
| **Revisão Manual** | Sim |
| **Erro LLM** | LLM indisponível. |

**Abstract:**
> AbstractA method of carbon dioxide capture is disclosed. In a step (a) anhydrous sodium carbonate is separated from a first aqueous solution formed by reacting carbon dioxide and an aqueous solution of sodium hydroxide. In step (b) the anhydrous sodium carbonate is treated by causticization to generate carbon dioxide and sodium hydroxide. The first aqueous solution of step (a) is formed by scrubbing a gas containing carbon dioxide with an aqueous solution of sodium hydroxide.

---

### 5. The production of formic acid or formaldehyde from carbon dioxide

| Campo | Valor |
|-------|-------|
| **Record ID** | `rec_53f1ec4a61a1` |
| **Family ID** | `family:64e9d52fbc42dfb7ae4a8ffa96d8f2dd2b01fbb2` |
| **ID** | `US20240228419A1` |
| **Inventores** | Earl GOETHEER, Carlos SÃNCHEZ MARTÃNEZ, Maartje Sietske FEENSTRA, Lawien Feisal ZUBEIR |
| **Titular** | Nederlandse Organisatie voor Toegepast Natuurwetenschappelijk Onderzoek TNO |
| **Data** | 2024-07-11 |
| **Fonte** | Google Patents |
| **URL** | [US20240228419A1](https://patents.google.com/patent/US20240228419A1/en) |
| **Triagem** | review |
| **Rota** | N/A |
| **Motivo da rota** | N/A |
| **Score de Triagem** | 0.0/10 |
| **Score de Relevância** | 0.0/10 |
| **Nível de Inovação** | N/A |
| **Domínio Técnico** | N/A |
| **Cluster Temático** | N/A |
| **Papel do CO2** | N/A |
| **Papel do Armazenamento** | N/A |
| **Limite Sistêmico** | N/A |
| **Tipo de Ciclo** | N/A |
| **Fonte/Sumidouro Térmico** | N/A |
| **Foco das Claims** | N/A |
| **Categoria de Exclusão** | N/A |
| **Confiança** | 0.00 |
| **Rerank Aplicado** | Não |
| **Motivo do Rerank** | N/A |
| **Revisão Manual** | Sim |
| **Erro LLM** | LLM indisponível. |

**Abstract:**
> AbstractThe invention concerns a process and modular system for producing formic acid from a source of carbon dioxide. The process according to the invention comprises (a) a carbon capture step wherein a source of carbon dioxide is contacted with an alkaline solution to obtain a solution comprising carbonate and/or bicarbonate; optionally (b) subjecting the solution comprising carbonate and/or bicarbonate to alkaline water electrolysis, wherein carbonate present in the solution comprising carbonate and/or bicarbonate is converted to bicarbonate and H2O is converted into H2and O2; (c) subjecting the solution comprising carbonate and/or bicarbonate to a hydrogenation step in the presence of a catalyst to obtain a solution comprising formate; and (d) subjecting the solution comprising formate obtained in step (c) to bipolar membrane electrodialysis to obtain a concentrated formic acid solution and a recovered alkaline solution, wherein the recovered alkaline solution obtained in step (d) is recycled back to step (a). The concentrated formic acid solution obtained from step (d) may be subjected to a hydrogenation step in the presence of a hydrogenation catalyst to obtain a concentrated formaldehyde solution.

---

### 6. System and method for carbon dioxide capture and sequestration

| Campo | Valor |
|-------|-------|
| **Record ID** | `rec_1d2f62aad7c7` |
| **Family ID** | `family:247714a45dc0120aa1b837271fa4aee30a08c2c0` |
| **ID** | `US8500855B2` |
| **Inventores** | Peter Eisenberger |
| **Titular** | Individual |
| **Data** | 2013-08-06 |
| **Fonte** | Google Patents |
| **URL** | [US8500855B2](https://patents.google.com/patent/US8500855B2/en) |
| **Triagem** | review |
| **Rota** | N/A |
| **Motivo da rota** | N/A |
| **Score de Triagem** | 0.0/10 |
| **Score de Relevância** | 0.0/10 |
| **Nível de Inovação** | N/A |
| **Domínio Técnico** | N/A |
| **Cluster Temático** | N/A |
| **Papel do CO2** | N/A |
| **Papel do Armazenamento** | N/A |
| **Limite Sistêmico** | N/A |
| **Tipo de Ciclo** | N/A |
| **Fonte/Sumidouro Térmico** | N/A |
| **Foco das Claims** | N/A |
| **Categoria de Exclusão** | N/A |
| **Confiança** | 0.00 |
| **Rerank Aplicado** | Não |
| **Motivo do Rerank** | N/A |
| **Revisão Manual** | Sim |
| **Erro LLM** | LLM indisponível. |

**Abstract:**
> AbstractA method and a system to remove relatively pure carbon dioxide directly from ambient air. The method comprises generating process heat, to co-generate substantially saturated steam; alternately and repeatedly exposing a sorbent to a flow of ambient air, at substantially ambient conditions, to sorb, and therefore remove, carbon dioxide from said ambient air, and exposing the CO2-laden sorbent to a flow of the co-generated steam, at a temperature in the range of not greater than about 130Â° C, to release the carbon dioxide, thereby regenerating the sorbent, and capturing relatively pure carbon dioxide. To render this process more efficient, admix with the air a minor amount of a pre-treated effluent gas containing a higher concentration of carbon dioxide than in the atmosphere. The captured carbon dioxide can be stored for further use, or sequestered permanently. The purified carbon dioxide is useful for agriculture or chemical processes.

---

### 7. Method and apparatus for carbon dioxide sequestration

| Campo | Valor |
|-------|-------|
| **Record ID** | `rec_b16b4420296f` |
| **Family ID** | `family:47a60062849b26f723676cb1fd7c9d384a6cb13c` |
| **ID** | `US20260008008A1` |
| **Inventores** | James Warner Lawler, Corey Adam Myers |
| **Titular** | Anvil Capture Systems Inc |
| **Data** | 2026-01-08 |
| **Fonte** | Google Patents |
| **URL** | [US20260008008A1](https://patents.google.com/patent/US20260008008A1/en) |
| **Triagem** | review |
| **Rota** | N/A |
| **Motivo da rota** | N/A |
| **Score de Triagem** | 0.0/10 |
| **Score de Relevância** | 0.0/10 |
| **Nível de Inovação** | N/A |
| **Domínio Técnico** | N/A |
| **Cluster Temático** | N/A |
| **Papel do CO2** | N/A |
| **Papel do Armazenamento** | N/A |
| **Limite Sistêmico** | N/A |
| **Tipo de Ciclo** | N/A |
| **Fonte/Sumidouro Térmico** | N/A |
| **Foco das Claims** | N/A |
| **Categoria de Exclusão** | N/A |
| **Confiança** | 0.00 |
| **Rerank Aplicado** | Não |
| **Motivo do Rerank** | N/A |
| **Revisão Manual** | Sim |
| **Erro LLM** | LLM indisponível. |

**Abstract:**
> AbstractA method for sequestering carbon dioxide includes contacting a first feedstock that is a gaseous feedstock including carbon dioxide with a second feedstock comprising one or more minerals, such that at least a portion of the carbon dioxide in the first feedstock reacts with the one or more minerals in the second feedstock to form a first output including one or more carbonate minerals and a second output that is a gaseous output having a lower concentration of carbon dioxide than a concentration of carbon dioxide in the first feedstock.

---

### 8. Direct air capture reactor systems and related methods of transporting carbon dioxide

| Campo | Valor |
|-------|-------|
| **Record ID** | `rec_bad1378c89ef` |
| **Family ID** | `family:4c59dcf7ccee98a5050ed42358c17ffa2281af1a` |
| **ID** | `US20240252980A1` |
| **Inventores** | Dong Ding, Lucun WANG, Wei Wu |
| **Titular** | Battelle Energy Alliance LLC |
| **Data** | 2024-08-01 |
| **Fonte** | Google Patents |
| **URL** | [US20240252980A1](https://patents.google.com/patent/US20240252980A1/en) |
| **Triagem** | review |
| **Rota** | N/A |
| **Motivo da rota** | N/A |
| **Score de Triagem** | 0.0/10 |
| **Score de Relevância** | 0.0/10 |
| **Nível de Inovação** | N/A |
| **Domínio Técnico** | N/A |
| **Cluster Temático** | N/A |
| **Papel do CO2** | N/A |
| **Papel do Armazenamento** | N/A |
| **Limite Sistêmico** | N/A |
| **Tipo de Ciclo** | N/A |
| **Fonte/Sumidouro Térmico** | N/A |
| **Foco das Claims** | N/A |
| **Categoria de Exclusão** | N/A |
| **Confiança** | 0.00 |
| **Rerank Aplicado** | Não |
| **Motivo do Rerank** | N/A |
| **Revisão Manual** | Sim |
| **Erro LLM** | LLM indisponível. |

**Abstract:**
> AbstractA direct air capture (DAC) reactor system is disclosed and comprises electrochemical cells. One or more of the electrochemical cells comprises a cathode, an anode, and an electrolyte membrane between the cathode and the anode. The electrolyte membrane is configured to transport carbonate ions and oxygenate ions from the cathode to the anode. Additional DAC reactor systems and methods of capturing carbon dioxide from a feedstream using the reactor systems are also disclosed.

---

### 9. Systems and methods for capturing carbon dioxide and regenerating a capture solution

| Campo | Valor |
|-------|-------|
| **Record ID** | `rec_9db979686474` |
| **Family ID** | `family:efbe4325fce05ac616d6c6847912debf6efcf4fb` |
| **ID** | `WO2022235708A1` |
| **Inventores** | Andrew Logan OSTERICHER, Kyle Wayne KEMP, Douglas Edward Olmstead |
| **Titular** | Carbon Engineering Ltd |
| **Data** | 2022-11-10 |
| **Fonte** | Google Patents |
| **URL** | [WO2022235708A1](https://patents.google.com/patent/WO2022235708A1/en) |
| **Triagem** | review |
| **Rota** | N/A |
| **Motivo da rota** | N/A |
| **Score de Triagem** | 0.0/10 |
| **Score de Relevância** | 0.0/10 |
| **Nível de Inovação** | N/A |
| **Domínio Técnico** | N/A |
| **Cluster Temático** | N/A |
| **Papel do CO2** | N/A |
| **Papel do Armazenamento** | N/A |
| **Limite Sistêmico** | N/A |
| **Tipo de Ciclo** | N/A |
| **Fonte/Sumidouro Térmico** | N/A |
| **Foco das Claims** | N/A |
| **Categoria de Exclusão** | N/A |
| **Confiança** | 0.00 |
| **Rerank Aplicado** | Não |
| **Motivo do Rerank** | N/A |
| **Revisão Manual** | Sim |
| **Erro LLM** | LLM indisponível. |

**Abstract:**
> AbstractTechniques according to the present disclosure include capturing carbon dioxide from a dilute gas source with a CO2 capture solution to form a carbonate-rich capture solution; separating at least a portion of carbonate from the carbonate-rich capture solution; forming an electrodialysis (ED) feed solution; flowing a water stream and the ED feed solution to a bipolar membrane electrodialysis (BPMED) unit; applying an electric potential to the BPMED unit to form at least two ED product streams including a first ED product stream including a hydroxide; and flowing the first ED product stream to use in the capturing the carbon dioxide from the dilute gas source with the CO2 capture solution.

---

## 🧾 Fila de Revisão Manual

- rec_42a3a58fa795 (WO2025230882A1) | rota= | motivo=LLM indisponível. | erro_llm=LLM indisponível.
- rec_bb7ef455d20e (US8119091B2) | rota= | motivo=LLM indisponível. | erro_llm=LLM indisponível.
- rec_bad1378c89ef (US20240252980A1) | rota= | motivo=LLM indisponível. | erro_llm=LLM indisponível.
- rec_bf9199489578 (US20220072471A1) | rota= | motivo=LLM indisponível. | erro_llm=LLM indisponível.
- rec_b16b4420296f (US20260008008A1) | rota= | motivo=LLM indisponível. | erro_llm=LLM indisponível.
- rec_654cb5b98f3f (US7132090B2) | rota= | motivo=LLM indisponível. | erro_llm=LLM indisponível.
- rec_1d2f62aad7c7 (US8500855B2) | rota= | motivo=LLM indisponível. | erro_llm=LLM indisponível.
- rec_9db979686474 (WO2022235708A1) | rota= | motivo=LLM indisponível. | erro_llm=LLM indisponível.
- rec_53f1ec4a61a1 (US20240228419A1) | rota= | motivo=LLM indisponível. | erro_llm=LLM indisponível.

---

## ℹ️ Informações do Sistema

- **Gerado por:** Agente de Web Scraping de Patentes
- **Modelo LLM:** gemma3:27b
- **Data de geração:** 11/06/2026 10:44:14
- **Query de busca:** `carbon dioxide`
- **Status da execução:** completed
- **Tempo total:** 66.7s
- **LLM disponível:** não
- **Fila de revisão manual:** 9 itens
- **Snapshot hash:** `0c5668a0e4559e9e2958654e8e9bcd9126c26ac04f9fec68dcecd05624b84c88`
- **Features habilitadas:** require_evidence, enable_thematic_clusters, enable_structural_roles, enable_screening_rerank, enable_prisma, enable_snapshot, enable_comparative_analysis, enable_whitespace_analysis, enable_manual_review_queue
- **Features desabilitadas:** nenhum
- **Versão do pipeline:** 1.1
- **Thresholds snapshot:** include=7.0, review=4.5
- **Cache LLM:** 0 hits, 0 misses, 27 entradas
- **Status do rascunho:** blocked
- **Avisos do rascunho:** 1