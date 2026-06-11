# 📋 Relatório de Análise de Patentes

**Data:** 09/04/2026 22:02:37
**Busca:** `carbon dioxide thermal energy storage`
**Total de patentes encontradas:** 10
**Modelo de avaliação:** gemma3:4b

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

- **Total bruto coletado:** 10
- **Patentes únicas:** 10
- **Duplicatas removidas:** 0
- **Triadas:** 10
- **Incluídas:** 4
- **Em revisão manual:** 2
- **Excluídas:** 4
- **Extrações completas:** 6
- **Sem abstract/snippet:** 1
- **Sem ID:** 0
- **Identidade por conteúdo:** 0
- **Identidade fallback:** 0
- **Duplicatas por família removidas:** 0
- **Falhas de triagem LLM:** 0
- **Falhas totais LLM:** 0

## 🧭 Fluxo PRISMA-Like

- **Identificação:** 10 bruto(s), 10 único(s), 0 duplicata(s) removida(s)
- **Triagem:** 10 triado(s), 4 incluído(s), 2 em revisão, 4 excluído(s)
- **Elegibilidade:** 6 extração(ões) completa(s), 2 revisão(ões) manual(is), 0 adiada(s)
- **Cobertura:** 1 sem abstract/snippet, 0 sem ID
- **Síntese:** 6 registro(s) analisado(s)

## 🧩 Síntese Temática

### CO2 Cycle Configurations

- **Patentes:** 2
- **Score médio:** 9.70/10
- **Confiança média:** 0.95
- **Evidências citadas:** 4
- **IDs:** CN118934113A, CN115234318A

### Thermal Transfer Mechanisms

- **Patentes:** 2
- **Score médio:** 8.00/10
- **Confiança média:** 0.95
- **Evidências citadas:** 4
- **IDs:** US20230029186A1, WO2021081541A1

## 🧠 Contexto Compartilhado

- **Top patentes no contexto:** 4
- **Clusters no contexto:** 2
- **Roteamento agregado:** 3 rota(s)
- **Slots ativos:** N/A

## ⏱️ Métricas por Etapa

| Etapa | Status | Duração | Itens | Detalhes |
|---|---|---:|---:|---|
| setup | ok | 0.35s | 1 | Verificação do modelo Ollama |
| search | ok | 56.03s | 10 | 10 patentes únicas após dedupe |
| screening | ok | 29.62s | 10 | 4 incluídas, 2 revisão |
| comparative_analysis | ok | 6.01s | 10 | Síntese comparativa gerada |
| reporting | ok | 0.00s | 10 | Relatórios Markdown e JSON |
| finalization | ok | 0.00s | 7 | Persistência de artefatos e estado |

## 🌐 Diagnósticos de Coleta

### GooglePatents

- Nenhum sinal relevante detectado.

### Patentscope

- **discovery_empty**: DuckDuckGo não retornou links para Patentscope.

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
- **Latência média:** 0.337s
- **Latência máxima:** 0.337s

### screening

- **Chamadas:** 10
- **Sucessos:** 10
- **Falhas:** 0
- **Retries:** 0
- **Cache hits:** 0
- **Pulos por degradação:** 0
- **Latência média:** 1.335s
- **Latência máxima:** 2.464s

### evaluation

- **Chamadas:** 6
- **Sucessos:** 6
- **Falhas:** 0
- **Retries:** 0
- **Cache hits:** 0
- **Pulos por degradação:** 0
- **Latência média:** 2.711s
- **Latência máxima:** 3.913s

### comparative

- **Chamadas:** 1
- **Sucessos:** 1
- **Falhas:** 0
- **Retries:** 0
- **Cache hits:** 0
- **Pulos por degradação:** 0
- **Latência média:** 6.012s
- **Latência máxima:** 6.012s

## 🔎 Observabilidade Estruturada

### Rotas

- **deep_extraction**: total=4, include=4, review=0, exclude=0, llm_errors=0
- **screen_only**: total=4, include=0, review=0, exclude=4, llm_errors=0
- **manual_review**: total=2, include=0, review=2, exclude=0, llm_errors=0

### Fontes

- **GooglePatents**: bruto=5, duração=14.38s, diagnósticos=nenhum
- **Patentscope**: bruto=5, duração=41.65s, diagnósticos=discovery_empty=1

### Falhas

- **Erros de execução:** 0
- **Registros com erro de LLM:** 0
- **Falhas totais do LLM:** 0
- **LLM por operação:** comparative(falhas=0, retries=0, skips=0), evaluation(falhas=0, retries=0, skips=0), healthcheck(falhas=0, retries=0, skips=0), screening(falhas=0, retries=0, skips=0)
- **Scraper por tipo de sinal:** discovery_empty=1

## 📊 Resumo Executivo

**Score médio de relevância:** 8.8/10

