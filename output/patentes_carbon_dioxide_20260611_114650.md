# 📋 Relatório de Análise de Patentes

**Data:** 11/06/2026 11:46:50
**Busca:** `carbon dioxide`
**Total de patentes encontradas:** 19
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

- **Total bruto coletado:** 19
- **Patentes únicas:** 19
- **Duplicatas removidas:** 0
- **Triadas:** 19
- **Incluídas:** 9
- **Em revisão manual:** 1
- **Excluídas:** 9
- **Extrações completas:** 10
- **Sem abstract/snippet:** 1
- **Sem ID:** 0
- **Identidade por conteúdo:** 0
- **Identidade fallback:** 0
- **Duplicatas por família removidas:** 0
- **Falhas de triagem LLM:** 0
- **Falhas totais LLM:** 1

## 🧭 Fluxo PRISMA-Like

- **Identificação:** 19 bruto(s), 19 único(s), 0 duplicata(s) removida(s)
- **Triagem:** 19 triado(s), 9 incluído(s), 1 em revisão, 9 excluído(s)
- **Elegibilidade:** 10 extração(ões) completa(s), 2 revisão(ões) manual(is), 0 adiada(s)
- **Cobertura:** 1 sem abstract/snippet, 0 sem ID
- **Síntese:** 10 registro(s) analisado(s)

## 🧩 Síntese Temática

### Captura e Sequestro de Carbono

- **Patentes:** 2
- **Score médio:** 7.80/10
- **Confiança média:** 0.93
- **Evidências citadas:** 4
- **IDs:** US8500855B2, WO2022235708A1

### CO2 Cycle Configurations

- **Patentes:** 2
- **Score médio:** 6.70/10
- **Confiança média:** 0.47
- **Evidências citadas:** 4
- **IDs:** WO2025230882A1, US20240228419A1

### Sequestro de Carbono

- **Patentes:** 1
- **Score médio:** 8.60/10
- **Confiança média:** 0.95
- **Evidências citadas:** 2
- **IDs:** US20260008008A1

### Economic Optimization

- **Patentes:** 1
- **Score médio:** 8.20/10
- **Confiança média:** 0.95
- **Evidências citadas:** 2
- **IDs:** US20220072471A1

### Engenharia Química, Captura e Sequestro de Carbono

- **Patentes:** 1
- **Score médio:** 7.80/10
- **Confiança média:** 0.95
- **Evidências citadas:** 2
- **IDs:** US7132090B2

### Engenharia Química

- **Patentes:** 1
- **Score médio:** 7.10/10
- **Confiança média:** 0.95
- **Evidências citadas:** 2
- **IDs:** US8119091B2

## 🧠 Contexto Compartilhado

- **Top patentes no contexto:** 5
- **Clusters no contexto:** 6
- **Roteamento agregado:** 3 rota(s)
- **Slots ativos:** N/A

## ⏱️ Métricas por Etapa

| Etapa | Status | Duração | Itens | Detalhes |
|---|---|---:|---:|---|
| setup | ok | 6.98s | 1 | Verificação do modelo Ollama |
| search | ok | 85.07s | 19 | 19 patentes únicas após dedupe |
| screening | ok | 6362.29s | 19 | 9 incluídas, 2 revisão |
| comparative_analysis | degraded | 600.10s | 19 | Fallback da síntese comparativa |
| whitespace_analysis | ok | 0.00s | 11 | Whitespace analysis estruturada gerada |
| reporting | ok | 0.01s | 19 | Relatórios Markdown e JSON |
| finalization | ok | 0.00s | 8 | Persistência de artefatos e estado |

## 🌐 Diagnósticos de Coleta

### GooglePatents

- Nenhum sinal relevante detectado.

### Patentscope

- **discovery_empty**: DuckDuckGo não retornou links para Patentscope.

## 📡 Telemetria do LLM

- **Degradado:** não
- **Falhas totais:** 2
- **Falhas consecutivas:** 1

### healthcheck

- **Chamadas:** 1
- **Sucessos:** 1
- **Falhas:** 0
- **Retries:** 0
- **Cache hits:** 0
- **Pulos por degradação:** 0
- **Latência média:** 6.977s
- **Latência máxima:** 6.977s

### screening

- **Chamadas:** 19
- **Sucessos:** 19
- **Falhas:** 0
- **Retries:** 0
- **Cache hits:** 0
- **Pulos por degradação:** 0
- **Latência média:** 140.165s
- **Latência máxima:** 231.213s

### rerank

- **Chamadas:** 3
- **Sucessos:** 3
- **Falhas:** 0
- **Retries:** 0
- **Cache hits:** 0
- **Pulos por degradação:** 0
- **Latência média:** 117.428s
- **Latência máxima:** 120.711s

### evaluation

- **Chamadas:** 10
- **Sucessos:** 9
- **Falhas:** 1
- **Retries:** 0
- **Cache hits:** 0
- **Pulos por degradação:** 0
- **Latência média:** 334.686s
- **Latência máxima:** 600.103s

### comparative

- **Chamadas:** 1
- **Sucessos:** 0
- **Falhas:** 1
- **Retries:** 0
- **Cache hits:** 0
- **Pulos por degradação:** 0
- **Latência média:** 600.101s
- **Latência máxima:** 600.101s

## 🔎 Observabilidade Estruturada

### Rotas

- **deep_extraction**: total=9, include=8, review=1, exclude=0, llm_errors=1
- **screen_only**: total=9, include=0, review=0, exclude=9, llm_errors=0
- **manual_review**: total=1, include=0, review=1, exclude=0, llm_errors=0

### Fontes

- **GooglePatents**: bruto=9, duração=27.34s, diagnósticos=nenhum
- **Patentscope**: bruto=10, duração=57.73s, diagnósticos=discovery_empty=1

### Falhas

- **Erros de execução:** 1
- **Registros com erro de LLM:** 1
- **Falhas totais do LLM:** 2
- **LLM por operação:** comparative(falhas=1, retries=0, skips=0), evaluation(falhas=1, retries=0, skips=0), healthcheck(falhas=0, retries=0, skips=0), rerank(falhas=0, retries=0, skips=0), screening(falhas=0, retries=0, skips=0)
- **Scraper por tipo de sinal:** discovery_empty=1

## 📊 Resumo Executivo

**Score médio de relevância:** 7.6/10