| # | Patente | Score | Inovação | Domínio |
|---|---------|-------|----------|---------|
| 1 | [CN118934113A](https://patents.google.com/patent/CN118934113A/en) — An isothermal and isobaric supercritical compressed carbon d... | 🟢 10.0 (include) | Significativa | Engenharia Termodinâmica, Armazenamento de Energia |
| 2 | [CN115234318A](https://patents.google.com/patent/CN115234318A/en) — Carbon dioxide energy storage system matched with thermal po... | 🟢 9.4 (include) | Incremental | Armazenamento de Energia, Termodinâmica, Engenharia de Combustão |
| 3 | [US20230029186A1](https://patents.google.com/patent/US20230029186A1/en) — Method for thermal energy transmission using water and carbo... | 🟢 8.0 (include) | Incremental | Armazenamento de Energia, Termodinâmica, Engenharia de Fluidos |
| 4 | [WO2021081541A1](https://patents.google.com/patent/WO2021081541A1/en) — Method for thermal energy transmission using water and carbo... | 🟢 8.0 (include) | Incremental | Armazenamento de Energia, Termodinâmica, Engenharia de Fluidos |
| 5 | [US20200182095A1](https://patents.google.com/patent/US20200182095A1/en) — Carbon dioxide upgrade and energy storage system and method | 🟡 6.5 (review) | Incremental | Engenharia Termodinâmica, Armazenamento de Energia |
| 6 | [AU244427549](https://patentscope.wipo.int/search/en/detail.jsf;jsessionid=BAAD772379BE651666C3D16A4E44112D.wapp2nB?docId=AU244427549&_cid=P21-MNS7A1-22073-1) — 1. AU2019901965 - A System to Improve Performance of Transcr... | 🟡 6.5 (review) | Incremental | Sistemas de Refrigeração, Armazenamento Térmico, Engenharia Térmica |
| 7 | [US433566429](https://patentscope.wipo.int/search/en/detail.jsf;jsessionid=BAAD772379BE651666C3D16A4E44112D.wapp2nB?docId=US433566429&_cid=P21-MNS7A1-22073-1) — 2. US20240229681 - Calcination system with thermal energy st... | 🔴 0.0 (exclude) | N/A | Armazenamento de Energia Térmica, Geração de Calor |
| 8 | [US400261922](https://patentscope.wipo.int/search/en/detail.jsf;jsessionid=BAAD772379BE651666C3D16A4E44112D.wapp2nB?docId=US400261922&_cid=P21-MNS7A1-22073-1) — 3. US20230203968 - Methods for material activation with ther... | 🔴 0.0 (exclude) | N/A | Armazenamento de Energia Térmica, Engenharia de Calor |
| 9 | [US433566430](https://patentscope.wipo.int/search/en/detail.jsf;jsessionid=BAAD772379BE651666C3D16A4E44112D.wapp2nB?docId=US433566430&_cid=P21-MNS7A1-22073-1) — 4. US20240229682 - Methods for material activation with ther... | 🔴 0.0 (exclude) | N/A | Armazenamento de Energia, Engenharia Térmica, Materiais |
| 10 | [US373267798](https://patentscope.wipo.int/search/en/detail.jsf;jsessionid=BAAD772379BE651666C3D16A4E44112D.wapp2nB?docId=US373267798&_cid=P21-MNS7A1-22073-1) — 5. US20220282638 - Material activation system with thermal e... | 🔴 0.0 (exclude) | N/A | Armazenamento de Energia, Termodinâmica, Engenharia Química |

---

## 🔍 Análise Detalhada das Patentes

### 1. An isothermal and isobaric supercritical compressed carbon dioxide energy storage system

| Campo | Valor |
|-------|-------|
| **Record ID** | `rec_e9bfd6ecaee9` |
| **Family ID** | `family:93e61d9efb570bcdd84ea6254a70ea2c9b769d40` |
| **ID** | `CN118934113A` |
| **Inventores** | å¾çæ°, æ±è½¶æ, èµµææº, æå£æ, ç¨æ³, è¡ä¸å­, å¨å­¦å¿, å¼ åè¯, éæµ·ç |
| **Titular** | Institute of Engineering Thermophysics of CAS |
| **Data** | 2024-11-12 |
| **Fonte** | Google Patents |
| **URL** | [CN118934113A](https://patents.google.com/patent/CN118934113A/en) |
| **Triagem** | include |
| **Rota** | deep_extraction |
| **Motivo da rota** | Há evidência suficiente para extração detalhada. |
| **Score de Triagem** | 9.2/10 |
| **Score de Relevância** | 10.0/10 |
| **Nível de Inovação** | Significativa |
| **Domínio Técnico** | Engenharia Termodinâmica, Armazenamento de Energia |
| **Cluster Temático** | CO2 Cycle Configurations |
| **Confiança** | 0.95 |
| **Revisão Manual** | Não |
| **Erro LLM** | N/A |

**Abstract:**
> AbstractTranslated fromChineseæ¬åææ¶åè¶ä¸´çåç¼©äºæ°§åç¢³å¨è½ææ¯é¢åï¼ç­æ¸©ç­åçè¶ä¸´çåç¼©äºæ°§åç¢³å¨è½ç³»ç»ï¼åæ¬ï¼åç¼©æºç»ï¼å©ç¨çµåå°ä½æ¸©ä½åçè¶ä¸´çäºæ°§åç¢³åç¼©ä¸ºé«æ¸©é«åçè¶ä¸´çäºæ°§åç¢³ï¼è¨èæºç»ï¼å©ç¨é«æ¸©é«åçè¶ä¸´çäºæ°§åç¢³åååçµï¼é«åå¨æ°å®¤ï¼è®¾ç½®å¨æ°´ä¸æå°ä¸çé«åç¯å¢ä¸­ï¼ç¨äºå¨å­åç¼©æºç»åç¼©çè¶ä¸´çäºæ°§åç¢³ï¼ä½åå¨æ°å®¤ï¼è®¾ç½®å¨æ°´ä¸æå°ä¸çä½åç¯å¢ä¸­ç¨äºå¨å­è¨èæºç»åååçµä¸­äº§ççè¶ä¸´çäºæ°§åç¢³ï¼ç¬¬ä¸æ¢ç­å¨ï¼å¸æ¶åç¼©æºç»å·¥ä½è¿ç¨ä¸­äº§ççåç¼©ç­å¹¶å¨å­å¨å¨ç­ç½ä¸­ï¼ç¬¬äºæ¢ç­å¨ï¼å ç­é«åå¨æ°å®¤æåºçè¶ä¸´çäºæ°§åç¢³ãéè¿å°é«åå¨æ°å®¤åä½åå¨æ°å®¤è®¾ç½®å¨æ°´ä¸ï¼å¹¶éåæ¢ç­å¨ï¼å®ç°ç»´æå¨æ°å®¤ç­ååæ°ç¨³å®çè¶ä¸´çåç¼©äºæ°§åç¢³å¨è½ç³»ç»ãThe present invention relates to the technical field of supercritical compressed carbon dioxide energy storage, and an isothermal and isobaric supercritical compressed carbon dioxide energy storage system, comprising: a compressor unit, which compresses low-temperature and low-pressure supercritical carbon dioxide into high-temperature and high-pressure supercritical carbon dioxide by using electricity; an expansion unit, which uses high-temperature and high-pressure supercritical carbon dioxide to generate electricity; a high-pressure gas storage chamber, which is arranged in an underwater or underground high-pressure environment, and is used to store supercritical carbon dioxide compressed by the compressor unit; a low-pressure gas storage chamber, which is arranged in an underwater or underground low-pressure environment, and is used to store supercritical carbon dioxide generated by the expansion unit in generating electricity; a first heat exchanger, which absorbs compression heat generated during the operation of the compressor unit and stores it in a heat storage tank; and a second heat exchanger, which heats the supercritical carbon dioxide discharged from the high-pressure gas storage chamber. By arranging the high-pressure gas storage chamber and the low-pressure gas storage chamber underwater and cooperating with the heat exchanger, a supercritical compressed carbon dioxide energy storage system that maintains stable thermal parameters of the gas storage chamber is realized.

**Avaliação do LLM:**
Esta patente descreve um sistema de armazenamento de energia de CO2 supercrítico isoterma e isotrópico, utilizando câmaras de alta e baixa pressão para controle térmico. O sistema emprega um compressor e um expander para converter energia térmica em elétrica e vice-versa, com armazenamento em câmaras de alta e baixa pressão. A inovação reside na otimização do controle térmico e na utilização de CO2 supercrítico para armazenamento de energia.

**Extração Estruturada:**
- **Problema:** O problema abordado é a necessidade de um sistema de armazenamento de energia que possa controlar eficientemente a temperatura do CO2 supercrítico durante o ciclo de armazenamento e recuperação de energia, permitindo um controle térmico preciso e estável.
- **Solução:** A solução proposta é um sistema de armazenamento de energia de CO2 supercrítico que utiliza câmaras de alta e baixa pressão para manter a temperatura constante do CO2 durante o ciclo de armazenamento e recuperação de energia. O sistema inclui um compressor, um expander, câmaras de armazenamento de alta e baixa pressão e um sistema de troca de calor para controlar a temperatura do CO2.
- **Maturidade:** Intermediária

**Achados-chave:**
- O sistema utiliza CO2 supercrítico para otimizar o armazenamento de energia devido às suas propriedades termodinâmicas.
- A utilização de câmaras de alta e baixa pressão permite o controle preciso da temperatura do CO2 durante o ciclo de armazenamento e recuperação de energia.

**Vantagens alegadas:**
- Controle térmico preciso do CO2 supercrítico.
- Eficiência aprimorada no armazenamento e recuperação de energia.
- Estabilidade térmica do sistema de armazenamento.

**Limitações:**
- A patente não detalha especificamente os materiais utilizados nos componentes do sistema, o que pode afetar sua durabilidade e desempenho.
- A implementação em larga escala pode exigir considerações adicionais relacionadas à segurança e ao custo.

**Aplicações potenciais:**
- Armazenamento de energia em redes elétricas.
- Sistemas de aquecimento e resfriamento.
- Veículos elétricos.

**Evidências citadas:**
> æ¬åææ¶åè¶ä¸´çåç¼©äºæ°§åç¢³å¨è½ææ¯é¢åï¼ç­æ¸©ç­åçè¶ä¸´çåç¼©äºæ°§åç¢³å¨è½ç³»ç»ï¼
> åæ¬ï¼åç¼©æºç»ï¼å©ç¨çµåå°ä½æ¸©ä½åçè¶ä¸´çäºæ°§åç¢³åç¼©ä¸ºé«æ¸©é«åçè¶ä¸´çäºæ°§åç¢³ï¼è¨èæºç»ï¼å©ç¨é«æ¸©é«åçè¶ä¸´çäºæ°§åç¢³ï¼

---

### 2. Carbon dioxide energy storage system matched with thermal power plant deep peak shaving and control method thereof

| Campo | Valor |
|-------|-------|
| **Record ID** | `rec_60aba676d2d1` |
| **Family ID** | `family:e199d77fe5f85343c72bd55fe064233f9c8b31ec` |
| **ID** | `CN115234318A` |
| **Inventores** | è°¢æ°¸æ§, çç§¦, çé¼, å­ç£, å¼ è», æ±ªæå, æ¨å½ª |
| **Titular** | Baihe New Energy Technology Shenzhen Co ltd |
| **Data** | 2022-10-25 |
| **Fonte** | Google Patents |
| **URL** | [CN115234318A](https://patents.google.com/patent/CN115234318A/en) |
| **Triagem** | include |
| **Rota** | deep_extraction |
| **Motivo da rota** | Há evidência suficiente para extração detalhada. |
| **Score de Triagem** | 9.2/10 |
| **Score de Relevância** | 9.4/10 |
| **Nível de Inovação** | Incremental |
| **Domínio Técnico** | Armazenamento de Energia, Termodinâmica, Engenharia de Combustão |
| **Cluster Temático** | CO2 Cycle Configurations |
| **Confiança** | 0.95 |
| **Revisão Manual** | Não |
| **Erro LLM** | N/A |

**Abstract:**
> AbstractThe invention provides a carbon dioxide energy storage system matched with deep peak shaving of a thermal power plant and a control method thereof, and relates to the technical field of energy storage. The energy storage system includes: the gas storage, the energy storage component, the liquid storage tank and the energy release component are sequentially connected in a closed loop manner, and the energy release component comprises an expander; the coupling assembly comprises a steam extraction bypass and a first heat storage module; the steam extraction bypass is used for guiding high-temperature steam in the steam turbine to the first heat storage module when the thermal power plant is in a deep peak shaving working condition; the first heat storage module is connected with the energy release assembly and used for storing heat contained in the high-temperature steam and providing heat for the energy release assembly when the energy release assembly works so as to improve the temperature of carbon dioxide at the inlet of the expansion machine. The carbon dioxide energy storage system and the control method can improve the peak regulation flexibility and safety of the thermal power plant and can also improve the work efficiency of the carbon dioxide.

**Avaliação do LLM:**
Esta patente descreve um sistema de armazenamento de energia em dióxido de carbono acoplado a uma usina termelétrica, utilizando CO2 como meio de armazenamento térmico e um sistema de 'deep peak shaving'. O sistema inclui um ciclo fechado com um expander e módulos de armazenamento de calor, otimizando a flexibilidade e a segurança da usina termelétrica.

**Extração Estruturada:**
- **Problema:** O problema abordado é a necessidade de flexibilidade e segurança na regulação de pico de uma usina termelétrica, especialmente durante períodos de alta demanda.
- **Solução:** A patente propõe um sistema que utiliza CO2 para armazenar calor gerado durante o funcionamento da usina termelétrica, permitindo o 'deep peak shaving' e a recuperação do calor armazenado sob demanda através de um expander.
- **Maturidade:** Intermediária

**Achados-chave:**
- O sistema utiliza um ciclo fechado com CO2 para armazenamento térmico.
- Um expander é utilizado para liberar o calor armazenado em CO2, otimizando a eficiência do processo.

**Vantagens alegadas:**
- Melhora a flexibilidade e a segurança da usina termelétrica.
- Aumenta a eficiência do trabalho do CO2 como meio de armazenamento térmico.

**Limitações:**
- A patente não detalha a capacidade de armazenamento de energia ou a eficiência do sistema em condições operacionais específicas.
- A viabilidade econômica e a escalabilidade do sistema podem ser fatores limitantes.

**Aplicações potenciais:**
- Armazenamento de energia em usinas termelétricas.
- Sistemas de cogeração de calor e energia.

**Evidências citadas:**
> The invention provides a carbon dioxide energy storage system matched with deep peak shaving of a thermal power plant...
> The energy release component comprises an expander; the first heat storage module is connected with the energy release assembly and used for storing heat contained in the high-temperature steam...

---

### 3. Carbon dioxide upgrade and energy storage system and method

| Campo | Valor |
|-------|-------|
| **Record ID** | `rec_d32965bf3945` |
| **Family ID** | `family:1065f16bddea8989ffd25dd50703f560a5611777` |
| **ID** | `US20200182095A1` |
| **Inventores** | John Frederick Cirucci, Klaus Stephan Lackner |
| **Titular** | Arizona State University Downtown Phoenix campus |
| **Data** | 2020-06-11 |
| **Fonte** | Google Patents |
| **URL** | [US20200182095A1](https://patents.google.com/patent/US20200182095A1/en) |
| **Triagem** | review |
| **Rota** | manual_review |
| **Motivo da rota** | Triagem indicou revisão humana. |
| **Score de Triagem** | 7.7/10 |
| **Score de Relevância** | 6.5/10 |
| **Nível de Inovação** | Incremental |
| **Domínio Técnico** | Engenharia Termodinâmica, Armazenamento de Energia |
| **Cluster Temático** | Armazenamento de Energia Térmica com Fluidos de Trabalho |
| **Confiança** | 0.79 |
| **Revisão Manual** | Sim |
| **Erro LLM** | N/A |

**Abstract:**
> AbstractA method for producing work is disclosed. The method includes increasing the pressure of a working fluid including carbon dioxide from a first pressure at least equal to a triple point pressure to a second pressure above the triple point pressure. The method also includes heating the working fluid, extracting mechanical work by expanding a first portion of the heated working fluid to a third pressure, supplying a second portion of the heated working fluid as a motive fluid to an ejector, increasing the pressure of the expanded working fluid by supplying the expanded working fluid to the ejector to combine with the motive fluid and form an output fluid at the fourth pressure, the fourth pressure at least equal to the triple point pressure of the working fluid. The method also includes refrigerating the output fluid to condense a vapor phase into a liquid phase.

**Avaliação do LLM:**
Esta patente descreve um sistema e método para a produção de trabalho utilizando dióxido de carbono, envolvendo a manipulação da pressão e temperatura do fluido para realizar trabalho mecânico e armazenamento de energia. O sistema utiliza ciclos de aquecimento, expansão e resfriamento do CO2, explorando a sua capacidade de armazenar energia térmica. A patente foca na utilização do CO2 como fluido de trabalho para conversão de energia térmica em trabalho mecânico.

**Extração Estruturada:**
- **Problema:** O problema abordado é a necessidade de sistemas eficientes para armazenar energia térmica, explorando as propriedades termodinâmicas de fluidos como o dióxido de carbono.
- **Solução:** A solução proposta é um sistema que aumenta a pressão do CO2 acima da pressão do ponto triplo, aquece o fluido, extrai trabalho através da expansão, utiliza o CO2 como fluido de trabalho em um ejector e resfria o fluido para condensação, permitindo a conversão de energia térmica em trabalho mecânico e armazenamento.
- **Maturidade:** Inicial

**Achados-chave:**
- O sistema utiliza um ciclo que envolve aumento de pressão, aquecimento, expansão, e resfriamento do CO2.
- A patente detalha o uso do CO2 como fluido de trabalho, manipulando sua pressão e temperatura para extrair trabalho e realizar armazenamento de energia.

**Vantagens alegadas:**
- Potencial para conversão eficiente de energia térmica em trabalho mecânico.
- Utilização de dióxido de carbono como fluido de trabalho, que possui propriedades termodinâmicas favoráveis.

**Limitações:**
- A patente não detalha a escala ou o custo de implementação do sistema.
- A eficiência do sistema depende das condições operacionais e da otimização do ciclo termodinâmico.

**Aplicações potenciais:**
- Sistemas de armazenamento de energia térmica.
- Geração de energia a partir de fontes de calor residual.
- Sistemas de refrigeração e aquecimento.

**Evidências citadas:**
> “increasing the pressure of a working fluid including carbon dioxide from a first pressure at least equal to a triple point pressure to a second pressure above the triple point pressure.”
> “extracting mechanical work by expanding a first portion of the heated working fluid to a third pressure”

---

### 4. Method for thermal energy transmission using water and carbon dioxide

| Campo | Valor |
|-------|-------|
| **Record ID** | `rec_77e9991aef51` |
| **Family ID** | `family:2814d8c5f1b29d7789869b790858678c99ffc517` |
| **ID** | `US20230029186A1` |
| **Inventores** | Francois Ignace Geinoz, Marcel Cueni, Kameran Yakob |
| **Titular** | MED Energy Inc |
| **Data** | 2023-01-26 |
| **Fonte** | Google Patents |
| **URL** | [US20230029186A1](https://patents.google.com/patent/US20230029186A1/en) |
| **Triagem** | include |
| **Rota** | deep_extraction |
| **Motivo da rota** | Há evidência suficiente para extração detalhada. |
| **Score de Triagem** | 9.2/10 |
| **Score de Relevância** | 8.0/10 |
| **Nível de Inovação** | Incremental |
| **Domínio Técnico** | Armazenamento de Energia, Termodinâmica, Engenharia de Fluidos |
| **Cluster Temático** | Thermal Transfer Mechanisms |
| **Confiança** | 0.95 |
| **Revisão Manual** | Não |
| **Erro LLM** | N/A |

**Abstract:**
> AbstractThe invention provides a system for energy distribution that uses liquid carbon dioxide as a working fluid. Evaporation of the carbon dioxide provides cooling, and compression of the carbon dioxide gas back to the liquid state provides heat. The amount of heat transferred at both stages is sufficient to provide environmental heating and cooling. Waste thermal energy from a power plant, in the form of hot water, is fed into the system and used to drive the overall process. An underground thermal energy storage system is used to store energy flowing into the system that is in excess of the current demand.

**Avaliação do LLM:**
Esta patente descreve um sistema de distribuição de energia que utiliza dióxido de carbono líquido como fluido de trabalho para transferência de calor, aproveitando o ciclo de evaporação e compressão para gerar aquecimento e resfriamento. O sistema incorpora armazenamento de energia térmica subterrâneo para otimizar a utilização de energia excedente, particularmente de fontes como usinas termelétricas.

**Extração Estruturada:**
- **Problema:** O problema abordado é a utilização ineficiente de resíduos de energia térmica, como água quente proveniente de usinas, que poderiam ser armazenados e reutilizados para aplicações de aquecimento e resfriamento.
- **Solução:** A solução proposta é um sistema que utiliza o ciclo de dióxido de carbono para converter calor em energia útil e vice-versa, com armazenamento subterrâneo para otimizar o uso da energia.
- **Maturidade:** Inicial

**Achados-chave:**
- Utilização de dióxido de carbono líquido como fluido de trabalho para transferência de calor.
- Integração com um sistema de armazenamento subterrâneo de energia para otimizar o uso da energia.
- Aproveitamento de resíduos de energia térmica (água quente) para acionar o ciclo de dióxido de carbono.

**Vantagens alegadas:**
- Otimização da utilização de resíduos de energia térmica.
- Capacidade de fornecer aquecimento e resfriamento.
- Potencial para reduzir emissões de carbono através da reutilização de calor.

**Limitações:**
- Dependência da viabilidade técnica e econômica do armazenamento subterrâneo de energia.
- Eficiência do ciclo de dióxido de carbono pode ser afetada por perdas de calor.

**Aplicações potenciais:**
- Armazenamento de energia térmica em usinas termelétricas.
- Sistemas de aquecimento e resfriamento de edifícios.
- Integração com redes de energia renovável.

**Evidências citadas:**
> Evaporation of the carbon dioxide provides cooling, and compression of the carbon dioxide gas back to the liquid state provides heat.
> An underground thermal energy storage system is used to store energy flowing into the system that is in excess of the current demand.

---

### 5. Method for thermal energy transmission using water and carbon dioxide

| Campo | Valor |
|-------|-------|
| **Record ID** | `rec_cb86ce571d5d` |
| **Family ID** | `family:156d9db54f6d2df5efd352ddbf3bd612f775a37b` |
| **ID** | `WO2021081541A1` |
| **Inventores** | Francois Ignace GEINOZ, Marcel CUENI, Kameran Yakob |
| **Titular** | MED Energy Inc |
| **Data** | 2021-04-29 |
| **Fonte** | Google Patents |
| **URL** | [WO2021081541A1](https://patents.google.com/patent/WO2021081541A1/en) |
| **Triagem** | include |
| **Rota** | deep_extraction |
| **Motivo da rota** | Há evidência suficiente para extração detalhada. |
| **Score de Triagem** | 9.2/10 |
| **Score de Relevância** | 8.0/10 |
| **Nível de Inovação** | Incremental |
| **Domínio Técnico** | Armazenamento de Energia, Termodinâmica, Engenharia de Fluidos |
| **Cluster Temático** | Thermal Transfer Mechanisms |
| **Confiança** | 0.95 |
| **Revisão Manual** | Não |
| **Erro LLM** | N/A |

**Abstract:**
> AbstractThe invention provides a system for energy distribution that uses liquid carbon dioxide as a working fluid. Evaporation of the carbon dioxide provides cooling, and compression of the carbon dioxide gas back to the liquid state provides heat. The amount of heat transferred at both stages is sufficient to provide environmental heating and cooling. Waste thermal energy from a power plant, in the form of hot water, is fed into the system and used to drive the overall process. An underground thermal energy storage system is used to store energy flowing into the system that is in excess of the current demand.

**Avaliação do LLM:**
Esta patente descreve um sistema para distribuição de energia que utiliza dióxido de carbono como fluido de trabalho, aproveitando a evaporação e compressão para gerar aquecimento e resfriamento. O sistema incorpora um armazenamento de energia térmica subterrâneo para otimizar o uso de energia excedente, particularmente de fontes como usinas termelétricas.

**Extração Estruturada:**
- **Problema:** O problema abordado é a utilização de energia térmica residual, como a de usinas termelétricas, de forma eficiente, permitindo seu armazenamento e reutilização para aplicações de aquecimento e resfriamento.
- **Solução:** A solução proposta é um sistema que utiliza dióxido de carbono para armazenar e transferir energia térmica, com um sistema de armazenamento subterrâneo para otimizar o armazenamento de energia excedente.
- **Maturidade:** Intermediária

**Achados-chave:**
- Utilização de dióxido de carbono como fluido de trabalho para transferência de energia térmica.
- Incorporação de um sistema de armazenamento subterrâneo de energia térmica para otimizar o uso de energia excedente.

**Vantagens alegadas:**
- Otimização do uso de energia térmica residual.
- Possibilidade de armazenamento de energia para uso posterior.

**Limitações:**
- Dependência de um sistema de armazenamento subterrâneo.
- Eficiência do sistema pode ser afetada por perdas de calor durante o armazenamento.

**Aplicações potenciais:**
- Armazenamento de energia térmica em usinas termelétricas.
- Sistemas de aquecimento e resfriamento de edifícios.
- Integração com fontes de energia renovável.

**Evidências citadas:**
> AbstractThe invention provides a system for energy distribution that uses liquid carbon dioxide as a working fluid.
> An underground thermal energy storage system is used to store energy flowing into the system that is in excess of the current demand.

---

### 6. 1. AU2019901965 - A System to Improve Performance of Transcritical Carbon Dioxide Cooling by Integration of Ice Thermal Storage for Subcooling

| Campo | Valor |
|-------|-------|
| **Record ID** | `rec_5cb75be738eb` |
| **Family ID** | `family:f2562110d58e9c2be7e7177585da03af0dd8bffa` |
| **ID** | `AU244427549` |
| **Inventores** | N/A |
| **Titular** | IceCap; Thermal; Energy; Pty Ltd; KALDORBULL PTY LTD |
| **Data** | 20.06.2019 |
| **Fonte** | Patentscope |
| **URL** | [AU244427549](https://patentscope.wipo.int/search/en/detail.jsf;jsessionid=BAAD772379BE651666C3D16A4E44112D.wapp2nB?docId=AU244427549&_cid=P21-MNS7A1-22073-1) |
| **Triagem** | review |
| **Rota** | manual_review |
| **Motivo da rota** | Triagem indicou revisão humana. |
| **Score de Triagem** | 7.2/10 |
| **Score de Relevância** | 6.5/10 |
| **Nível de Inovação** | Incremental |
| **Domínio Técnico** | Sistemas de Refrigeração, Armazenamento Térmico, Engenharia Térmica |
| **Cluster Temático** | Armazenamento de Energia Térmica com CO2 |
| **Confiança** | 0.79 |
| **Revisão Manual** | Sim |
| **Erro LLM** | N/A |

**Avaliação do LLM:**
Esta patente descreve um sistema para melhorar o desempenho de sistemas de refrigeração transcríticos utilizando a integração de armazenamento térmico de gelo com dióxido de carbono (CO2). O sistema visa otimizar o subresfriamento do CO2, aumentando a eficiência do ciclo de refrigeração. A patente se concentra na utilização do CO2 como fluido refrigerante e no armazenamento de energia térmica através de gelo.

**Extração Estruturada:**
- **Problema:** O sistema busca abordar a ineficiência em sistemas de refrigeração transcríticos, onde o subresfriamento do CO2 pode ser um gargalo que limita o desempenho geral.
- **Solução:** A solução proposta é integrar um sistema de armazenamento de gelo com o ciclo de refrigeração transcrítico de CO2, permitindo que o gelo absorva o calor excedente e o libere quando necessário, otimizando o subresfriamento do fluido refrigerante.
- **Maturidade:** Inicial

**Achados-chave:**
- Utilização de CO2 como fluido refrigerante em um sistema de refrigeração transcrítico.
- Integração de armazenamento de gelo para otimizar o subresfriamento do CO2.
- Otimização do desempenho do ciclo de refrigeração transcrítico.

**Vantagens alegadas:**
- Melhora no desempenho do sistema de refrigeração transcrítico.
- Aumento da eficiência do ciclo de refrigeração.
- Potencial para reduzir o consumo de energia.

**Limitações:**
- Dependência da disponibilidade e gestão do gelo para o armazenamento térmico.
- Potenciais desafios relacionados à manutenção e ao ciclo de vida do sistema de armazenamento de gelo.

**Aplicações potenciais:**
- Sistemas de refrigeração transcríticos em diversas indústrias (alimentos, eletrônicos, etc.).
- Aplicações de resfriamento de processos industriais.
- Armazenamento de energia térmica em sistemas de aquecimento e resfriamento.

**Evidências citadas:**
> AU2019901965 - A System to Improve Performance of Transcritical Carbon Dioxide Cooling by Integration of Ice Thermal Storage for Subcooling

---

### 7. 2. US20240229681 - Calcination system with thermal energy storage system

| Campo | Valor |
|-------|-------|
| **Record ID** | `rec_0d58733a5389` |
| **Family ID** | `family:a5909788b69b641216917fdfccb844df018cba89` |
| **ID** | `US433566429` |
| **Inventores** | John Setel O'Donnell, Peter Emery von Behrens, Chiaki Treynor, Matthieu Jonemann, Robert Ratz, Yusef Desjardins Ferhani |
| **Titular** | Rondo; Energy; , Inc. |
| **Data** | 11.07.2024 |
| **Fonte** | Patentscope |
| **URL** | [US433566429](https://patentscope.wipo.int/search/en/detail.jsf;jsessionid=BAAD772379BE651666C3D16A4E44112D.wapp2nB?docId=US433566429&_cid=P21-MNS7A1-22073-1) |
| **Triagem** | exclude |
| **Rota** | screen_only |
| **Motivo da rota** | Patente excluída na triagem. |
| **Score de Triagem** | 3.5/10 |
| **Score de Relevância** | 0.0/10 |
| **Nível de Inovação** | N/A |
| **Domínio Técnico** | Armazenamento de Energia Térmica, Geração de Calor |
| **Cluster Temático** | Armazenamento de Energia em Meio Sólido com Aplicações de Alta Temperatura |
| **Confiança** | 0.70 |
| **Revisão Manual** | Não |
| **Erro LLM** | N/A |

**Abstract:**
> (EN)Anenergystoragesystem converts variable renewable electricity (VRE) to continuous heat at over 1000° C. Intermittent electricalenergyheats a solid medium. Heat from the solid medium is delivered continuously on demand. An array of bricks incorporating internal radiation cavities is directly heated bythermalradiation. The cavities facilitate rapid, uniform heating via reradiation. Heat delivery via flowing gas establishes a thermocline which maintains high outlet temperature throughout discharge. Gas flows through structured pathways within the array, delivering heat which may be used for processes including calcination, hydrogen electrolysis, steam generation, andthermalpower generation and cogeneration. Groups ofthermalstoragearrays may be controlled and operated at high temperatures withoutthermalrunaway via deep-discharge sequencing. Forecast-based control enables continuous, year-round heat supply using current and advance information of weather and VRE availability. High-voltage DC power conversion and distribution circuitry improves the efficiency of VRE power transfer into the system.

**Evidências citadas:**
> An energystoragesystem converts variable renewable electricity (VRE) to continuous heat at over 1000° C.
> Heat from the solid medium is delivered continuously on demand.

---

### 8. 3. US20230203968 - Methods for material activation with thermal energy storage system

| Campo | Valor |
|-------|-------|
| **Record ID** | `rec_3da6b58fde67` |
| **Family ID** | `family:05206822f399c166b617cf99088b736afdf59e4b` |
| **ID** | `US400261922` |
| **Inventores** | John Setel O'Donnell, Peter Emery von Behrens, Chiaki Treynor, Jeremy Quentin Keller, Matthieu Jonemann, Robert Ratz, Yusef Desjardins Ferhani |
| **Titular** | Rondo; Energy; , Inc. |
| **Data** | 29.06.2023 |
| **Fonte** | Patentscope |
| **URL** | [US400261922](https://patentscope.wipo.int/search/en/detail.jsf;jsessionid=BAAD772379BE651666C3D16A4E44112D.wapp2nB?docId=US400261922&_cid=P21-MNS7A1-22073-1) |
| **Triagem** | exclude |
| **Rota** | screen_only |
| **Motivo da rota** | Patente excluída na triagem. |
| **Score de Triagem** | 3.5/10 |
| **Score de Relevância** | 0.0/10 |
| **Nível de Inovação** | N/A |
| **Domínio Técnico** | Armazenamento de Energia Térmica, Engenharia de Calor |
| **Cluster Temático** | Armazenamento de Energia em Meio Sólido com Aplicações de Alta Temperatura |
| **Confiança** | 0.79 |
| **Revisão Manual** | Não |
| **Erro LLM** | N/A |

**Abstract:**
> (EN)Anenergystoragesystem converts variable renewable electricity (VRE) to continuous heat at over 1000° C. Intermittent electricalenergyheats a solid medium. Heat from the solid medium is delivered continuously on demand. An array of bricks incorporating internal radiation cavities is directly heated bythermalradiation. The cavities facilitate rapid, uniform heating via reradiation. Heat delivery via flowing gas establishes a thermocline which maintains high outlet temperature throughout discharge. Gas flows through structured pathways within the array, delivering heat which may be used for processes including calcination, hydrogen electrolysis, steam generation, andthermalpower generation and cogeneration. Groups ofthermalstoragearrays may be controlled and operated at high temperatures withoutthermalrunaway via deep-discharge sequencing. Forecast-based control enables continuous, year-round heat supply using current and advance information of weather and VRE availability. High-voltage DC power conversion and distribution circuitry improves the efficiency of VRE power transfer into the system.

**Evidências citadas:**
> An energystoragesystem converts variable renewable electricity (VRE) to continuous heat at over 1000° C.
> Heat from the solid medium is delivered continuously on demand. An array of bricks incorporating internal radiation cavities is directly heated by thermal radiation.

---

### 9. 4. US20240229682 - Methods for material activation with thermal energy storage system

| Campo | Valor |
|-------|-------|
| **Record ID** | `rec_d53841fc186a` |
| **Family ID** | `family:5759c6bc508072e5f9d303a96f846c77f3fcfe07` |
| **ID** | `US433566430` |
| **Inventores** | John Setel O'Donnell, Peter Emery von Behrens, Matthieu Jonemann, Yusef Desjardins Ferhani |
| **Titular** | Rondo; Energy; , Inc. |
| **Data** | 11.07.2024 |
| **Fonte** | Patentscope |
| **URL** | [US433566430](https://patentscope.wipo.int/search/en/detail.jsf;jsessionid=BAAD772379BE651666C3D16A4E44112D.wapp2nB?docId=US433566430&_cid=P21-MNS7A1-22073-1) |
| **Triagem** | exclude |
| **Rota** | screen_only |
| **Motivo da rota** | Patente excluída na triagem. |
| **Score de Triagem** | 3.5/10 |
| **Score de Relevância** | 0.0/10 |
| **Nível de Inovação** | N/A |
| **Domínio Técnico** | Armazenamento de Energia, Engenharia Térmica, Materiais |
| **Cluster Temático** | Armazenamento de Energia Térmica com Eletricidade Renovável |
| **Confiança** | 0.79 |
| **Revisão Manual** | Não |
| **Erro LLM** | N/A |

**Abstract:**
> (EN)Anenergystoragesystem converts variable renewable electricity (VRE) to continuous heat at over 1000° C. Intermittent electricalenergyheats a solid medium. Heat from the solid medium is delivered continuously on demand. An array of bricks incorporating internal radiation cavities is directly heated bythermalradiation. The cavities facilitate rapid, uniform heating via reradiation. Heat delivery via flowing gas establishes a thermocline which maintains high outlet temperature throughout discharge. Gas flows through structured pathways within the array, delivering heat which may be used for processes including calcination, hydrogen electrolysis, steam generation, andthermalpower generation and cogeneration. Groups ofthermalstoragearrays may be controlled and operated at high temperatures withoutthermalrunaway via deep-discharge sequencing. Forecast-based control enables continuous, year-round heat supply using current and advance information of weather and VRE availability. High-voltage DC power conversion and distribution circuitry improves the efficiency of VRE power transfer into the system.

**Evidências citadas:**
> Anenergystoragesystem converts variable renewable electricity (VRE) to continuous heat at over 1000° C.
> Heat from the solid medium is delivered continuously on demand. An array of bricks incorporating internal radiation cavities is directly heated bythermalradiation.

---

### 10. 5. US20220282638 - Material activation system with thermal energy storage system

| Campo | Valor |
|-------|-------|
| **Record ID** | `rec_e94308d296fb` |
| **Family ID** | `family:edd5cd46beac8cd878fb34bf81f89eeab14f618e` |
| **ID** | `US373267798` |
| **Inventores** | John Setel O'Donnell, Peter Emery von Behrens, Chiaki Treynor, Jeremy Quentin Keller, Matthieu Jonemann, Robert Ratz, Yusef Desjardins Ferhani |
| **Titular** | Rondo; Energy; , Inc. |
| **Data** | 08.09.2022 |
| **Fonte** | Patentscope |
| **URL** | [US373267798](https://patentscope.wipo.int/search/en/detail.jsf;jsessionid=BAAD772379BE651666C3D16A4E44112D.wapp2nB?docId=US373267798&_cid=P21-MNS7A1-22073-1) |
| **Triagem** | exclude |
| **Rota** | screen_only |
| **Motivo da rota** | Patente excluída na triagem. |
| **Score de Triagem** | 3.5/10 |
| **Score de Relevância** | 0.0/10 |
| **Nível de Inovação** | N/A |
| **Domínio Técnico** | Armazenamento de Energia, Termodinâmica, Engenharia Química |
| **Cluster Temático** | Armazenamento de Energia em Alta Temperatura |
| **Confiança** | 0.66 |
| **Revisão Manual** | Não |
| **Erro LLM** | N/A |

**Abstract:**
> (EN)Anenergystoragesystem converts variable renewable electricity (VRE) to continuous heat at over 1000° C. Intermittent electricalenergyheats a solid medium. Heat from the solid medium is delivered continuously on demand. An array of bricks incorporating internal radiation cavities is directly heated bythermalradiation. The cavities facilitate rapid, uniform heating via reradiation. Heat delivery via flowing gas establishes a thermocline which maintains high outlet temperature throughout discharge. Gas flows through structured pathways within the array, delivering heat which may be used for processes including calcination, hydrogen electrolysis, steam generation, andthermalpower generation and cogeneration. Groups ofthermalstoragearrays may be controlled and operated at high temperatures withoutthermalrunaway via deep-discharge sequencing. Forecast-based control enables continuous, year-round heat supply using current and advance information of weather and VRE availability. High-voltage DC power conversion and distribution circuitry improves the efficiency of VRE power transfer into the system.

**Evidências citadas:**
> An energystoragesystem converts variable renewable electricity (VRE) to continuous heat at over 1000° C.
> Heat from the solid medium is delivered continuously on demand.

---

## 🧾 Fila de Revisão Manual

- rec_d32965bf3945 (US20200182095A1) | rota=manual_review | motivo=Triagem indicou revisão humana. | erro_llm=N/A
- rec_5cb75be738eb (AU244427549) | rota=manual_review | motivo=Triagem indicou revisão humana. | erro_llm=N/A

---

## 🔬 Análise Comparativa

### 1. Panorama Geral

- O conjunto incluído contém 4 patente(s) e não deve ser tratado como um bloco homogêneo; ele combina arquiteturas centradas em armazenamento explícito de CO2 com soluções mais adjacentes de transferência/distribuição térmica usando CO2 como fluido de trabalho [IDs: CN118934113A, CN115234318A, US20230029186A1, WO2021081541A1]
- O subgrupo mais diretamente alinhado ao núcleo da query é CN118934113A, CN115234318A, com foco em armazenamento de CO2, compressão/expansão e controle termodinâmico do meio armazenado [IDs: CN118934113A, CN115234318A]
- CN115234318A, US20230029186A1, WO2021081541A1 tratam CO2 principalmente como fluido de trabalho em transferência térmica ou distribuição de energia; nesses casos o armazenamento aparece como subsistema associado ou contexto operacional, não necessariamente como o núcleo arquitetural [IDs: CN115234318A, US20230029186A1, WO2021081541A1]
- A menção a armazenamento subterrâneo ou subaquático aparece apenas em CN118934113A, US20230029186A1, WO2021081541A1 e não deve ser generalizada para todo o conjunto incluído [IDs: CN118934113A, US20230029186A1, WO2021081541A1]

## Análise Comparativa de Patentes: Armazenamento Térmico de Energia com Dióxido de Carbono

### 2. Tendências Identificadas

*   **Ciclos de Evaporação/Compressão:** Todas as patentes exploram o uso de ciclos de evaporação e compressão do CO2 líquido para a conversão de energia térmica, indicando uma tendência central no domínio [IDs: CN118934113A, CN115234318A, US20230029186A1, WO2021081541A1].
*   **Armazenamento Subterrâneo:**  Várias patentes (CN115234318A, US20230029186A1, WO2021081541A1)  enfatizam o uso de sistemas de armazenamento de energia térmica subterrâneos para o armazenamento de energia excedente [IDs: CN115234318A, US20230029186A1, WO2021081541A1].
*   **Integração com Termelétricas:** CN115234318A destaca a integração do sistema de armazenamento de CO2 com usinas termelétricas para "deep peak shaving" [IDs: CN115234318A].
*   **Transferência de Calor:** A US20230029186A1 e as WO2021081541A1  demonstram o uso do CO2 como fluido de trabalho para transferência de calor, incluindo sistemas subterrâneos [IDs: US20230029186A1, WO2021081541A1].

### 3. Lacunas e Oportunidades

*   **Otimização de Ciclos:**  A análise das patentes sugere uma lacuna na otimização dos ciclos de evaporação/compressão do CO2 para maximizar a eficiência energética em diferentes aplicações e condições de operação [IDs: CN118934113A, CN115234318A, US20230029186A1, WO2021081541A1].
*   **Materiais de Isolamento:**  A utilização de armazenamento subterrâneo apresenta a necessidade de investigar e desenvolver materiais de isolamento térmico mais eficientes para os sistemas [IDs: CN115234318A, US20230029186A1, WO2021081541A1].
*   **Controle Térmico Avançado:** Existe uma oportunidade para desenvolver sistemas de controle térmico mais sofisticados, capazes de adaptar-se dinamicamente às variações de demanda e às características do meio de armazenamento [IDs: CN118934113A, CN115234318A, US20230029186A1, WO2021081541A1].

### 4. Recomendações

*   **Pesquisa em Ciclos Termodinâmicos:**  Investigar e desenvolver novos ciclos termodinâmicos que utilizem CO2, otimizando a eficiência energética e a capacidade de armazenamento [IDs: CN118934113A, CN115234318A, US20230029186A1, WO2021081541A1].
*   **Estudos de Materiais:** Realizar estudos aprofundados sobre materiais de isolamento térmico para sistemas de armazenamento subterrâneo, buscando alternativas com melhor desempenho e custo-benefício [IDs: CN115234318A, US20230029186A1, WO2021081541A1].
*   **Integração com Redes Inteligentes:** Explorar a integração dos sistemas de armazenamento de CO2 com redes inteligentes de energia, permitindo uma gestão mais eficiente da demanda e da oferta de energia [IDs: CN118934113A, CN115234318A, US20230029186A1, WO2021081541A1].

### 5. Ranking Final

1. **CN118934113A** — armazenamento explícito de CO2 como núcleo da arquitetura; score 10.0/10 [IDs: CN118934113A]
2. **CN115234318A** — armazenamento explícito de CO2 como núcleo da arquitetura; CO2 usado principalmente como fluido de trabalho para transferência térmica; score 9.4/10 [IDs: CN115234318A]
3. **US20230029186A1** — CO2 usado principalmente como fluido de trabalho para transferência térmica; armazenamento subterrâneo aparece como subsistema de suporte; score 8.0/10 [IDs: US20230029186A1]
4. **WO2021081541A1** — CO2 usado principalmente como fluido de trabalho para transferência térmica; armazenamento subterrâneo aparece como subsistema de suporte; score 8.0/10 [IDs: WO2021081541A1]

### 6. Mapa de Evidências por ID

- **CO2 Cycle Configurations** [IDs: CN118934113A, CN115234318A]
- **Thermal Transfer Mechanisms** [IDs: US20230029186A1, WO2021081541A1]

### 7. Ranking por ID

1. **CN118934113A** — score 10.0/10 [IDs: CN118934113A]
2. **CN115234318A** — score 9.4/10 [IDs: CN115234318A]
3. **US20230029186A1** — score 8.0/10 [IDs: US20230029186A1]
4. **WO2021081541A1** — score 8.0/10 [IDs: WO2021081541A1]

---

## ℹ️ Informações do Sistema

- **Gerado por:** Agente de Web Scraping de Patentes
- **Modelo LLM:** gemma3:4b
- **Data de geração:** 09/04/2026 22:02:37
- **Query de busca:** `carbon dioxide thermal energy storage`
- **Status da execução:** completed
- **Tempo total:** 92.0s
- **LLM disponível:** sim
- **Fila de revisão manual:** 2 itens
- **Snapshot hash:** `d465fc231267bbc19e7129cceb179b71680903700d7111352674a3e221bfcf40`
- **Features habilitadas:** require_evidence, enable_thematic_clusters, enable_prisma, enable_snapshot, enable_comparative_analysis, enable_manual_review_queue
- **Features desabilitadas:** nenhum
- **Versão do pipeline:** 1.1
- **Thresholds snapshot:** include=7.0, review=4.5
- **Cache LLM:** 0 hits, 17 misses, 17 entradas
- **Status do rascunho:** ready