| # | Patente | Score | Inovação | Domínio |
|---|---------|-------|----------|---------|
| 1 | [US20260008008A1](https://patents.google.com/patent/US20260008008A1/en) — Method and apparatus for carbon dioxide sequestration | 🟢 8.6 (include) | Incremental | Sequestro de Carbono |
| 2 | [US20240228419A1](https://patents.google.com/patent/US20240228419A1/en) — The production of formic acid or formaldehyde from carbon di... | 🟢 8.4 (include) | Significativa | Química, Engenharia Química |
| 3 | [US20220072471A1](https://patents.google.com/patent/US20220072471A1/en) — Direct carbon dioxide capture from air | 🟢 8.2 (include) | Significativa | Captura de Carbono |
| 4 | [US8500855B2](https://patents.google.com/patent/US8500855B2/en) — System and method for carbon dioxide capture and sequestrati... | 🟢 8.2 (include) | Significativa | Captura e Sequestro de Carbono |
| 5 | [US7132090B2](https://patents.google.com/patent/US7132090B2/en) — Sequestration of carbon dioxide | 🟢 7.8 (include) | Significativa | Engenharia Química, Captura e Sequestro de Carbono |
| 6 | [WO2022235708A1](https://patents.google.com/patent/WO2022235708A1/en) — Systems and methods for capturing carbon dioxide and regener... | 🟢 7.4 (include) | Significativa | Captura e Sequestro de Carbono |
| 7 | [US8119091B2](https://patents.google.com/patent/US8119091B2/en) — Carbon dioxide capture | 🟢 7.1 (include) | Incremental | Engenharia Química |
| 8 | [GB135599119](https://patentscope.wipo.int/search/en/detail.jsf;jsessionid=B7FF3B8F425CF49CCBA4A34522F9AFB1.wapp2nB?docId=GB135599119&_cid=P21-MQ9HVZ-13283-1) — 1. GB1429678 - APPARATUS FOR SUPPLYING LIQUID CARBON DIOXIDE | 🟡 6.5 (review) | Incremental | Fluid Dynamics & Control Systems |
| 9 | [WO2025230882A1](https://patents.google.com/patent/WO2025230882A1/en) — Capture and release of carbon dioxide using electrogenerated... | 🟡 5.0 (include) | N/A | N/A |
| 10 | [US20240252980A1](https://patents.google.com/patent/US20240252980A1/en) — Direct air capture reactor systems and related methods of tr... | 🔴 0.0 (review) | N/A | Captura de Carbono |
| 11 | [GB135354895](https://patentscope.wipo.int/search/en/detail.jsf;jsessionid=B7FF3B8F425CF49CCBA4A34522F9AFB1.wapp2nB?docId=GB135354895&_cid=P21-MQ9HVZ-13283-1) — 2. GB1171698 - Dispensing Device | 🔴 0.0 (exclude) | N/A | Engenharia Mecânica / Dispositivos de Dispensação |
| 12 | [GB135726881](https://patentscope.wipo.int/search/en/detail.jsf;jsessionid=B7FF3B8F425CF49CCBA4A34522F9AFB1.wapp2nB?docId=GB135726881&_cid=P21-MQ9HVZ-13283-1) — 3. GB1557123 - METHOD AND APPARATUS FOR REPARING EXTRACTS OF... | 🔴 0.0 (exclude) | N/A | Processamento de Alimentos/Bebidas |
| 13 | [GB135860928](https://patentscope.wipo.int/search/en/detail.jsf;jsessionid=B7FF3B8F425CF49CCBA4A34522F9AFB1.wapp2nB?docId=GB135860928&_cid=P21-MQ9HVZ-13283-1) — 4. GB2047588 - Reclamation of foundry sand | 🔴 0.0 (exclude) | N/A | Materials Science/Foundry Processes |
| 14 | [GB135595668](https://patentscope.wipo.int/search/en/detail.jsf;jsessionid=B7FF3B8F425CF49CCBA4A34522F9AFB1.wapp2nB?docId=GB135595668&_cid=P21-MQ9HVZ-13283-1) — 5. GB1426573 - WEIGHING MACHINES | 🔴 0.0 (exclude) | N/A | Engenharia Mecânica / Pesagem e Controle |
| 15 | [GB135357801](https://patentscope.wipo.int/search/en/detail.jsf;jsessionid=B7FF3B8F425CF49CCBA4A34522F9AFB1.wapp2nB?docId=GB135357801&_cid=P21-MQ9HVZ-13283-1) — 6. GB1174314 - A Dispensing Device for Gases Under Pressure. | 🔴 0.0 (exclude) | N/A | Engenharia Mecânica |
| 16 | [GB135438798](https://patentscope.wipo.int/search/en/detail.jsf;jsessionid=B7FF3B8F425CF49CCBA4A34522F9AFB1.wapp2nB?docId=GB135438798&_cid=P21-MQ9HVZ-13283-1) — 7. GB1253973 - LIQUID MOVING SYSTEMS | 🔴 0.0 (exclude) | N/A | Engenharia Mecânica, Sistemas de Controle de Fluidos |
| 17 | [GB135513929](https://patentscope.wipo.int/search/en/detail.jsf;jsessionid=B7FF3B8F425CF49CCBA4A34522F9AFB1.wapp2nB?docId=GB135513929&_cid=P21-MQ9HVZ-13283-1) — 8. GB1329637 - TEMPORARY FREEZING OF SOFT OR FLEXIBLE ARTICL... | 🔴 0.0 (exclude) | N/A | Engenharia Mecânica / Processamento de Materiais |
| 18 | [GB135308953](https://patentscope.wipo.int/search/en/detail.jsf;jsessionid=B7FF3B8F425CF49CCBA4A34522F9AFB1.wapp2nB?docId=GB135308953&_cid=P21-MQ9HVZ-13283-1) — 9. GB1125505 - Production of carbon dioxide and argon | 🔴 0.0 (exclude) | N/A | Industrial Gas Production |
| 19 | [GB135420945](https://patentscope.wipo.int/search/en/detail.jsf;jsessionid=B7FF3B8F425CF49CCBA4A34522F9AFB1.wapp2nB?docId=GB135420945&_cid=P21-MQ9HVZ-13283-1) — 10. GB1236064 - IMPROVEMENTS IN OR RELATING TO FIRE EXTINGUI... | 🔴 0.0 (exclude) | N/A | Extintores de Incêndio |

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
| **Triagem** | include |
| **Rota** | deep_extraction |
| **Motivo da rota** | Há evidência suficiente para extração detalhada. |
| **Score de Triagem** | 9.2/10 |
| **Score de Relevância** | 8.2/10 |
| **Nível de Inovação** | Significativa |
| **Domínio Técnico** | Captura de Carbono |
| **Cluster Temático** | Economic Optimization |
| **Papel do CO2** | capture_process_stream |
| **Papel do Armazenamento** | explicit_thermal_storage |
| **Limite Sistêmico** | dedicated_storage_system |
| **Tipo de Ciclo** | not_clear |
| **Fonte/Sumidouro Térmico** | power_generation |
| **Foco das Claims** | process_integration |
| **Categoria de Exclusão** | None |
| **Confiança** | 0.95 |
| **Rerank Aplicado** | Não |
| **Motivo do Rerank** | N/A |
| **Revisão Manual** | Não |
| **Erro LLM** | N/A |

**Abstract:**
> AbstractThe present invention concerns a device and process for capturing CO2 from air. The device comprises (a) a membrane at least partly permeable for air comprising a solid state CO2 sorbent; (b) at least one sorption chamber; (c) at least one regeneration chamber; (d) means for transporting the membrane from the sorption chamber to the regeneration chamber and back; (e) an inlet for receiving air located on one end of the membrane and an outlet for discharging air depleted in CO2 located on the other end of the membrane in the sorption chamber, wherein the device is configured to allow air to flow from the inlet to the outlet through the membrane; (f) means for flowing stripping gas through the membrane into the regeneration chamber; (g) at least one outlet for discharging CO2, located in the regeneration chamber; and (h) heating means for heating the regeneration chamber. The device according to the invention provides an efficient and low-cost solution for capturing CO2 directly from air.

**Avaliação do LLM:**
A patente descreve um dispositivo e processo para capturar dióxido de carbono (CO2) diretamente do ar. O dispositivo utiliza uma membrana com um sorvente sólido de CO2, alternando entre câmaras de sorção e regeneração para capturar e liberar o CO2. O sistema visa fornecer uma solução eficiente e de baixo custo para a captura direta de CO2 do ar.

**Extração Estruturada:**
- **Problema:** A necessidade de uma solução eficiente e de baixo custo para a captura direta de dióxido de carbono (CO2) do ar.
- **Solução:** A patente propõe um dispositivo que utiliza uma membrana permeável ao ar contendo um sorvente sólido de CO2. O ar flui através da membrana para a câmara de sorção, onde o CO2 é capturado. A membrana é então movida para uma câmara de regeneração, onde um gás de stripping remove o CO2 capturado, permitindo a reutilização do sorvente.
- **Maturidade:** Intermediária

**Achados-chave:**
- Utilização de uma membrana com sorvente sólido para captura de CO2.
- Alternância entre câmaras de sorção e regeneração para otimizar a eficiência.
- Integração de meios de transporte da membrana para facilitar o processo.

**Vantagens alegadas:**
- Eficiência na captura de CO2 diretamente do ar.
- Baixo custo de implementação e operação.

**Limitações:**
- Dependência da eficiência do sorvente sólido de CO2.
- Necessidade de um gás de stripping para a regeneração do sorvente.

**Aplicações potenciais:**
- Mitigação das mudanças climáticas através da redução das emissões de CO2.
- Produção de CO2 puro para aplicações industriais.

**Evidências citadas:**
> “The present invention concerns a device and process for capturing CO2 from air.”
> “The device comprises (a) a membrane at least partly permeable for air comprising a solid state CO2 sorbent;”

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
| **Triagem** | include |
| **Rota** | deep_extraction |
| **Motivo da rota** | Há evidência suficiente para extração detalhada. |
| **Score de Triagem** | 9.2/10 |
| **Score de Relevância** | 5.0/10 |
| **Nível de Inovação** | N/A |
| **Domínio Técnico** | N/A |
| **Cluster Temático** | CO2 Cycle Configurations |
| **Papel do CO2** | capture_process_stream |
| **Papel do Armazenamento** | storage_not_explicit |
| **Limite Sistêmico** | process_integration |
| **Tipo de Ciclo** | not_clear |
| **Fonte/Sumidouro Térmico** | general_thermal_management |
| **Foco das Claims** | process_integration |
| **Categoria de Exclusão** | None |
| **Confiança** | 0.00 |
| **Rerank Aplicado** | Não |
| **Motivo do Rerank** | N/A |
| **Revisão Manual** | Não |
| **Erro LLM** | N/A |

**Abstract:**
> AbstractSystems and methods for capturing and releasing carbon dioxide at least in part via the electrochemical production of acids and/or bases are generally described. An aqueous input stream that includes a dissolved salt such as sodium chloride may be input into an electrolysis assembly to produce acidic and/or basic species. The basic species may promote capture of carbon dioxide (e.g., via direct air capture or from a point source). The acidic species may promote subsequent release of the carbon dioxide to form a carbon dioxide-rich stream. In some instances, at least some streams are concentrated and/or recycled, thereby improving overall system performance and/or efficiency.

**Avaliação do LLM:**
{
    "relevance_score": 9.2,
    "summary": "Esta patente descreve sistemas e métodos para capturar e liberar dióxido de carbono utilizando a produção eletroquímica de ácidos e/ou bases. Um fluxo de entrada aquoso contendo um sal dissolvido, como cloreto de sódio, é submetido à eletrólise para gerar espécies ácidas e/ou básicas, promovendo a captura e liberação do CO2. A patente também aborda a concentração e reciclagem de fluxos para melhorar o desempenho e a eficiência do sistema.",
    "prob

**Evidências citadas:**
> Systems and methods for capturing and releasing carbon dioxide at least in part via the electrochemical production of acids and/or bases are generally described.
> The basic species may promote capture of carbon dioxide (e.g., via direct air capture or from a point source). The acidic species may promote subsequent release of the carbon dioxide to form a carbon dioxide-rich stream.

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
| **Triagem** | include |
| **Rota** | deep_extraction |
| **Motivo da rota** | Há evidência suficiente para extração detalhada. |
| **Score de Triagem** | 8.2/10 |
| **Score de Relevância** | 7.8/10 |
| **Nível de Inovação** | Significativa |
| **Domínio Técnico** | Engenharia Química, Captura e Sequestro de Carbono |
| **Cluster Temático** | Engenharia Química, Captura e Sequestro de Carbono |
| **Papel do CO2** | capture_process_stream |
| **Papel do Armazenamento** | implicit_or_support_storage |
| **Limite Sistêmico** | process_integration |
| **Tipo de Ciclo** | not_clear |
| **Fonte/Sumidouro Térmico** | not_clear |
| **Foco das Claims** | process_integration |
| **Categoria de Exclusão** | None |
| **Confiança** | 0.95 |
| **Rerank Aplicado** | Não |
| **Motivo do Rerank** | N/A |
| **Revisão Manual** | Não |
| **Erro LLM** | N/A |

**Abstract:**
> AbstractA process for selectively removing carbon dioxide from a gaseous stream by converting the carbon dioxide to a solid, stable form is provided. In a sequestration process, carbon dioxide enriched air is passed through a gas diffusion membrane to transfer the carbon dioxide to a fluid medium. The carbon dioxide rich fluid is then passed through a matrix containing a catalyst specific for carbon dioxide, which accelerates the conversion of the carbon dioxide to carbonic acid. In the final step, a mineral ion is added to the reaction so that a precipitate of carbonate salt is formed. This solid mineral precipitate can be safely stored for extended periods of time, such as by burying the precipitate in the ground or depositing the precipitate into storage sites either on land or into a body of water. An apparatus for removing carbon dioxide from a gaseous stream is also provided.

**Avaliação do LLM:**
A patente descreve um processo para remover seletivamente dióxido de carbono de um fluxo gasoso, convertendo-o em uma forma sólida e estável. O processo utiliza uma membrana de difusão gasosa e um catalisador específico para acelerar a conversão do CO2 em ácido carbônico, formando um precipitado de sal mineral que pode ser armazenado de forma segura.

**Extração Estruturada:**
- **Problema:** A necessidade de remover dióxido de carbono de fluxos gasosos de forma eficiente e segura, convertendo-o em um estado estável para armazenamento a longo prazo.
- **Solução:** A patente propõe um processo que utiliza uma membrana de difusão gasosa para transferir o CO2 para um fluido, seguido pela conversão em ácido carbônico com um catalisador e, finalmente, a precipitação como um sal mineral estável.
- **Maturidade:** Intermediária

**Achados-chave:**
- Utilização de membrana de difusão gasosa para transferência de CO2.
- Conversão de CO2 em ácido carbônico com catalisador específico.
- Formação de um precipitado de sal mineral para armazenamento seguro.

**Vantagens alegadas:**
- Conversão de CO2 em forma sólida e estável.
- Armazenamento seguro e de longo prazo do CO2 precipitado.

**Limitações:**
- Dependência de um catalisador específico para a conversão de CO2.
- Necessidade de um mineral ion para a formação do precipitado.

**Aplicações potenciais:**
- Captura de carbono em emissões industriais.
- Sequestro de carbono em processos de geração de energia.

**Evidências citadas:**
> "converting the carbon dioxide to a solid, stable form is provided."
> "a mineral ion is added to the reaction so that a precipitate of carbonate salt is formed"

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
| **Triagem** | include |
| **Rota** | deep_extraction |
| **Motivo da rota** | Há evidência suficiente para extração detalhada. |
| **Score de Triagem** | 8.2/10 |
| **Score de Relevância** | 7.1/10 |
| **Nível de Inovação** | Incremental |
| **Domínio Técnico** | Engenharia Química |
| **Cluster Temático** | Engenharia Química |
| **Papel do CO2** | capture_process_stream |
| **Papel do Armazenamento** | explicit_thermal_storage |
| **Limite Sistêmico** | process_integration |
| **Tipo de Ciclo** | not_clear |
| **Fonte/Sumidouro Térmico** | not_clear |
| **Foco das Claims** | process_integration |
| **Categoria de Exclusão** | None |
| **Confiança** | 0.95 |
| **Rerank Aplicado** | Não |
| **Motivo do Rerank** | N/A |
| **Revisão Manual** | Não |
| **Erro LLM** | N/A |

**Abstract:**
> AbstractA method of carbon dioxide capture is disclosed. In a step (a) anhydrous sodium carbonate is separated from a first aqueous solution formed by reacting carbon dioxide and an aqueous solution of sodium hydroxide. In step (b) the anhydrous sodium carbonate is treated by causticization to generate carbon dioxide and sodium hydroxide. The first aqueous solution of step (a) is formed by scrubbing a gas containing carbon dioxide with an aqueous solution of sodium hydroxide.

**Avaliação do LLM:**
A patente descreve um método para captura de dióxido de carbono utilizando carbonato de sódio anidro. O processo envolve a separação do carbonato de sódio de uma solução aquosa resultante da reação entre dióxido de carbono e hidróxido de sódio, seguido pelo tratamento do carbonato de sódio para gerar dióxido de carbono e hidróxido de sódio.

**Extração Estruturada:**
- **Problema:** A necessidade de um método eficiente para capturar dióxido de carbono de gases.
- **Solução:** A patente propõe um ciclo químico que utiliza carbonato de sódio para absorver o CO2, seguido pela regeneração do carbonato e do hidróxido de sódio, permitindo a captura contínua de CO2.
- **Maturidade:** Intermediária

**Achados-chave:**
- Utilização de carbonato de sódio anidro para captura de CO2.
- Regeneração de reagentes (carbonato de sódio e hidróxido de sódio) para um ciclo contínuo.
- O processo envolve a reação de CO2 com hidróxido de sódio.

**Vantagens alegadas:**
- Possibilidade de captura contínua de CO2.
- Regeneração de reagentes, reduzindo custos e desperdício.

**Limitações:**
- Dependência da disponibilidade de carbonato de sódio anidro.
- O processo pode ser sensível às condições operacionais (temperatura, pressão).

**Aplicações potenciais:**
- Captura de CO2 de fontes industriais.
- Mitigação de emissões de gases de efeito estufa.
- Produção de CO2 puro para outras aplicações.

**Evidências citadas:**
> A method of carbon dioxide capture is disclosed.
> In step (a) anhydrous sodium carbonate is separated from a first aqueous solution formed by reacting carbon dioxide and an aqueous solution of sodium hydroxide.

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
| **Triagem** | include |
| **Rota** | deep_extraction |
| **Motivo da rota** | Há evidência suficiente para extração detalhada. |
| **Score de Triagem** | 9.2/10 |
| **Score de Relevância** | 8.4/10 |
| **Nível de Inovação** | Significativa |
| **Domínio Técnico** | Química, Engenharia Química |
| **Cluster Temático** | CO2 Cycle Configurations |
| **Papel do CO2** | capture_process_stream |
| **Papel do Armazenamento** | explicit_thermal_storage |
| **Limite Sistêmico** | process_integration |
| **Tipo de Ciclo** | not_clear |
| **Fonte/Sumidouro Térmico** | not_clear |
| **Foco das Claims** | process_integration |
| **Categoria de Exclusão** | None |
| **Confiança** | 0.95 |
| **Rerank Aplicado** | Não |
| **Motivo do Rerank** | N/A |
| **Revisão Manual** | Não |
| **Erro LLM** | N/A |

**Abstract:**
> AbstractThe invention concerns a process and modular system for producing formic acid from a source of carbon dioxide. The process according to the invention comprises (a) a carbon capture step wherein a source of carbon dioxide is contacted with an alkaline solution to obtain a solution comprising carbonate and/or bicarbonate; optionally (b) subjecting the solution comprising carbonate and/or bicarbonate to alkaline water electrolysis, wherein carbonate present in the solution comprising carbonate and/or bicarbonate is converted to bicarbonate and H2O is converted into H2and O2; (c) subjecting the solution comprising carbonate and/or bicarbonate to a hydrogenation step in the presence of a catalyst to obtain a solution comprising formate; and (d) subjecting the solution comprising formate obtained in step (c) to bipolar membrane electrodialysis to obtain a concentrated formic acid solution and a recovered alkaline solution, wherein the recovered alkaline solution obtained in step (d) is recycled back to step (a). The concentrated formic acid solution obtained from step (d) may be subjected to a hydrogenation step in the presence of a hydrogenation catalyst to obtain a concentrated formaldehyde solution.

**Avaliação do LLM:**
A patente descreve um processo para a produção de ácido fórmico e formaldeído a partir de dióxido de carbono. O processo envolve a captura de CO2, eletrólise alcalina, hidrogenação e eletrodiálise de membrana bipolar para concentrar o ácido fórmico, com a possibilidade de conversão subsequente em formaldeído.

**Extração Estruturada:**
- **Problema:** A necessidade de um processo eficiente e sustentável para a produção de ácido fórmico e formaldeído a partir de dióxido de carbono, minimizando o impacto ambiental.
- **Solução:** A patente propõe um sistema modular que integra a captura de CO2 com eletrólise alcalina, hidrogenação catalítica e eletrodiálise de membrana bipolar para produzir ácido fórmico concentrado e, opcionalmente, formaldeído. A reciclagem da solução alcalina recuperada otimiza o processo.
- **Maturidade:** Intermediária

**Achados-chave:**
- A combinação de eletrólise alcalina e hidrogenação permite a conversão eficiente de CO2 em ácido fórmico.
- A eletrodiálise de membrana bipolar permite a concentração do ácido fórmico com recuperação da solução alcalina para reciclagem.
- O processo pode ser estendido para a produção de formaldeído a partir do ácido fórmico concentrado.

**Vantagens alegadas:**
- Produção sustentável de ácido fórmico e formaldeído a partir de CO2.
- Reciclagem da solução alcalina, reduzindo o consumo de reagentes.
- Sistema modular que permite flexibilidade e escalabilidade.

**Limitações:**
- Dependência da eficiência dos catalisadores de hidrogenação.
- Custo potencial da membrana bipolar para eletrodiálise.

**Aplicações potenciais:**
- Produção industrial de ácido fórmico para diversas aplicações (conservantes, têxteis, etc.).
- Produção industrial de formaldeído para a indústria de resinas e polímeros.

**Evidências citadas:**
> “a process and modular system for producing formic acid from a source of carbon dioxide.”
> “(a) a carbon capture step wherein a source of carbon dioxide is contacted with an alkaline solution”

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
| **Triagem** | include |
| **Rota** | deep_extraction |
| **Motivo da rota** | Há evidência suficiente para extração detalhada. |
| **Score de Triagem** | 9.2/10 |
| **Score de Relevância** | 8.2/10 |
| **Nível de Inovação** | Significativa |
| **Domínio Técnico** | Captura e Sequestro de Carbono |
| **Cluster Temático** | Captura e Sequestro de Carbono |
| **Papel do CO2** | capture_process_stream |
| **Papel do Armazenamento** | implicit_or_support_storage |
| **Limite Sistêmico** | process_integration |
| **Tipo de Ciclo** | not_clear |
| **Fonte/Sumidouro Térmico** | industrial_heat |
| **Foco das Claims** | system_architecture |
| **Categoria de Exclusão** | None |
| **Confiança** | 0.95 |
| **Rerank Aplicado** | Não |
| **Motivo do Rerank** | N/A |
| **Revisão Manual** | Não |
| **Erro LLM** | N/A |

**Abstract:**
> AbstractA method and a system to remove relatively pure carbon dioxide directly from ambient air. The method comprises generating process heat, to co-generate substantially saturated steam; alternately and repeatedly exposing a sorbent to a flow of ambient air, at substantially ambient conditions, to sorb, and therefore remove, carbon dioxide from said ambient air, and exposing the CO2-laden sorbent to a flow of the co-generated steam, at a temperature in the range of not greater than about 130Â° C, to release the carbon dioxide, thereby regenerating the sorbent, and capturing relatively pure carbon dioxide. To render this process more efficient, admix with the air a minor amount of a pre-treated effluent gas containing a higher concentration of carbon dioxide than in the atmosphere. The captured carbon dioxide can be stored for further use, or sequestered permanently. The purified carbon dioxide is useful for agriculture or chemical processes.

**Avaliação do LLM:**
A patente descreve um sistema e método para capturar dióxido de carbono diretamente do ar ambiente utilizando um sorvente. O processo envolve a exposição do sorvente ao ar para absorver o CO2 e, em seguida, a liberação do CO2 utilizando vapor gerado a partir do calor do processo, regenerando o sorvente. O CO2 capturado pode ser armazenado, utilizado em agricultura ou processos químicos.

**Extração Estruturada:**
- **Problema:** A necessidade de remover dióxido de carbono diretamente do ar ambiente de forma eficiente e com baixo consumo de energia.
- **Solução:** A patente propõe um sistema que utiliza um sorvente para capturar CO2 do ar, regenerando-o com vapor gerado pelo próprio processo, minimizando o consumo externo de energia. A adição de um gás residual pré-tratado com maior concentração de CO2 aumenta a eficiência.
- **Maturidade:** Intermediária

**Achados-chave:**
- Captura direta de CO2 do ar ambiente.
- Regeneração do sorvente com vapor gerado pelo processo.
- Utilização de gás residual para aumentar a eficiência da captura.

**Vantagens alegadas:**
- Captura de CO2 relativamente puro.
- Eficiência energética através da co-geração de vapor.
- Possibilidade de utilização ou sequestro do CO2 capturado.

**Limitações:**
- A temperatura de regeneração do sorvente é limitada a 130°C.
- Dependência da disponibilidade de um gás residual adequado.

**Aplicações potenciais:**
- Agricultura.
- Processos químicos.
- Sequestro de carbono.

**Evidências citadas:**
> A method and a system to remove relatively pure carbon dioxide directly from ambient air.
> exposing the CO2-laden sorbent to a flow of the co-generated steam, at a temperature in the range of not greater than about 130Â° C, to release the carbon dioxide, thereby regenerating the sorbent, and capturing relatively pure carbon dioxide.

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
| **Triagem** | include |
| **Rota** | deep_extraction |
| **Motivo da rota** | Há evidência suficiente para extração detalhada. |
| **Score de Triagem** | 9.2/10 |
| **Score de Relevância** | 8.6/10 |
| **Nível de Inovação** | Incremental |
| **Domínio Técnico** | Sequestro de Carbono |
| **Cluster Temático** | Sequestro de Carbono |
| **Papel do CO2** | capture_process_stream |
| **Papel do Armazenamento** | implicit_or_support_storage |
| **Limite Sistêmico** | process_integration |
| **Tipo de Ciclo** | not_clear |
| **Fonte/Sumidouro Térmico** | not_applicable |
| **Foco das Claims** | Método e aparato para sequestro de dióxido de carbono |
| **Categoria de Exclusão** | None |
| **Confiança** | 0.95 |
| **Rerank Aplicado** | Não |
| **Motivo do Rerank** | N/A |
| **Revisão Manual** | Não |
| **Erro LLM** | N/A |

**Abstract:**
> AbstractA method for sequestering carbon dioxide includes contacting a first feedstock that is a gaseous feedstock including carbon dioxide with a second feedstock comprising one or more minerals, such that at least a portion of the carbon dioxide in the first feedstock reacts with the one or more minerals in the second feedstock to form a first output including one or more carbonate minerals and a second output that is a gaseous output having a lower concentration of carbon dioxide than a concentration of carbon dioxide in the first feedstock.

**Avaliação do LLM:**
A patente descreve um método para sequestrar dióxido de carbono (CO2) através da reação com minerais. O processo envolve o contato de um fluxo gasoso contendo CO2 com minerais, formando carbonatos e reduzindo a concentração de CO2 no fluxo gasoso resultante. O sistema visa a remoção e conversão de CO2 em formas mais estáveis.

**Extração Estruturada:**
- **Problema:** A patente aborda o problema da alta concentração de dióxido de carbono na atmosfera e a necessidade de métodos eficazes para seu sequestro e mitigação.
- **Solução:** A patente propõe um método que utiliza a reação de CO2 com minerais para formar carbonatos, convertendo o CO2 em um estado sólido e estável, removendo-o efetivamente do fluxo gasoso.
- **Maturidade:** Intermediária

**Achados-chave:**
- A reação entre CO2 e minerais resulta na formação de carbonatos.
- O método reduz a concentração de CO2 em um fluxo gasoso.
- A utilização de minerais como reagentes permite o sequestro de CO2.

**Vantagens alegadas:**
- Sequestro permanente de CO2 através da mineralização.
- Redução da concentração de CO2 em fluxos gasosos.

**Limitações:**
- A eficácia do processo pode depender da disponibilidade e reatividade dos minerais.
- O processo pode gerar resíduos sólidos de carbonato.

**Aplicações potenciais:**
- Captura de carbono em indústrias emissoras.
- Remoção de CO2 de gases de combustão.
- Sequestro de carbono em larga escala.

**Evidências citadas:**
> A method for sequestering carbon dioxide includes contacting a first feedstock that is a gaseous feedstock including carbon dioxide with a second feedstock comprising one or more minerals
> at least a portion of the carbon dioxide in the first feedstock reacts with the one or more minerals in the second feedstock to form a first output including one or more carbonate minerals

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
| **Rota** | deep_extraction |
| **Motivo da rota** | Há evidência suficiente para extração detalhada. |
| **Score de Triagem** | 9.2/10 |
| **Score de Relevância** | 0.0/10 |
| **Nível de Inovação** | N/A |
| **Domínio Técnico** | Captura de Carbono |
| **Cluster Temático** | Captura Direta de Ar e Eletroquímica |
| **Papel do CO2** | capture_process_stream |
| **Papel do Armazenamento** | explicit_thermal_storage |
| **Limite Sistêmico** | process_integration |
| **Tipo de Ciclo** | not_clear |
| **Fonte/Sumidouro Térmico** | not_clear |
| **Foco das Claims** | system_architecture |
| **Categoria de Exclusão** | None |
| **Confiança** | 0.95 |
| **Rerank Aplicado** | Não |
| **Motivo do Rerank** | N/A |
| **Revisão Manual** | Sim |
| **Erro LLM** | Timeout ao chamar Ollama. |

**Abstract:**
> AbstractA direct air capture (DAC) reactor system is disclosed and comprises electrochemical cells. One or more of the electrochemical cells comprises a cathode, an anode, and an electrolyte membrane between the cathode and the anode. The electrolyte membrane is configured to transport carbonate ions and oxygenate ions from the cathode to the anode. Additional DAC reactor systems and methods of capturing carbon dioxide from a feedstream using the reactor systems are also disclosed.

**Avaliação do LLM:**
A patente descreve sistemas de captura direta de ar (DAC) e métodos para transportar dióxido de carbono, alinhando-se diretamente com o termo de busca.

**Evidências citadas:**
> A direct air capture (DAC) reactor system is disclosed...
> ...methods of capturing carbon dioxide from a feedstream...

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
| **Triagem** | include |
| **Rota** | deep_extraction |
| **Motivo da rota** | Há evidência suficiente para extração detalhada. |
| **Score de Triagem** | 8.2/10 |
| **Score de Relevância** | 7.4/10 |
| **Nível de Inovação** | Significativa |
| **Domínio Técnico** | Captura e Sequestro de Carbono |
| **Cluster Temático** | Captura e Sequestro de Carbono |
| **Papel do CO2** | capture_process_stream |
| **Papel do Armazenamento** | implicit_or_support_storage |
| **Limite Sistêmico** | process_integration |
| **Tipo de Ciclo** | not_clear |
| **Fonte/Sumidouro Térmico** | not_clear |
| **Foco das Claims** | system_architecture |
| **Categoria de Exclusão** | None |
| **Confiança** | 0.90 |
| **Rerank Aplicado** | Não |
| **Motivo do Rerank** | N/A |
| **Revisão Manual** | Não |
| **Erro LLM** | N/A |

**Abstract:**
> AbstractTechniques according to the present disclosure include capturing carbon dioxide from a dilute gas source with a CO2 capture solution to form a carbonate-rich capture solution; separating at least a portion of carbonate from the carbonate-rich capture solution; forming an electrodialysis (ED) feed solution; flowing a water stream and the ED feed solution to a bipolar membrane electrodialysis (BPMED) unit; applying an electric potential to the BPMED unit to form at least two ED product streams including a first ED product stream including a hydroxide; and flowing the first ED product stream to use in the capturing the carbon dioxide from the dilute gas source with the CO2 capture solution.

**Avaliação do LLM:**
Esta patente descreve um sistema para capturar dióxido de carbono de uma fonte gasosa diluída utilizando uma solução de captura. O sistema emprega eletrodiálise bipolar para regenerar a solução de captura, separando o carbonato e formando hidróxido para reutilização no processo de captura. O objetivo é otimizar a captura e regeneração da solução, tornando o processo mais eficiente.

**Extração Estruturada:**
- **Problema:** A captura eficiente de dióxido de carbono de fontes gasosas diluídas e a regeneração da solução de captura são desafios técnicos significativos.
- **Solução:** A patente propõe um sistema que combina a captura de CO2 com uma solução de captura, seguida pela separação de carbonato via eletrodiálise bipolar (BPMED) para regenerar a solução de captura e produzir hidróxido para reutilização.
- **Maturidade:** Intermediária

**Achados-chave:**
- Utilização de eletrodiálise bipolar (BPMED) para separação de carbonato.
- Formação de hidróxido a partir da BPMED para regeneração da solução de captura.
- Integração do processo de captura com a regeneração da solução para maior eficiência.

**Vantagens alegadas:**
- Maior eficiência na captura de CO2.
- Regeneração da solução de captura com menor consumo de energia.
- Produção de hidróxido como subproduto útil.

**Limitações:**
- Dependência da eficiência da eletrodiálise bipolar.
- Custo e complexidade da implementação do sistema BPMED.
- Escalabilidade do processo pode ser um desafio.

**Aplicações potenciais:**
- Captura de carbono em usinas de energia.
- Captura de carbono em processos industriais.
- Remoção de CO2 da atmosfera.

**Evidências citadas:**
> Techniques according to the present disclosure include capturing carbon dioxide from a dilute gas source...
> ...capturing the carbon dioxide from the dilute gas source with the CO2 capture solution.

---

### 10. 1. GB1429678 - APPARATUS FOR SUPPLYING LIQUID CARBON DIOXIDE

| Campo | Valor |
|-------|-------|
| **Record ID** | `rec_8b168382e70e` |
| **Family ID** | `family:b13b8777151f45e6284fa573185962959a515629` |
| **ID** | `GB135599119` |
| **Inventores** | N/A |
| **Titular** | DISTILLERS CO; CARBON; DIOXIDE |
| **Data** | 24.03.1976 |
| **Fonte** | Patentscope |
| **URL** | [GB135599119](https://patentscope.wipo.int/search/en/detail.jsf;jsessionid=B7FF3B8F425CF49CCBA4A34522F9AFB1.wapp2nB?docId=GB135599119&_cid=P21-MQ9HVZ-13283-1) |
| **Triagem** | review |
| **Rota** | manual_review |
| **Motivo da rota** | Triagem indicou revisão humana. |
| **Score de Triagem** | 5.7/10 |
| **Score de Relevância** | 6.5/10 |
| **Nível de Inovação** | Incremental |
| **Domínio Técnico** | Fluid Dynamics & Control Systems |
| **Cluster Temático** | Controle de fluxo e reutilização de CO2 líquido em sistemas de refrigeração e aplicações industriais. |
| **Papel do CO2** | working_fluid |
| **Papel do Armazenamento** | implicit_or_support_storage |
| **Limite Sistêmico** | cycle_or_transfer_subsystem |
| **Tipo de Ciclo** | refrigeration_cycle |
| **Fonte/Sumidouro Térmico** | ambiente |
| **Foco das Claims** | system_architecture |
| **Categoria de Exclusão** | None |
| **Confiança** | 0.75 |
| **Rerank Aplicado** | Sim |
| **Motivo do Rerank** | reranked:decision_confirmed |
| **Revisão Manual** | Sim |
| **Erro LLM** | N/A |

**Abstract:**
> (EN)1429678 Automatic control of level DISTILLERS CO (CARBONDIOXIDE) Ltd 18 Jan 1974 [28 March 1973] 14925/73 Heading G3R [Also in Division F4]  In apparatus for delivering liquid CO 2  from a heat insulated reservoir 1 through a discharge pipe 5, 5' to a delivery point at 8, a container 7 is connected in the discharge pipe for removal of gaseous CO 2  through an outlet pipe 12 with a valve 11 controlled by a unit 31 which opens the valve when the gas reaches a predetermined volume in the container. As shown the gas is passed to an accumulator 14 and thence to a cooler 17, and is returned as liquid to the reservoir 1. Simpler installations are, however, envisaged in which the gaseous CO 2  is vented to atmosphere or directly to the top of the reservoir. The reservoir is refrigerated by a coil 3. The delivery point is a metering jet 8 connected to a snow-making horn 9, but may alternatively be a connector for filling cylinders or the intake of a rotory pump.  The valve 11 is a solenoid valve and may be controlled by a float-operated switch. Preferably however, the container 7 has a tubular wall 22 forming the outer electrode of a coaxial capacitor, the inner electrode being formed by a perforated tube 27. The two electrodes are connected through a cable 29 to the resonance circuit of a Colpitts oscillator, Fig. 3 (not shown) in the control unit 31. When the container 7 is full of liquid CO 2 , the capacitance between the electrodes 22, 27 is enough to block the oscillator so that there is no input to an amplifying (T2), and a switching transistor (T4) controlled thereby is OFF. The emitter circuit of the transistor contains the coil of a relay (R) with normally open contacts (Ra) in series with the solenoid of the valve 11 which is therefore closed. As gaseous CO 2  collects in the container 7, the liquid level and the capacitance drop with the eventual onset of oscillation. The relay (R) is thereby closed, opening the valve 11  to vent the gas and opening auxiliary contacts (Rb) to disconnect a capacitor (C7) from the oscillator circuit. Oscillation therefore continues until the capacitance between the electrodes 22, 27 increases sufficiently, as the liquid level rises, to offset the effect of the capacitor (C7).

**Avaliação do LLM:**
Esta patente descreve um sistema para fornecer dióxido de carbono líquido a partir de um reservatório isolado termicamente, com controle automático do nível de gás. O sistema visa remover o CO2 gasoso que se acumula durante a descarga do líquido, permitindo a reutilização ou ventilação do gás.

**Extração Estruturada:**
- **Problema:** O acúmulo de CO2 gasoso durante a descarga de CO2 líquido a partir de um reservatório pode levar a ineficiências e necessidade de ventilação.
- **Solução:** A patente propõe um sistema que remove o CO2 gasoso através de um container conectado à tubulação de descarga, controlando a abertura de uma válvula para liberar o gás acumulado, que pode ser recirculado como líquido ou ventilado.
- **Maturidade:** Madura

**Achados-chave:**
- Utilização de um capacitor coaxial para detecção do nível de CO2 líquido no container.
- Controle automático da válvula de ventilação baseado na capacitância do capacitor.
- Possibilidade de recirculação do CO2 gasoso para o reservatório após resfriamento.

**Vantagens alegadas:**
- Controle preciso do nível de gás no sistema.
- Reutilização potencial do CO2 gasoso, reduzindo o desperdício.
- Adaptação a diferentes aplicações, como produção de neve ou enchimento de cilindros.

**Limitações:**
- Complexidade do sistema de controle baseado em capacitância.
- Dependência da manutenção e calibração do sensor de capacitância.
- A eficiência do resfriamento do CO2 gasoso para recirculação não é detalhada.

**Aplicações potenciais:**
- Sistemas de produção de neve artificial.
- Sistemas de enchimento de cilindros de CO2.
- Sistemas de refrigeração.

**Evidências citadas:**
> “apparatus for delivering liquid CO 2  from a heat insulated reservoir”
> “The reservoir is refrigerated by a coil 3.”

---

### 11. 2. GB1171698 - Dispensing Device

| Campo | Valor |
|-------|-------|
| **Record ID** | `rec_4de11ef09b88` |
| **Family ID** | `family:ec341320087c0ced87d61a70b2ae50b55f598166` |
| **ID** | `GB135354895` |
| **Inventores** | MOLE WALTER ERNEST |
| **Titular** | DISTILLERS CO; CARBON; DIOXIDE |
| **Data** | 26.11.1969 |
| **Fonte** | Patentscope |
| **URL** | [GB135354895](https://patentscope.wipo.int/search/en/detail.jsf;jsessionid=B7FF3B8F425CF49CCBA4A34522F9AFB1.wapp2nB?docId=GB135354895&_cid=P21-MQ9HVZ-13283-1) |
| **Triagem** | exclude |
| **Rota** | screen_only |
| **Motivo da rota** | Patente excluída na triagem. |
| **Score de Triagem** | 3.5/10 |
| **Score de Relevância** | 0.0/10 |
| **Nível de Inovação** | N/A |
| **Domínio Técnico** | Engenharia Mecânica / Dispositivos de Dispensação |
| **Cluster Temático** | Dispositivos de dispensação de líquidos pressurizados com CO2 |
| **Papel do CO2** | working_fluid |
| **Papel do Armazenamento** | implicit_or_support_storage |
| **Limite Sistêmico** | process_integration |
| **Tipo de Ciclo** | not_clear |
| **Fonte/Sumidouro Térmico** | not_clear |
| **Foco das Claims** | component_or_operation |
| **Categoria de Exclusão** | low_alignment |
| **Confiança** | 0.56 |
| **Rerank Aplicado** | Não |
| **Motivo do Rerank** | N/A |
| **Revisão Manual** | Não |
| **Erro LLM** | N/A |

**Abstract:**
> (EN)1, 171, 698. Dispensing liquids by gaseous pressure. DISTILLERS CO. (CARBONDIOXIDE) Ltd. April 11, 1968 (April 11, 1967], No.16511/67. Heading F1R. A dispenser of liquids from a container comprises a body provided with means for attaching the dispenser to the container, a sharp tube capable of piercing a hole in the lid of the container, a seal on the underside of the body surrounding the tube which when the dispenser is attached to the container forms a substantially gas-tight chamber around the tube, the chamber being in communication with the interior of the container via the hole in the lid, a supply ofcarbondioxideunder pressure with which the chamber is in communication via a non-return valve, and a delivery tube housed within the sharp tube which communicates with a dispensing tube projecting from the body of the device. After removal of a dip tube 8, a sharp tube 1 is forced into the lid of a beer can to form a hole. The dip tube 8 is then refitted and a screw thread 3 is screwed into the hole in the lid until a seal 43, which may be of silicone rubber, is in sealing engagement with the lid. A capsule 21 of high-pressurecarbondioxideis placed in a holder 20 and a cap 22 is screwed on, a pin 23 on the cap piercing the capsule. High-pressurecarbondioxidepasses through a pressure reducing valve, a sintered metal filter 34, and a capillary tube 29 to a low-pressure chamber 25. The pressure reducing valve is formed by the engagement of the end of the capillary tube 29 with a polyurethane pad 30, the capillary tube being pressed against the pad by a piston 26 subjected to the pressure in the low-pressure chamber 25 and the opposing force of a spring 27. From the low-pressure chamber 25, the low-pressurecarbondioxidepasses via a duct 39, a duct (38) and a non-return valve (44) into the space between the seal 43 and the sharp tube 1 and thence into the beer can. On depression of a button 5 to the position shown, a bore 11 is brought adjacent a port 12 to allow beer, urged by thecarbondioxideto be delivered via the dip tube 8, bores 10, 11, port 12 and a dispensing tube 13. A relief valve (45) vents excessive pressure to atmosphere. Castellations 55 cooperate with pins (56) depending from the button 5 so that by rotating the button the dispenser can be locked into a non-dispensing state. Instead of a screw thread 3, spring members hooking over the rim of the can may be used. Alternatively, a bayonet-type joint may be used with cans provided with the necessary fitment. The pin 23 can be provided at the other end of the holder 20, projecting from the pad 30. Provision may be made for holding twocarbondioxidecapsules with interchangeable connections to the interior of the can. Thecarbondioxidesupply may be a large cylinder of liquidcarbondioxideunder pressure.

**Evidências citadas:**
> “A dispenser of liquids from a container comprises a body provided with means for attaching the dispenser to the container, a sharp tube capable of piercing a hole in the lid of the container, a seal on the underside of the body surrounding the tube which when the dispenser is attached to the container forms a substantially gas-tight chamber around the tube, the chamber being in communication with the interior of the container via the hole in the lid, a supply of carbondioxide under pressure with which the chamber is in communication via a non-return valve, and a delivery tube housed within the sharp tube which communicates with a dispensing tube projecting from the body of the device.”
> “A capsule 21 of high-pressure carbondioxide is placed in a holder 20 and a cap 22 is screwed on, a pin 23 on the cap piercing the capsule.”

---

### 12. 3. GB1557123 - METHOD AND APPARATUS FOR REPARING EXTRACTS OF HOPS AND OTHER MATERIALS

| Campo | Valor |
|-------|-------|
| **Record ID** | `rec_76d55808cf57` |
| **Family ID** | `family:cbb7e61b410333c3d2ab0b915b28f262efafae4a` |
| **ID** | `GB135726881` |
| **Inventores** | N/A |
| **Titular** | DISTILLERS CO; CARBON; DIOXIDE |
| **Data** | 05.12.1979 |
| **Fonte** | Patentscope |
| **URL** | [GB135726881](https://patentscope.wipo.int/search/en/detail.jsf;jsessionid=B7FF3B8F425CF49CCBA4A34522F9AFB1.wapp2nB?docId=GB135726881&_cid=P21-MQ9HVZ-13283-1) |
| **Triagem** | exclude |
| **Rota** | screen_only |
| **Motivo da rota** | Patente excluída na triagem. |
| **Score de Triagem** | 1.2/10 |
| **Score de Relevância** | 0.0/10 |
| **Nível de Inovação** | N/A |
| **Domínio Técnico** | Processamento de Alimentos/Bebidas |
| **Cluster Temático** | Extração de lúpulo e outros materiais |
| **Papel do CO2** | co2_present_unclear_role |
| **Papel do Armazenamento** | explicit_thermal_storage |
| **Limite Sistêmico** | process_integration |
| **Tipo de Ciclo** | not_clear |
| **Fonte/Sumidouro Térmico** | not_clear |
| **Foco das Claims** | process_integration |
| **Categoria de Exclusão** | low_alignment |
| **Confiança** | 0.42 |
| **Rerank Aplicado** | Não |
| **Motivo do Rerank** | N/A |
| **Revisão Manual** | Não |
| **Erro LLM** | N/A |

**Evidências citadas:**
> DISTILLERS CO; CARBON; DIOXIDE

---

### 13. 4. GB2047588 - Reclamation of foundry sand

| Campo | Valor |
|-------|-------|
| **Record ID** | `rec_41383e272fc3` |
| **Family ID** | `family:bceb0440acbb089115ab7aef122c2422ff99fd35` |
| **ID** | `GB135860928` |
| **Inventores** | N/A |
| **Titular** | DISTILLERS CO; CARBON; DIOXIDE |
| **Data** | 03.12.1980 |
| **Fonte** | Patentscope |
| **URL** | [GB135860928](https://patentscope.wipo.int/search/en/detail.jsf;jsessionid=B7FF3B8F425CF49CCBA4A34522F9AFB1.wapp2nB?docId=GB135860928&_cid=P21-MQ9HVZ-13283-1) |
| **Triagem** | exclude |
| **Rota** | screen_only |
| **Motivo da rota** | Patente excluída na triagem. |
| **Score de Triagem** | 4.0/10 |
| **Score de Relevância** | 0.0/10 |
| **Nível de Inovação** | N/A |
| **Domínio Técnico** | Materials Science/Foundry Processes |
| **Cluster Temático** | Sand Reclamation & Binder Removal |
| **Papel do CO2** | co2_present_unclear_role |
| **Papel do Armazenamento** | explicit_thermal_storage |
| **Limite Sistêmico** | process_integration |
| **Tipo de Ciclo** | not_clear |
| **Fonte/Sumidouro Térmico** | not_clear |
| **Foco das Claims** | process_integration |
| **Categoria de Exclusão** | industrial_heat_adjacent |
| **Confiança** | 0.95 |
| **Rerank Aplicado** | Sim |
| **Motivo do Rerank** | reranked:review->exclude |
| **Revisão Manual** | Não |
| **Erro LLM** | N/A |

**Abstract:**
> (EN)A process for the reclamation of CO2-silicate bonded casting sand includes the step of subjecting the sand after it has been used for casting to treatment withcarbondioxidein the presence of water until substantially all of the reactive soluble alkali metal compounds present in the used sand which are capable of beingcarbonatedarecarbonated. Thiscarbonationstep improves the removal of the binder by a subsequent mechanical attrition step. In effecting the process, a batch of the used sand may be wetted and subjected to a vacuum, the vacuum then being broken by the introduction ofcarbondioxidewhich may be at a superatmospheric pressure.

**Evidências citadas:**
> “A process for the reclamation of CO2-silicate bonded casting sand includes the step of subjecting the sand…to treatment with carbon dioxide in the presence of water…”

---

### 14. 5. GB1426573 - WEIGHING MACHINES

| Campo | Valor |
|-------|-------|
| **Record ID** | `rec_30e4a6816fda` |
| **Family ID** | `family:36fc550daf20ead3ac342efcfb95c41f0a91aab1` |
| **ID** | `GB135595668` |
| **Inventores** | N/A |
| **Titular** | DISTILLERS CO; CARBON; DIOXIDE |
| **Data** | 03.03.1976 |
| **Fonte** | Patentscope |
| **URL** | [GB135595668](https://patentscope.wipo.int/search/en/detail.jsf;jsessionid=B7FF3B8F425CF49CCBA4A34522F9AFB1.wapp2nB?docId=GB135595668&_cid=P21-MQ9HVZ-13283-1) |
| **Triagem** | exclude |
| **Rota** | screen_only |
| **Motivo da rota** | Patente excluída na triagem. |
| **Score de Triagem** | 1.7/10 |
| **Score de Relevância** | 0.0/10 |
| **Nível de Inovação** | N/A |
| **Domínio Técnico** | Engenharia Mecânica / Pesagem e Controle |
| **Cluster Temático** | Sistemas de Pesagem e Controle de Fluxo |
| **Papel do CO2** | co2_present_unclear_role |
| **Papel do Armazenamento** | explicit_thermal_storage |
| **Limite Sistêmico** | process_integration |
| **Tipo de Ciclo** | not_clear |
| **Fonte/Sumidouro Térmico** | not_clear |
| **Foco das Claims** | component_or_operation |
| **Categoria de Exclusão** | industrial_heat_adjacent |
| **Confiança** | 0.49 |
| **Rerank Aplicado** | Não |
| **Motivo do Rerank** | N/A |
| **Revisão Manual** | Não |
| **Erro LLM** | N/A |

**Abstract:**
> (EN)1426573 Automatic weighing DISTILLERS CO (CARBONDIOXIDE) Ltd 15 Feb 1974 [27 Feb 1973] 9566/73 Heading G1W The filling of a cylinder with liquidcarbondioxideis controlled by a weighing machine having a dial, a pointer, a permanent magnet 7 mounted on the pointer or an arm 6 moving with pointer, normally open reed switches 9, 10, 11 operable by the magnet, and a control circuit (Fig. 3). The filling apparatus comprises a continuously running pump 21 having its inlet connected to a supply a by-pass 25 containing a solenoid valve 18 and connecting the outlet of the pump to the supply, and a connection 29 containing a solenoid valve 19 and to which the cylinder to be filled is connected. The control circuit includes an A.C. transformer 12, a D.C. relay R including a diode rectifying network, solenoids 16, 16 which energized respectively open and close valve 18, and solenoid 17 which when energized opens valve 19. In use, an empty cylinder is placed on the weighing machine which is then adjusted until the pointer reads zero, and reed switch 9 is therefore closed. Switch 15 is used to select reed switch 10 or 11 according to the size of the cylinder and switch 13 is pressed to energize relay R. Holding contacts Ra maintain the relay energized when switch 13 is released. When relay R is energized contacts Rb energize solenoids 16 17 so that valve 18 is closed and valve 19 is open. When reed switch 10 or 11 is closed by magnet 7, the coil of relay R is short circuited, contacts Ra open and contacts Rb switch over causing solenoid 17 to be de-energized and solenoid 16 to be energized, thus closing valve 19 and opening valve 18. Switch 31 is then operated to open solenoid valve 28 to vent connection 29 to atmosphere. The filling apparatus includes a non-return valve 24, a safety valve 26 and a damping chamber 27. In damping chamber 27, a heating element 28 maintains a body of gas which damps out the pulses produced by pump 21.

**Evidências citadas:**
> The filling of a cylinder with liquid carbondioxide is controlled by a weighing machine
> The filling apparatus comprises a continuously running pump 21 having its inlet connected to a supply a by-pass 25 containing a solenoid valve 18

---

### 15. 6. GB1174314 - A Dispensing Device for Gases Under Pressure.

| Campo | Valor |
|-------|-------|
| **Record ID** | `rec_503f33199a94` |
| **Family ID** | `family:202dab26a0dfe88a22b2a18fa9f80ed0a172ef8f` |
| **ID** | `GB135357801` |
| **Inventores** | GODFERY GORDON REGINALD |
| **Titular** | DISTILLERS CO; CARBON; DIOXIDE |
| **Data** | 17.12.1969 |
| **Fonte** | Patentscope |
| **URL** | [GB135357801](https://patentscope.wipo.int/search/en/detail.jsf;jsessionid=B7FF3B8F425CF49CCBA4A34522F9AFB1.wapp2nB?docId=GB135357801&_cid=P21-MQ9HVZ-13283-1) |
| **Triagem** | exclude |
| **Rota** | screen_only |
| **Motivo da rota** | Patente excluída na triagem. |
| **Score de Triagem** | 3.5/10 |
| **Score de Relevância** | 0.0/10 |
| **Nível de Inovação** | N/A |
| **Domínio Técnico** | Engenharia Mecânica |
| **Cluster Temático** | Dispositivos de dispensação de gases pressurizados |
| **Papel do CO2** | working_fluid |
| **Papel do Armazenamento** | implicit_or_support_storage |
| **Limite Sistêmico** | cycle_or_transfer_subsystem |
| **Tipo de Ciclo** | not_clear |
| **Fonte/Sumidouro Térmico** | not_clear |
| **Foco das Claims** | component_or_operation |
| **Categoria de Exclusão** | low_alignment |
| **Confiança** | 0.56 |
| **Rerank Aplicado** | Não |
| **Motivo do Rerank** | N/A |
| **Revisão Manual** | Não |
| **Erro LLM** | N/A |

**Abstract:**
> (EN)1,174,314. Valves. DISTILLERS CO. (CARBONDIOXIDE) Ltd. 22 May, 1968 [25 May, 1967], No. 24270/67. Heading F2V. Universal dispensing device for supplyingcarbondioxideat suitable reduced pressures to various appliances such as, soda syphones, fire extinguishers, dinghies, life-rafts and tyre inflators from a container comprises a reducing valve 12, 14 operated by a diaphragm 13 exposed to pressure in an outlet chamber 13. A loading spring 17 for the diaphragm is adjustable by a screwed retainer 16 connected through a rack and pinion device to pins 31 slidable in an outlet connection 28 and adapted to form a bayonet connection with the appliance. The appliances are arranged so that connection can only be made when the device is adjusted to supply the gas at the required pressure. A trigger operated valve 25 is in series with the reducing valve. The latter comprises a capillary tube 12 connected to the diaphragm and passing through an 0-ring seal to engage a seat 14 carried in a porous plug 10. A piercing member 6 opens the container as the device is coupled. The setting is indicated on a plate 5. A relief valve 19 is included.

**Evidências citadas:**
> “supplying carbondioxide at suitable reduced pressures”
> “reducing valve 12, 14 operated by a diaphragm 13 exposed to pressure in an outlet chamber 13”

---

### 16. 7. GB1253973 - LIQUID MOVING SYSTEMS

| Campo | Valor |
|-------|-------|
| **Record ID** | `rec_de4ca5e48547` |
| **Family ID** | `family:ebf3a506606670b244097541b77a7ba5940e87a1` |
| **ID** | `GB135438798` |
| **Inventores** | EVANS ARTHUR JAMES |
| **Titular** | DISTILLERS CO; CARBON; DIOXIDE |
| **Data** | 17.11.1971 |
| **Fonte** | Patentscope |
| **URL** | [GB135438798](https://patentscope.wipo.int/search/en/detail.jsf;jsessionid=B7FF3B8F425CF49CCBA4A34522F9AFB1.wapp2nB?docId=GB135438798&_cid=P21-MQ9HVZ-13283-1) |
| **Triagem** | exclude |
| **Rota** | screen_only |
| **Motivo da rota** | Patente excluída na triagem. |
| **Score de Triagem** | 2.2/10 |
| **Score de Relevância** | 0.0/10 |
| **Nível de Inovação** | N/A |
| **Domínio Técnico** | Engenharia Mecânica, Sistemas de Controle de Fluidos |
| **Cluster Temático** | Controle de Nível de Líquido, Detecção de Gás, Sistemas de Distribuição de Bebidas |
| **Papel do CO2** | co2_present_unclear_role |
| **Papel do Armazenamento** | implicit_or_support_storage |
| **Limite Sistêmico** | process_integration |
| **Tipo de Ciclo** | not_clear |
| **Fonte/Sumidouro Térmico** | not_clear |
| **Foco das Claims** | component_or_operation |
| **Categoria de Exclusão** | industrial_heat_adjacent |
| **Confiança** | 0.49 |
| **Rerank Aplicado** | Não |
| **Motivo do Rerank** | N/A |
| **Revisão Manual** | Não |
| **Erro LLM** | N/A |

**Abstract:**
> (EN)1,253,973. Liquid level control. DISTILLERS CO. (CARBONDIOXIDE) Ltd. Jan. 13, 1970 [Oct.22, 1968], No. 50060/68. Heading G1H. In equipment in which beer is drawn by a pump from a bulk container through a pipe 1 into a glass cylinder 3 and leaves through a pipe 2, a reed switch 4 is arranged adjacent or above the pipe 1 and a float containing a magnet 9, floats on the beer, the arrangement is such that ascarbondioxidegas collects in the cylinder 3 the beer level 18 and hence the float 5 drops until the magnet 9 actuates switch 4 to close a contact in a switch 10 to isolate a circuit 11, controlling the pump, and complete a circuit to a warning lamp. A valve 7 is manually operated to allow all the gas to escape through a pipe 6 and then closed and a push button operated to resume normal operation. In a modification, Fig. 2 (not shown) the float is provided with two magnets and two reed switches one of which is in circuit with the valve 6.

**Evidências citadas:**
> “as carbon dioxide gas collects in the cylinder 3 the beer level 18 and hence the float 5 drops”
> “Titular: DISTILLERS CO; CARBON; DIOXIDE”

---

### 17. 8. GB1329637 - TEMPORARY FREEZING OF SOFT OR FLEXIBLE ARTICLES

| Campo | Valor |
|-------|-------|
| **Record ID** | `rec_8d5d3fbad60e` |
| **Family ID** | `family:8d2d39153d4a37df4db17f0af0630c0b88758942` |
| **ID** | `GB135513929` |
| **Inventores** | N/A |
| **Titular** | DISTILLERS CO; CARBON; DIOXIDE |
| **Data** | 12.09.1973 |
| **Fonte** | Patentscope |
| **URL** | [GB135513929](https://patentscope.wipo.int/search/en/detail.jsf;jsessionid=B7FF3B8F425CF49CCBA4A34522F9AFB1.wapp2nB?docId=GB135513929&_cid=P21-MQ9HVZ-13283-1) |
| **Triagem** | exclude |
| **Rota** | screen_only |
| **Motivo da rota** | Patente excluída na triagem. |
| **Score de Triagem** | 3.3/10 |
| **Score de Relevância** | 0.0/10 |
| **Nível de Inovação** | N/A |
| **Domínio Técnico** | Engenharia Mecânica / Processamento de Materiais |
| **Cluster Temático** | Refrigeração e Congelamento, Processamento de Polímeros |
| **Papel do CO2** | refrigerant_loop |
| **Papel do Armazenamento** | implicit_or_support_storage |
| **Limite Sistêmico** | process_integration |
| **Tipo de Ciclo** | refrigeration_cycle |
| **Fonte/Sumidouro Térmico** | cooling_or_refrigeration |
| **Foco das Claims** | component_or_operation |
| **Categoria de Exclusão** | cooling_only |
| **Confiança** | 0.49 |
| **Rerank Aplicado** | Não |
| **Motivo do Rerank** | N/A |
| **Revisão Manual** | Não |
| **Erro LLM** | N/A |

**Abstract:**
> (EN)1329637 Chilling flexible articles DISTILLERS CO (CARBONDIOXIDE) Ltd 29 March 1972 [23 April 1971] 10925/71 Heading F4H A rubber tube 15 is temporarily made rigid by freezing in an enclosure 1 supplied with a liquid refrigerant, e.g. liquidcarbondioxide, through an external control valve 8 having a metering jet 12 and a closure member 13 which is operated to open the valve, the jet communicating with the interior of the enclosure by a duet 3 having a diameter many times that of the jet 12. The tube moves in the same direction as the cold vapour, i.e. right to left, and passes out of the enclosure through an opening in an end wall 5. The enclosure is insulated at 2, The valve is opened intermittently to keep the temperature at the desired level by a pulse generator 14 acting through a solenoid. The provision of a wide duct downstream of the metering jet prevents the jet becoming blocked withcarbondioxideice and dirt. The rigid tube 15 is passed to a braiding machine where it is braided with wire or cord.

**Evidências citadas:**
> “e.g. liquidcarbondioxide”
> “The provision of a wide duct downstream of the metering jet prevents the jet becoming blocked withcarbondioxideice and dirt.”

---

### 18. 9. GB1125505 - Production of carbon dioxide and argon

| Campo | Valor |
|-------|-------|
| **Record ID** | `rec_f9a115b06b66` |
| **Family ID** | `family:df3fa53f6bed201115d9ced152735bedd3357fbb` |
| **ID** | `GB135308953` |
| **Inventores** | WEIR THOMAS, WHELDON ALFRED GORDON |
| **Titular** | DISTILLERS CO; CARBON; DIOXIDE |
| **Data** | 28.08.1968 |
| **Fonte** | Patentscope |
| **URL** | [GB135308953](https://patentscope.wipo.int/search/en/detail.jsf;jsessionid=B7FF3B8F425CF49CCBA4A34522F9AFB1.wapp2nB?docId=GB135308953&_cid=P21-MQ9HVZ-13283-1) |
| **Triagem** | exclude |
| **Rota** | screen_only |
| **Motivo da rota** | Patente excluída na triagem. |
| **Score de Triagem** | 5.7/10 |
| **Score de Relevância** | 0.0/10 |
| **Nível de Inovação** | N/A |
| **Domínio Técnico** | Industrial Gas Production |
| **Cluster Temático** | CO2/Argon separation from combustion gases |
| **Papel do CO2** | co2_present_unclear_role |
| **Papel do Armazenamento** | explicit_thermal_storage |
| **Limite Sistêmico** | process_integration |
| **Tipo de Ciclo** | not_clear |
| **Fonte/Sumidouro Térmico** | industrial_heat |
| **Foco das Claims** | process_integration |
| **Categoria de Exclusão** | industrial_heat_adjacent |
| **Confiança** | 0.90 |
| **Rerank Aplicado** | Sim |
| **Motivo do Rerank** | reranked:review->exclude |
| **Revisão Manual** | Não |
| **Erro LLM** | N/A |

**Abstract:**
> (EN)1,125,505.Carbondioxideand argon. DISTILLERS CO. (CARBONDIOXIDE) Ltd. 30 May, 1967 [23 June, 1966], No. 28050/66. Heading C1A. [Also in Division F4]Carbondioxideand argon are produced by subjecting a mixture of argon, oxygen, and acarbon-containing compound or compounds to complete combustion and separating the combustion products to obtain a CO 2  fraction and an Ar fraction. The mixture of Ar and oxygen may be obtained from the liquefaction and fractional distillation of air. The combustible compound may be a heavy fuel oil. The combustion products may be separated by subjecting them to cooling, drying, liquefaction and distillation steps. Should a sulphur-impurecarbon-containing compound be used, sulphurdioxidemay be removed in the distillation step as a high boiling base product,

**Evidências citadas:**
> “Carbondioxideand argon are produced by subjecting a mixture of argon, oxygen, and a carbon-containing compound or compounds to complete combustion”

---

### 19. 10. GB1236064 - IMPROVEMENTS IN OR RELATING TO FIRE EXTINGUISHING COMPOSITIONS

| Campo | Valor |
|-------|-------|
| **Record ID** | `rec_4d7241bf789e` |
| **Family ID** | `family:87b56bacc82d6fc615f6650da0a0c662368c8996` |
| **ID** | `GB135420945` |
| **Inventores** | WHELDON ALBERT GORDON |
| **Titular** | DISTILLERS CO; CARBON; DIOXIDE |
| **Data** | 16.06.1971 |
| **Fonte** | Patentscope |
| **URL** | [GB135420945](https://patentscope.wipo.int/search/en/detail.jsf;jsessionid=B7FF3B8F425CF49CCBA4A34522F9AFB1.wapp2nB?docId=GB135420945&_cid=P21-MQ9HVZ-13283-1) |
| **Triagem** | exclude |
| **Rota** | screen_only |
| **Motivo da rota** | Patente excluída na triagem. |
| **Score de Triagem** | 3.3/10 |
| **Score de Relevância** | 0.0/10 |
| **Nível de Inovação** | N/A |
| **Domínio Técnico** | Extintores de Incêndio |
| **Cluster Temático** | Composições extintoras de incêndio contendo CO2 |
| **Papel do CO2** | co2_present_unclear_role |
| **Papel do Armazenamento** | explicit_thermal_storage |
| **Limite Sistêmico** | process_integration |
| **Tipo de Ciclo** | not_clear |
| **Fonte/Sumidouro Térmico** | not_clear |
| **Foco das Claims** | component_or_operation |
| **Categoria de Exclusão** | industrial_heat_adjacent |
| **Confiança** | 0.49 |
| **Rerank Aplicado** | Não |
| **Motivo do Rerank** | N/A |
| **Revisão Manual** | Não |
| **Erro LLM** | N/A |

**Abstract:**
> (EN)1,236,064. Fire extinguishing slurries. DISTILLERS CO. (CARBONDIOXIDE) Ltd. 27 Oct., 1969 [19 Oct., 1968], No. 49685/68. Heading ASA. A slurry of solid CO 2  in a liquid fireextinguishing agent for fire-fighting purposes is produced by mixing liquid Co 2  and the liquid extinguishant under pressure such that a solution of one in the other is formed, and releasing the solution at a lower pressure when the slurry is required. Bromochlorodifluoromethane (BCF) is preferred. The two liquids are pumped into a container maintained at 30‹ to -80‹C., e.g. in a ratio 3:1 CO 2 :BCF by volume. The solution may be released via a cyclone separator.

**Evidências citadas:**
> A slurry of solid CO 2  in a liquid fireextinguishing agent...
> The two liquids are pumped into a container maintained at 30‹ to -80‹C., e.g. in a ratio 3:1 CO 2 :BCF by volume.

---

## 🧾 Fila de Revisão Manual

- rec_bad1378c89ef (US20240252980A1) | rota=deep_extraction | motivo=Há evidência suficiente para extração detalhada. | erro_llm=Timeout ao chamar Ollama.
- rec_8b168382e70e (GB135599119) | rota=manual_review | motivo=Triagem indicou revisão humana. | erro_llm=N/A

---

## 🔬 Análise Comparativa

⚠️ Não foi possível gerar a análise comparativa.

---

## 🧭 Matriz de Whitespaces

- **Patentes selecionadas:** 11
- **Núcleo:** 8
- **Fronteira:** 1
- **Adjacência:** 2

- **hybrid_cycle_storage_architecture**: Combinar ciclos/transferencia com CO2 e armazenamento termico explicitamente reivindicado ainda aparece fragmentado entre nucleo e borda tecnica. [core=US20260008008A1, US20240228419A1, US20220072471A1 | frontier=GB135599119 | adjacent=GB135308953, GB135860928]

---

## ℹ️ Informações do Sistema

- **Gerado por:** Agente de Web Scraping de Patentes
- **Modelo LLM:** gemma3:27b
- **Data de geração:** 11/06/2026 11:46:50
- **Query de busca:** `carbon dioxide`
- **Status da execução:** completed
- **Tempo total:** 7054.5s
- **LLM disponível:** sim
- **Erros registrados:** 1
- **Fila de revisão manual:** 2 itens
- **Snapshot hash:** `6d7003cf4f98c0c537ddffc872e74a2940563538706ae8424b8b9029dbac9535`
- **Features habilitadas:** require_evidence, enable_thematic_clusters, enable_structural_roles, enable_screening_rerank, enable_prisma, enable_snapshot, enable_comparative_analysis, enable_whitespace_analysis, enable_manual_review_queue
- **Features desabilitadas:** nenhum
- **Versão do pipeline:** 1.1
- **Thresholds snapshot:** include=7.0, review=4.5
- **Cache LLM:** 0 hits, 33 misses, 36 entradas
- **Status do rascunho:** ready