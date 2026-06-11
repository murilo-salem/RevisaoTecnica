# 📋 Relatório de Análise de Patentes

**Data:** 06/04/2026 01:16:41
**Busca:** `carbon dioxide thermal energy storage`
**Total de patentes encontradas:** 20
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

- **Total bruto coletado:** 20
- **Patentes únicas:** 20
- **Duplicatas removidas:** 0
- **Triadas:** 20
- **Incluídas:** 7
- **Em revisão manual:** 4
- **Excluídas:** 9
- **Extrações completas:** 11
- **Sem abstract/snippet:** 1
- **Sem ID:** 0
- **Identidade por conteúdo:** 0
- **Identidade fallback:** 0
- **Duplicatas por família removidas:** 0
- **Falhas de triagem LLM:** 0
- **Falhas totais LLM:** 0

## 🧭 Fluxo PRISMA-Like

- **Identificação:** 20 bruto(s), 20 único(s), 0 duplicata(s) removida(s)
- **Triagem:** 20 triado(s), 7 incluído(s), 4 em revisão, 9 excluído(s)
- **Elegibilidade:** 11 extração(ões) completa(s), 4 revisão(ões) manual(is), 0 adiada(s)
- **Cobertura:** 1 sem abstract/snippet, 0 sem ID
- **Síntese:** 11 registro(s) analisado(s)

## 🧩 Síntese Temática

### Thermal Transfer Mechanisms

- **Patentes:** 3
- **Score médio:** 8.53/10
- **Confiança média:** 0.93
- **Evidências citadas:** 5
- **IDs:** WO2021081541A1, US20230029186A1, CN117318319B

### CO2 Cycle Configurations

- **Patentes:** 2
- **Score médio:** 9.35/10
- **Confiança média:** 0.92
- **Evidências citadas:** 4
- **IDs:** CN118934113A, CN116164573B

### Armazenamento de Energia, Termodinâmica, Engenharia de Usinas Termelétricas

- **Patentes:** 1
- **Score médio:** 9.40/10
- **Confiança média:** 0.95
- **Evidências citadas:** 2
- **IDs:** CN115234318A

### CO2 Phase Properties

- **Patentes:** 1
- **Score médio:** 9.20/10
- **Confiança média:** 0.95
- **Evidências citadas:** 2
- **IDs:** CN117266954B

## 🧠 Contexto Compartilhado

- **Top patentes no contexto:** 5
- **Clusters no contexto:** 4
- **Roteamento agregado:** 3 rota(s)
- **Slots ativos:** N/A

## ⏱️ Métricas por Etapa

| Etapa | Status | Duração | Itens | Detalhes |
|---|---|---:|---:|---|
| setup | ok | 0.34s | 1 | Verificação do modelo Ollama |
| search | ok | 93.00s | 20 | 20 patentes únicas após dedupe |
| screening | ok | 60.86s | 20 | 7 incluídas, 4 revisão |
| comparative_analysis | ok | 6.61s | 20 | Síntese comparativa gerada |
| reporting | ok | 0.00s | 20 | Relatórios Markdown e JSON |
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
- **Latência média:** 0.34s
- **Latência máxima:** 0.34s

### screening

- **Chamadas:** 20
- **Sucessos:** 20
- **Falhas:** 0
- **Retries:** 0
- **Cache hits:** 0
- **Pulos por degradação:** 0
- **Latência média:** 1.38s
- **Latência máxima:** 2.927s

### evaluation

- **Chamadas:** 11
- **Sucessos:** 11
- **Falhas:** 0
- **Retries:** 0
- **Cache hits:** 0
- **Pulos por degradação:** 0
- **Latência média:** 3.023s
- **Latência máxima:** 4.151s

### comparative

- **Chamadas:** 1
- **Sucessos:** 1
- **Falhas:** 0
- **Retries:** 0
- **Cache hits:** 0
- **Pulos por degradação:** 0
- **Latência média:** 6.606s
- **Latência máxima:** 6.606s

## 🔎 Observabilidade Estruturada

### Rotas

- **screen_only**: total=9, include=0, review=0, exclude=9, llm_errors=0
- **deep_extraction**: total=7, include=7, review=0, exclude=0, llm_errors=0
- **manual_review**: total=4, include=0, review=4, exclude=0, llm_errors=0

### Fontes

- **GooglePatents**: bruto=10, duração=26.66s, diagnósticos=nenhum
- **Patentscope**: bruto=10, duração=66.33s, diagnósticos=discovery_empty=1

### Falhas

- **Erros de execução:** 0
- **Registros com erro de LLM:** 0
- **Falhas totais do LLM:** 0
- **LLM por operação:** comparative(falhas=0, retries=0, skips=0), evaluation(falhas=0, retries=0, skips=0), healthcheck(falhas=0, retries=0, skips=0), screening(falhas=0, retries=0, skips=0)
- **Scraper por tipo de sinal:** discovery_empty=1

## 📊 Resumo Executivo

**Score médio de relevância:** 9.0/10

| # | Patente | Score | Inovação | Domínio |
|---|---------|-------|----------|---------|
| 1 | [CN118934113A](https://patents.google.com/patent/CN118934113A/en) — An isothermal and isobaric supercritical compressed carbon d... | 🟢 10.0 (include) | Significativa | Engenharia Termodinâmica, Armazenamento de Energia |
| 2 | [CN117318319B](https://patents.google.com/patent/CN117318319B/en) — Carbon dioxide energy storage system and method using carbon... | 🟢 9.6 (include) | Significativa | Armazenamento de Energia, Termodinâmica, Engenharia de Refrigeração |
| 3 | [CN115234318A](https://patents.google.com/patent/CN115234318A/en) — Carbon dioxide energy storage system matched with thermal po... | 🟢 9.4 (include) | Incremental | Armazenamento de Energia, Termodinâmica, Engenharia de Usinas Termelétricas |
| 4 | [CN117266954B](https://patents.google.com/patent/CN117266954B/en) — Liquid carbon dioxide energy storage system | 🟢 9.2 (include) | Incremental | Armazenamento de Energia Térmica |
| 5 | [CN116164573B](https://patents.google.com/patent/CN116164573B/en) — A dry ice energy storage system and method based on carbon d... | 🟢 8.7 (include) | Incremental | Armazenamento de Energia, Termodinâmica, Engenharia de Gases |
| 6 | [WO2021081541A1](https://patents.google.com/patent/WO2021081541A1/en) — Method for thermal energy transmission using water and carbo... | 🟢 8.0 (include) | Incremental | Armazenamento de Energia, Termodinâmica, Engenharia de Sistemas |
| 7 | [US20230029186A1](https://patents.google.com/patent/US20230029186A1/en) — Method for thermal energy transmission using water and carbo... | 🟢 8.0 (include) | Significativa | Armazenamento de Energia, Termodinâmica, Engenharia de Fluidos |
| 8 | [US20200182095A1](https://patents.google.com/patent/US20200182095A1/en) — Carbon dioxide upgrade and energy storage system and method | 🟡 6.5 (review) | Incremental | Engenharia Termodinâmica, Armazenamento de Energia |
| 9 | [CN114930087A](https://patents.google.com/patent/CN114930087A/en) — Thermal energy transfer method using water and carbon dioxid... | 🟡 6.5 (review) | Significativa | Armazenamento de Energia Térmica, Ciclo de Refrigeração |
| 10 | [KR20140023113A](https://patents.google.com/patent/KR20140023113A/en) — The carbon dioxide capture and storage system by using heat ... | 🟡 6.5 (review) | Significativa | Captura e Armazenamento de Carbono, Termodinâmica, Bomba de Calor, Células de Combustível |
| 11 | [AU244427549](https://patentscope.wipo.int/search/en/detail.jsf;jsessionid=2511917E8505F03BC8500F97357E5851.wapp2nC?docId=AU244427549&_cid=P22-MNMOEY-15419-1) — 1. AU2019901965 - A System to Improve Performance of Transcr... | 🟡 6.5 (review) | Incremental | Refrigeração, Armazenamento Térmico, Ciclo Transcíclico |
| 12 | [US433566429](https://patentscope.wipo.int/search/en/detail.jsf;jsessionid=2511917E8505F03BC8500F97357E5851.wapp2nC?docId=US433566429&_cid=P22-MNMOEY-15419-1) — 2. US20240229681 - Calcination system with thermal energy st... | 🔴 0.0 (exclude) | N/A | Armazenamento de Energia Térmica, Engenharia Química |
| 13 | [US400261922](https://patentscope.wipo.int/search/en/detail.jsf;jsessionid=2511917E8505F03BC8500F97357E5851.wapp2nC?docId=US400261922&_cid=P22-MNMOEY-15419-1) — 3. US20230203968 - Methods for material activation with ther... | 🔴 0.0 (exclude) | N/A | Armazenamento de Energia Térmica, Geração de Energia |
| 14 | [US433566430](https://patentscope.wipo.int/search/en/detail.jsf;jsessionid=2511917E8505F03BC8500F97357E5851.wapp2nC?docId=US433566430&_cid=P22-MNMOEY-15419-1) — 4. US20240229682 - Methods for material activation with ther... | 🔴 0.0 (exclude) | N/A | Armazenamento de Energia, Termodinâmica, Engenharia de Processos |
| 15 | [US373267798](https://patentscope.wipo.int/search/en/detail.jsf;jsessionid=2511917E8505F03BC8500F97357E5851.wapp2nC?docId=US373267798&_cid=P22-MNMOEY-15419-1) — 5. US20220282638 - Material activation system with thermal e... | 🔴 0.0 (exclude) | N/A | Armazenamento de Energia Térmica, Termodinâmica, Geração de Energia |
| 16 | [US403483831](https://patentscope.wipo.int/search/en/detail.jsf;jsessionid=2511917E8505F03BC8500F97357E5851.wapp2nC?docId=US403483831&_cid=P22-MNMOEY-15419-1) — 6. US20230243278 - Energy storage system and applications | 🔴 0.0 (exclude) | N/A | Armazenamento de Energia Térmica, Termodinâmica |
| 17 | [US377255809](https://patentscope.wipo.int/search/en/detail.jsf;jsessionid=2511917E8505F03BC8500F97357E5851.wapp2nC?docId=US377255809&_cid=P22-MNMOEY-15419-1) — 7. US20220341349 - Solid oxide electrolysis system with ther... | 🔴 0.0 (exclude) | N/A | Armazenamento de Energia, Eletroquímica, Engenharia Térmica |
| 18 | [EP449228070](https://patentscope.wipo.int/search/en/detail.jsf;jsessionid=2511917E8505F03BC8500F97357E5851.wapp2nC?docId=EP449228070&_cid=P22-MNMOEY-15419-1) — 8. EP4509205 - ENERGY STORAGE SYSTEM AND APPLICATIONS | 🔴 0.0 (exclude) | N/A | Armazenamento de Energia Térmica, Termodinâmica |
| 19 | [US432849550](https://patentscope.wipo.int/search/en/detail.jsf;jsessionid=2511917E8505F03BC8500F97357E5851.wapp2nC?docId=US432849550&_cid=P22-MNMOEY-15419-1) — 9. US20240218811 - Thermal energy storage system with deep d... | 🔴 0.0 (exclude) | N/A | Armazenamento de Energia Térmica, Geração de Energia |
| 20 | [US371833683](https://patentscope.wipo.int/search/en/detail.jsf;jsessionid=2511917E8505F03BC8500F97357E5851.wapp2nC?docId=US371833683&_cid=P22-MNMOEY-15419-1) — 10. US20220259988 - Thermal energy storage system with steam... | 🔴 0.0 (exclude) | N/A | Armazenamento de Energia Térmica, Geração de Vapor, Cogeração |

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
Esta patente descreve um sistema de armazenamento de energia utilizando dióxido de carbono supercrítico em condições isobáricas e isotérmicas, com componentes chave incluindo um compressor, expansor, câmaras de armazenamento de alta e baixa pressão, e trocadores de calor. O sistema visa manter parâmetros térmicos estáveis durante o ciclo de armazenamento e recuperação de energia. A inovação reside na utilização de dióxido de carbono supercrítico para otimizar o armazenamento térmico.

**Extração Estruturada:**
- **Problema:** O problema abordado é a necessidade de um sistema de armazenamento de energia que possa utilizar as propriedades termodinâmicas do dióxido de carbono supercrítico de forma eficiente e estável, permitindo o armazenamento e a recuperação de energia térmica.
- **Solução:** A solução proposta é um sistema de armazenamento de energia que utiliza dióxido de carbono supercrítico em condições isobáricas e isotérmicas, com um ciclo que envolve compressão, expansão, armazenamento e troca de calor para armazenar e recuperar energia térmica de forma eficiente.
- **Maturidade:** Inicial

**Achados-chave:**
- O sistema utiliza um compressor para comprimir dióxido de carbono supercrítico e um expansor para gerar eletricidade.
- A configuração inclui câmaras de armazenamento de alta e baixa pressão, juntamente com trocadores de calor para controlar a temperatura do dióxido de carbono supercrítico.

**Vantagens alegadas:**
- Eficiência no armazenamento e recuperação de energia térmica.
- Estabilidade térmica do sistema devido ao controle preciso da temperatura.

**Limitações:**
- A patente não detalha especificamente os materiais utilizados nos componentes do sistema ou as condições operacionais ideais.
- A viabilidade econômica do sistema pode depender do custo de implementação e manutenção.

**Aplicações potenciais:**
- Armazenamento de energia renovável (solar, eólica).
- Geração de energia de calor residual.
- Sistemas de aquecimento e resfriamento industrial.

**Evidências citadas:**
> æ¬åææ¶åè¶ä¸´çåç¼©äºæ°§åç¢³å¨è½ææ¯é¢åï¼ç­æ¸©ç­åçè¶ä¸´çåç¼©äºæ°§åç¢³å¨è½ç³»ç»ï¼
> åæ¬ï¼åç¼©æºç»ï¼å©ç¨çµåå°ä½æ¸©ä½åçè¶ä¸´çäºæ°§åç¢³åç¼©ä¸ºé«æ¸©é«åçè¶ä¸´çäºæ°§åç¢³ï¼è¨èæºç»ï¼

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
| **Domínio Técnico** | Armazenamento de Energia, Termodinâmica, Engenharia de Usinas Termelétricas |
| **Cluster Temático** | Armazenamento de Energia, Termodinâmica, Engenharia de Usinas Termelétricas |
| **Confiança** | 0.95 |
| **Revisão Manual** | Não |
| **Erro LLM** | N/A |

**Abstract:**
> AbstractThe invention provides a carbon dioxide energy storage system matched with deep peak shaving of a thermal power plant and a control method thereof, and relates to the technical field of energy storage. The energy storage system includes: the gas storage, the energy storage component, the liquid storage tank and the energy release component are sequentially connected in a closed loop manner, and the energy release component comprises an expander; the coupling assembly comprises a steam extraction bypass and a first heat storage module; the steam extraction bypass is used for guiding high-temperature steam in the steam turbine to the first heat storage module when the thermal power plant is in a deep peak shaving working condition; the first heat storage module is connected with the energy release assembly and used for storing heat contained in the high-temperature steam and providing heat for the energy release assembly when the energy release assembly works so as to improve the temperature of carbon dioxide at the inlet of the expansion machine. The carbon dioxide energy storage system and the control method can improve the peak regulation flexibility and safety of the thermal power plant and can also improve the work efficiency of the carbon dioxide.

**Avaliação do LLM:**
Esta patente descreve um sistema de armazenamento de energia de dióxido de carbono integrado a uma usina termelétrica, focado em 'deep peak shaving' e controle. O sistema utiliza um ciclo de expansão com um módulo de armazenamento de calor para otimizar a utilização de energia e regular a produção da usina termelétrica.

**Extração Estruturada:**
- **Problema:** O problema abordado é a necessidade de flexibilidade e segurança na regulação de energia de usinas termelétricas, particularmente durante picos de demanda.
- **Solução:** A solução proposta é um sistema de armazenamento de energia de CO2 que utiliza um ciclo de expansão com um módulo de armazenamento de calor para armazenar e liberar calor, permitindo o controle e a redução dos picos de demanda da usina termelétrica.
- **Maturidade:** Intermediária

**Achados-chave:**
- O sistema inclui um expander para converter a energia térmica do CO2 em energia mecânica.
- Um primeiro módulo de armazenamento de calor é usado para armazenar o calor do vapor de alta temperatura extraído da turbina a vapor.

**Vantagens alegadas:**
- Melhora a flexibilidade e segurança da regulação de energia da usina termelétrica.
- Aumenta a eficiência do uso do CO2.

**Limitações:**
- A patente não detalha a capacidade de armazenamento de energia ou a eficiência do sistema.
- A viabilidade econômica do sistema depende de fatores como o custo do CO2 e a eficiência do ciclo de expansão.

**Aplicações potenciais:**
- Usinas termelétricas com capacidade de armazenamento de energia.
- Sistemas de energia distribuída com integração de armazenamento de energia de CO2.

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
| **Cluster Temático** | Ciclos Termodinâmicos com Dióxido de Carbono |
| **Confiança** | 0.79 |
| **Revisão Manual** | Sim |
| **Erro LLM** | N/A |

**Abstract:**
> AbstractA method for producing work is disclosed. The method includes increasing the pressure of a working fluid including carbon dioxide from a first pressure at least equal to a triple point pressure to a second pressure above the triple point pressure. The method also includes heating the working fluid, extracting mechanical work by expanding a first portion of the heated working fluid to a third pressure, supplying a second portion of the heated working fluid as a motive fluid to an ejector, increasing the pressure of the expanded working fluid by supplying the expanded working fluid to the ejector to combine with the motive fluid and form an output fluid at the fourth pressure, the fourth pressure at least equal to the triple point pressure of the working fluid. The method also includes refrigerating the output fluid to condense a vapor phase into a liquid phase.

**Avaliação do LLM:**
Esta patente descreve um sistema e método para a produção de trabalho utilizando dióxido de carbono, envolvendo aumento de pressão, aquecimento, expansão e condensação. O sistema utiliza um ciclo de trabalho com dióxido de carbono para extrair trabalho mecânico e potencialmente armazenar energia térmica.

**Extração Estruturada:**
- **Problema:** O problema abordado é a produção de trabalho a partir de um fluido de trabalho, especificamente dióxido de carbono, utilizando um ciclo termodinâmico.
- **Solução:** A solução proposta é um sistema que aumenta a pressão do dióxido de carbono, aquece-o, expande uma parte para extrair trabalho mecânico, e refrigera o fluido resultante para condensá-lo, criando um ciclo contínuo.
- **Maturidade:** Inicial

**Achados-chave:**
- O sistema utiliza um ciclo termodinâmico com dióxido de carbono, envolvendo pressão, aquecimento, expansão e condensação.
- A pressão do fluido de trabalho é aumentada a níveis acima da pressão do ponto triplo do dióxido de carbono.

**Vantagens alegadas:**
- Extração de trabalho mecânico a partir do ciclo termodinâmico.
- Possibilidade de armazenamento de energia térmica através do processo de condensação.

**Limitações:**
- A patente não detalha a eficiência do sistema ou as condições operacionais específicas.
- A aplicação do sistema pode ser limitada pela necessidade de fontes de calor e sistemas de refrigeração.

**Aplicações potenciais:**
- Sistemas de energia renovável
- Sistemas de armazenamento de energia térmica

**Evidências citadas:**
> “increasing the pressure of a working fluid including carbon dioxide from a first pressure at least equal to a triple point pressure to a second pressure above the triple point pressure.”
> “extracting mechanical work by expanding a first portion of the heated working fluid to a third pressure”

---

### 4. Method for thermal energy transmission using water and carbon dioxide

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
| **Domínio Técnico** | Armazenamento de Energia, Termodinâmica, Engenharia de Sistemas |
| **Cluster Temático** | Thermal Transfer Mechanisms |
| **Confiança** | 0.95 |
| **Revisão Manual** | Não |
| **Erro LLM** | N/A |

**Abstract:**
> AbstractThe invention provides a system for energy distribution that uses liquid carbon dioxide as a working fluid. Evaporation of the carbon dioxide provides cooling, and compression of the carbon dioxide gas back to the liquid state provides heat. The amount of heat transferred at both stages is sufficient to provide environmental heating and cooling. Waste thermal energy from a power plant, in the form of hot water, is fed into the system and used to drive the overall process. An underground thermal energy storage system is used to store energy flowing into the system that is in excess of the current demand.

**Avaliação do LLM:**
Esta patente descreve um sistema para distribuição de energia que utiliza dióxido de carbono como fluido de trabalho, aproveitando a evaporação e compressão para fornecer aquecimento e resfriamento. O sistema incorpora armazenamento de energia térmica subterrâneo para lidar com o excesso de energia proveniente de fontes como usinas termelétricas.

**Extração Estruturada:**
- **Problema:** O problema abordado é a gestão e utilização de energia térmica residual, especificamente 'waste thermal energy from a power plant', buscando uma forma eficiente de armazená-la e reutilizá-la.
- **Solução:** A solução proposta é um sistema que utiliza dióxido de carbono para absorver e liberar calor, com armazenamento subterrâneo de energia para otimizar a distribuição e utilização da energia térmica.
- **Maturidade:** Inicial

**Achados-chave:**
- Utilização de água e dióxido de carbono como fluido de trabalho.
- Incorporação de um sistema de armazenamento subterrâneo de energia para excedentes de energia.

**Vantagens alegadas:**
- Utilização de energia residual de usinas termelétricas.
- Capacidade de fornecer aquecimento e resfriamento ambiental.

**Limitações:**
- Dependência da disponibilidade de fontes de energia térmica residual.
- Potenciais desafios relacionados à eficiência do armazenamento subterrâneo.

**Aplicações potenciais:**
- Armazenamento de energia térmica em usinas termelétricas.
- Sistemas de aquecimento e resfriamento de edifícios.
- Integração com redes de energia renovável.

**Evidências citadas:**
> AbstractThe invention provides a system for energy distribution that uses liquid carbon dioxide as a working fluid.
> An underground thermal energy storage system is used to store energy flowing into the system that is in excess of the current demand.

---

### 5. Method for thermal energy transmission using water and carbon dioxide

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
| **Nível de Inovação** | Significativa |
| **Domínio Técnico** | Armazenamento de Energia, Termodinâmica, Engenharia de Fluidos |
| **Cluster Temático** | Thermal Transfer Mechanisms |
| **Confiança** | 0.95 |
| **Revisão Manual** | Não |
| **Erro LLM** | N/A |

**Abstract:**
> AbstractThe invention provides a system for energy distribution that uses liquid carbon dioxide as a working fluid. Evaporation of the carbon dioxide provides cooling, and compression of the carbon dioxide gas back to the liquid state provides heat. The amount of heat transferred at both stages is sufficient to provide environmental heating and cooling. Waste thermal energy from a power plant, in the form of hot water, is fed into the system and used to drive the overall process. An underground thermal energy storage system is used to store energy flowing into the system that is in excess of the current demand.

**Avaliação do LLM:**
Esta patente descreve um sistema para distribuição de energia que utiliza dióxido de carbono como fluido de trabalho, aproveitando a evaporação e compressão para transferência de calor. O sistema integra armazenamento subterrâneo de energia térmica para otimizar o uso de energia excedente, particularmente de fontes como usinas termelétricas.

**Extração Estruturada:**
- **Problema:** O problema abordado é a utilização de resíduos de energia térmica, como água quente de uma usina termelétrica, para fins de aquecimento e resfriamento de ambientes.
- **Solução:** A solução proposta é um sistema que utiliza dióxido de carbono como fluido de trabalho, convertendo calor em frio e vice-versa, e armazenando o excesso de energia em um sistema de armazenamento subterrâneo térmico.
- **Maturidade:** Inicial

**Achados-chave:**
- Utilização de dióxido de carbono como fluido de trabalho para transferência de energia térmica.
- Integração com um sistema de armazenamento subterrâneo de energia térmica para otimizar o uso de energia.
- Aproveitamento de resíduos de calor de uma usina termelétrica para impulsionar o processo de armazenamento e distribuição de energia.

**Vantagens alegadas:**
- Otimização do uso de resíduos de calor.
- Possibilidade de armazenamento de energia em larga escala.
- Eficiência na transferência de energia térmica.

**Limitações:**
- Dependência da disponibilidade de fontes de calor para alimentar o sistema.
- Custos associados à construção e operação do sistema de armazenamento subterrâneo.

**Aplicações potenciais:**
- Armazenamento de energia térmica em usinas termelétricas.
- Aquecimento e resfriamento de edifícios.
- Sistemas de energia renovável com armazenamento térmico.

**Evidências citadas:**
> AbstractThe invention provides a system for energy distribution that uses liquid carbon dioxide as a working fluid.
> An underground thermal energy storage system is used to store energy flowing into the system that is in excess of the current demand.

---

### 6. Liquid carbon dioxide energy storage system

| Campo | Valor |
|-------|-------|
| **Record ID** | `rec_efb86870a5fb` |
| **Family ID** | `family:4c114c45cbd4f573834db5ca6025ee6216f03b61` |
| **ID** | `CN117266954B` |
| **Inventores** | éå¹³æ´, äºæ³½, éä½³è±ª, å¼ å®¶ä¿, è¶äºå¯, æäºå, å³å² |
| **Titular** | Changsha Borui Dingneng Power Technology Co ltd |
| **Data** | 2024-06-07 |
| **Fonte** | Google Patents |
| **URL** | [CN117266954B](https://patents.google.com/patent/CN117266954B/en) |
| **Triagem** | include |
| **Rota** | deep_extraction |
| **Motivo da rota** | Há evidência suficiente para extração detalhada. |
| **Score de Triagem** | 9.2/10 |
| **Score de Relevância** | 9.2/10 |
| **Nível de Inovação** | Incremental |
| **Domínio Técnico** | Armazenamento de Energia Térmica |
| **Cluster Temático** | CO2 Phase Properties |
| **Confiança** | 0.95 |
| **Revisão Manual** | Não |
| **Erro LLM** | N/A |

**Abstract:**
> AbstractThe invention relates to the technical field of energy storage, in particular to a liquid carbon dioxide energy storage system, which comprises: a carbon dioxide storage unit including a low pressure storage module and a high pressure storage module; the energy storage unit is used for performing compression cooling and outputting a heat energy medium; the power generation unit is used for heating and expanding and outputting electric energy; the cold accumulation unit is used for storing cold energy media; a heat storage unit for storing a thermal energy medium; the cold accumulation liquefying unit is provided with a first area and a second area, the first area is provided with a phase change material and a first spiral coil, and the second area is provided with a single-phase working medium and a second spiral coil. The invention is beneficial to solving the large-scale long-time energy storage problem, has the advantages of high energy storage density, stable operation and the like, adopts the first spiral coil and the second spiral coil, realizes the separate absorption of the latent heat and the sensible heat of the carbon dioxide through the phase change material and the single-phase working medium, improves the cold storage liquefaction efficiency, reduces the occupied area, generates secondary flow, enhances the disturbance and improves the heat exchange effect.

**Avaliação do LLM:**
Esta patente descreve um sistema de armazenamento de energia de dióxido de carbono líquido que utiliza armazenamento de fase de mudança e um meio de trabalho único para absorver calor latente e sensível. O sistema integra módulos de armazenamento de alta e baixa pressão, unidades de geração e armazenamento de energia, e unidades de armazenamento de frio, otimizando a absorção de calor e a eficiência do armazenamento.

**Extração Estruturada:**
- **Problema:** O problema abordado é a necessidade de soluções de armazenamento de energia em larga escala e de longo prazo, com alta densidade de energia e operação estável.
- **Solução:** A solução proposta é um sistema de armazenamento de energia de dióxido de carbono líquido que utiliza um sistema de absorção de calor latente e sensível através de materiais de mudança de fase e um meio de trabalho único, permitindo a conversão de energia térmica em elétrica e vice-versa.
- **Maturidade:** Inicial

**Achados-chave:**
- O sistema utiliza um primeiro e um segundo conjunto de espirais para absorver o calor latente e sensível do dióxido de carbono, respectivamente.
- A utilização de um meio de trabalho único permite a separação do armazenamento de calor latente e sensível, melhorando a eficiência do armazenamento.

**Vantagens alegadas:**
- Alta densidade de armazenamento de energia
- Operação estável
- Melhoria da eficiência de armazenamento de frio

**Limitações:**
- A patente não detalha especificamente os materiais utilizados para os espirais ou o meio de trabalho único.
- A patente não aborda os desafios relacionados à manutenção e ao controle de temperatura do sistema.

**Aplicações potenciais:**
- Armazenamento de energia renovável (solar, eólica)
- Geração de energia de calor residual
- Refrigeração industrial

**Evidências citadas:**
> AbstractThe invention relates to the technical field of energy storage, in particular to a liquid carbon dioxide energy storage system...
> The invention is beneficial to solving the large-scale long-time energy storage problem, has the advantages of high energy storage density, stable operation and the like, adopts the first spiral coil and the second spiral coil, realizes the separate absorption of the latent heat and the sensible heat of the carbon dioxide through the phase change material and the single-phase working medium

---

### 7. Thermal energy transfer method using water and carbon dioxide

| Campo | Valor |
|-------|-------|
| **Record ID** | `rec_de31b088dc2d` |
| **Family ID** | `family:588784407a89e2f6beb518acaf221c766de7e6bf` |
| **ID** | `CN114930087A` |
| **Inventores** | FÂ·IÂ·çè¯ºå¹, MÂ·åºåå°¼, KÂ·éåå¸ |
| **Titular** | MED Energy Corp |
| **Data** | 2022-08-19 |
| **Fonte** | Google Patents |
| **URL** | [CN114930087A](https://patents.google.com/patent/CN114930087A/en) |
| **Triagem** | review |
| **Rota** | manual_review |
| **Motivo da rota** | Triagem indicou revisão humana. |
| **Score de Triagem** | 8.2/10 |
| **Score de Relevância** | 6.5/10 |
| **Nível de Inovação** | Significativa |
| **Domínio Técnico** | Armazenamento de Energia Térmica, Ciclo de Refrigeração |
| **Cluster Temático** | Armazenamento de Energia Térmica com Dióxido de Carbono |
| **Confiança** | 0.85 |
| **Revisão Manual** | Sim |
| **Erro LLM** | N/A |

**Abstract:**
> AbstractTranslated fromChineseæ¬åææä¾ä¸ç§ä½¿ç¨æ¶²ä½äºæ°§åç¢³ä½ä¸ºå·¥ä½æµä½çè½éåéç³»ç»ãä½¿æè¿°äºæ°§åç¢³è¸åæä¾éæ¸©ï¼å¹¶ä¸å°äºæ°§åç¢³æ°ä½åç¼©åå°æ¶²ææä¾ç­éãå¨ä¸¤ä¸ªé¶æ®µå¤è½¬ç§»çç­éçéè¶³ä»¥æä¾ç¯å¢åæ¸©åéæ¸©ãå°æ¥èªåçµåçåç­æ°´å½¢å¼çåºå¼ç­è½é¦éå°æè¿°ç³»ç»ä¸­å¹¶ä¸ä½¿ç¨æè¿°åºå¼ç­è½æ¥é©±å¨æ´ä¸ªè¿ç¨ãä½¿ç¨å°ä¸ç­è½å­å¨ç³»ç»æ¥å­å¨è¶åºå½åéæ±çæµå¨å°æè¿°ç³»ç»ä¸­çè½éãThe present invention provides an energy distribution system using liquid carbon dioxide as a working fluid. Evaporating the carbon dioxide provides cooling, and compressing the carbon dioxide gas back into a liquid state provides heat. The amount of heat transferred at both stages is sufficient to provide ambient warming and cooling. Waste thermal energy in the form of hot water from the power plant is fed into the system and used to drive the entire process. An underground thermal energy storage system is used to store energy flowing into the system in excess of current demand.

**Avaliação do LLM:**
Esta patente descreve um sistema de armazenamento de energia térmica que utiliza dióxido de carbono líquido, explorando a evaporação e compressão para armazenar calor. O sistema incorpora o uso de energia térmica residual de uma usina de energia, especificamente água quente, e um sistema de armazenamento subterrâneo de energia térmica. A patente se alinha diretamente com a busca 'carbon dioxide thermal energy storage'.

**Extração Estruturada:**
- **Problema:** O problema abordado é a necessidade de um método eficiente para armazenar e utilizar energia térmica residual, particularmente calor gerado por usinas de energia.
- **Solução:** A solução proposta é um sistema que utiliza dióxido de carbono líquido para absorver e liberar calor, aproveitando a evaporação e compressão do gás. A energia térmica residual da usina é utilizada para impulsionar o ciclo, e o calor armazenado é recuperado através da compressão do dióxido de carbono.
- **Maturidade:** Inicial

**Achados-chave:**
- O sistema utiliza dióxido de carbono líquido como fluido de trabalho, permitindo a transferência eficiente de calor através da evaporação e compressão.
- A patente detalha o uso de energia térmica residual de uma usina de energia (água quente) para alimentar o ciclo de armazenamento de energia térmica.

**Vantagens alegadas:**
- Utilização de energia térmica residual, reduzindo o desperdício.
- Armazenamento de energia térmica em escala, permitindo o uso posterior do calor.

**Limitações:**
- A eficiência do sistema depende da temperatura e da disponibilidade da energia térmica residual.
- A necessidade de um sistema de armazenamento subterrâneo para otimizar o armazenamento de energia.

**Aplicações potenciais:**
- Armazenamento de energia térmica em usinas de energia.
- Sistemas de aquecimento e resfriamento de edifícios.
- Armazenamento de energia renovável (solar, eólica).

**Evidências citadas:**
> Evaporating the carbon dioxide provides cooling, and compressing the carbon dioxide gas back into a liquid state provides heat.
> The amount of heat transferred at both stages is sufficient to provide ambient warming and cooling.

---

### 8. Carbon dioxide energy storage system and method using carbon dioxide as condensation working medium

| Campo | Valor |
|-------|-------|
| **Record ID** | `rec_908a19ff4be7` |
| **Family ID** | `family:810f7d32adfb88b6c1b92b87ba665f47d52c74c5` |
| **ID** | `CN117318319B` |
| **Inventores** | è°¢æ°¸æ§, çç§¦, é¦ç»æ¾, ç°èªè±ª, çé¼, åä»æ¡¢, å¼ è» |
| **Titular** | Baihe New Energy Technology Shenzhen Co ltd |
| **Data** | 2024-03-19 |
| **Fonte** | Google Patents |
| **URL** | [CN117318319B](https://patents.google.com/patent/CN117318319B/en) |
| **Triagem** | include |
| **Rota** | deep_extraction |
| **Motivo da rota** | Há evidência suficiente para extração detalhada. |
| **Score de Triagem** | 8.6/10 |
| **Score de Relevância** | 9.6/10 |
| **Nível de Inovação** | Significativa |
| **Domínio Técnico** | Armazenamento de Energia, Termodinâmica, Engenharia de Refrigeração |
| **Cluster Temático** | Thermal Transfer Mechanisms |
| **Confiança** | 0.88 |
| **Revisão Manual** | Não |
| **Erro LLM** | N/A |

**Abstract:**
> AbstractThe embodiment of the invention discloses a carbon dioxide energy storage system and a method using carbon dioxide as a condensing working medium, wherein the system comprises the following steps: the device comprises a gas storage, an energy storage assembly and a liquid storage tank; the energy storage component comprises a compression energy storage part, a condenser and a condensation working medium providing component, wherein the compression energy storage part is used for compressing gaseous carbon dioxide at normal pressure to a preset energy storage pressure and then dividing the gaseous carbon dioxide into two paths, one path is used as gaseous condensation working medium carbon dioxide to be input to the condensation working medium providing component, and the other path is used as gaseous working medium carbon dioxide to be input to the condenser; the condensing working medium supply component is used for boosting gaseous condensing working medium carbon dioxide to a supercritical state, reducing temperature and pressure to a gas-liquid mixed state, outputting the gas-liquid mixed state to the condenser, and the condenser is used for condensing the gaseous working medium carbon dioxide to a liquid state by utilizing the cold energy of the gas-liquid mixed state of the condensing working medium carbon dioxide and outputting the liquid state to the liquid storage tank. The embodiment of the invention can realize the utilization of the carbon dioxide in the system as the condensing working medium, so that a water chiller can be canceled, and the water consumption is greatly reduced.

**Avaliação do LLM:**
Esta patente descreve um sistema de armazenamento de energia que utiliza dióxido de carbono como meio de condensação, comprimindo e condensando o CO2 para armazenar energia térmica. O sistema elimina a necessidade de chillers de água, reduzindo significativamente o consumo de água. A inovação reside na utilização do CO2 como fluido de trabalho em um ciclo de armazenamento de energia térmica.

**Extração Estruturada:**
- **Problema:** O problema abordado é a necessidade de métodos de armazenamento de energia térmica eficientes e com baixo consumo de água, especialmente em aplicações que tradicionalmente utilizam chillers de água.
- **Solução:** A patente propõe um sistema que comprime CO2, o utiliza como fluido de trabalho em um ciclo de condensação e, em seguida, condensa o CO2 para armazenar energia térmica. O CO2 condensado é então reutilizado no ciclo, eliminando a necessidade de água.
- **Maturidade:** Intermediária

**Achados-chave:**
- O sistema utiliza um ciclo de compressão, condensação e recondensação de CO2.
- O CO2 é usado como fluido de trabalho, substituindo o uso de água em chillers convencionais.

**Vantagens alegadas:**
- Redução significativa no consumo de água.
- Eficiência aprimorada no armazenamento de energia térmica.

**Limitações:**
- A patente não detalha especificamente a eficiência do sistema em diferentes condições de temperatura e pressão.
- A viabilidade econômica do sistema pode depender do custo de compressão e refrigeração do CO2.

**Aplicações potenciais:**
- Construções sustentáveis
- Sistemas de refrigeração de alta eficiência
- Armazenamento de energia renovável

**Evidências citadas:**
> AbstractThe embodiment of the invention discloses a carbon dioxide energy storage system and a method using carbon dioxide as a condensing working medium

---

### 9. A dry ice energy storage system and method based on carbon dioxide gas-solid phase change

| Campo | Valor |
|-------|-------|
| **Record ID** | `rec_a75aca85cd3d` |
| **Family ID** | `family:3a5bffc06818f2e4d98aea16eca47962b4fbf382` |
| **ID** | `CN116164573B` |
| **Inventores** | æ¾åå |
| **Titular** | Jubian Technology Shenzhen Co ltd |
| **Data** | 2023-09-19 |
| **Fonte** | Google Patents |
| **URL** | [CN116164573B](https://patents.google.com/patent/CN116164573B/en) |
| **Triagem** | include |
| **Rota** | deep_extraction |
| **Motivo da rota** | Há evidência suficiente para extração detalhada. |
| **Score de Triagem** | 8.6/10 |
| **Score de Relevância** | 8.7/10 |
| **Nível de Inovação** | Incremental |
| **Domínio Técnico** | Armazenamento de Energia, Termodinâmica, Engenharia de Gases |
| **Cluster Temático** | CO2 Cycle Configurations |
| **Confiança** | 0.88 |
| **Revisão Manual** | Não |
| **Erro LLM** | N/A |

**Abstract:**
> AbstractThe invention discloses a dry ice energy storage system and a method based on carbon dioxide gas-solid phase transition, which relate to the technical field of compressed gas energy storage, wherein the system comprises: the system comprises an energy storage subsystem and an energy release subsystem, wherein the energy storage subsystem comprises a gas storage device, a compressor unit, a dry ice generator and a dry ice storage tank; the energy release subsystem comprises a dry ice sublimation reactor and an expansion unit; the gas storage device stores gaseous carbon dioxide, the gaseous carbon dioxide is conveyed from the gas storage device to the compressor unit for compression and power consumption, and solid carbon dioxide is generated through the dry ice generator and stored in the dry ice storage tank for energy storage; and solid carbon dioxide is conveyed to the dry ice sublimation reactor from the dry ice storage tank to absorb heat and sublimate to a fixed volume to form gaseous carbon dioxide again, and the gaseous carbon dioxide is conveyed to the expansion unit again, and is expanded by the expansion unit to perform work so as to release energy.

**Avaliação do LLM:**
Esta patente descreve um sistema e método para armazenamento de energia utilizando dióxido de carbono sólido (dry ice), explorando a mudança de fase térmica através da sublimação e expansão. O sistema incorpora um armazenamento de dióxido de carbono gasoso, um gerador de dióxido de carbono sólido e um reator de sublimação, permitindo a conversão de energia térmica em energia mecânica e vice-versa.

**Extração Estruturada:**
- **Problema:** O problema abordado é a necessidade de um sistema eficiente para o armazenamento de energia térmica, utilizando um fluido de trabalho com propriedades favoráveis e um ciclo de mudança de fase para maximizar a densidade de energia.
- **Solução:** A solução proposta é um sistema que utiliza a sublimação de dióxido de carbono sólido para armazenar energia térmica. O dióxido de carbono gasoso é comprimido e expandido, convertendo energia térmica em energia mecânica e vice-versa, permitindo o armazenamento e a liberação de energia de forma controlada.
- **Maturidade:** Inicial

**Achados-chave:**
- O sistema inclui um gas storage device, compressor unit, dry ice generator e dry ice storage tank.
- A sublimação de dióxido de carbono sólido é utilizada para absorver e liberar calor, permitindo o armazenamento e a recuperação de energia térmica.

**Vantagens alegadas:**
- Alta densidade de energia devido à mudança de fase térmica.
- Potencial para eficiência energética superior em comparação com métodos de armazenamento de energia convencionais.

**Limitações:**
- A eficiência do sistema pode ser afetada pela necessidade de refrigeração para manter o dióxido de carbono sólido.
- O custo de implementação do sistema pode ser elevado devido aos componentes especializados.

**Aplicações potenciais:**
- Armazenamento de energia em sistemas de aquecimento e resfriamento.
- Geração de energia em aplicações de cogeração.
- Armazenamento de energia em veículos elétricos (potencial).

**Evidências citadas:**
> The invention discloses a dry ice energy storage system and method based on carbon dioxide gas-solid phase change
> the system comprises an energy storage subsystem and an energy release subsystem, wherein the energy storage subsystem comprises a gas storage device, a compressor unit, a dry ice generator and a dry ice storage tank

---

### 10. The carbon dioxide capture and storage system by using heat pump and fuel cell

| Campo | Valor |
|-------|-------|
| **Record ID** | `rec_090110e4a3fb` |
| **Family ID** | `family:2a29f710b0bf8fa24c2097771b2a197edb7b4f8f` |
| **ID** | `KR20140023113A` |
| **Inventores** | í©ì°ì  |
| **Titular** | (ì£¼) ì¨íí¬ëë¡ì§ìì¤í |
| **Data** | 2014-02-26 |
| **Fonte** | Google Patents |
| **URL** | [KR20140023113A](https://patents.google.com/patent/KR20140023113A/en) |
| **Triagem** | review |
| **Rota** | manual_review |
| **Motivo da rota** | Triagem indicou revisão humana. |
| **Score de Triagem** | 7.7/10 |
| **Score de Relevância** | 6.5/10 |
| **Nível de Inovação** | Significativa |
| **Domínio Técnico** | Captura e Armazenamento de Carbono, Termodinâmica, Bomba de Calor, Células de Combustível |
| **Cluster Temático** | Utilização de calor recuperado para otimizar sistemas de captura e armazenamento de CO2, com foco em bombas de calor de absorção. |
| **Confiança** | 0.84 |
| **Revisão Manual** | Sim |
| **Erro LLM** | N/A |

**Abstract:**
> AbstractTranslated fromKoreanë³¸ ë°ëªììë ì°ë£ì ì§ì ë°°ì´(Exhaust Heat) ë° ì´íììì¤í(Heat Recovery System)ìì ë°ìíë ê³ ì¨ì ì´ìì ì´ì©íì¬ í¡ìì íí¸ííë¥¼ êµ¬ëìí´ì¼ë¡ì¨, í¡ìì íí¸ííì ì ì¨ì´ìì íìíì¬ ì´ì°ííì í¬ì§ ì ì¥ ìì¤íì ê²½ì ì±ì í¥ììí¬ ì ìë¤. í¡ìì íí¸ííìì ëì¨ ì´ìëì§ë¥¼ ì´ì©íì¬ ë§ëí ìëì§ê° íìí ì´ì°ííì í¬ì§ ì ì¥ ìì¤íì ì¬ìíì êµ¬ëìí´ì¼ë¡ì¨ íì í¬ì§ ì ì¥ ìì¤íì ì©ë ì¦ë ë° ê²½ì ì± í¥ìì íµí ì¡°ê¸° ì¤ì©íë¥¼ ë¬ì±í  ì ìë¤.ì´ë ê²í¨ì¼ë¡ì¨ íìì°ë£ì ì¬ì©ì¼ë¡ ì¸í´ ë°ì ì, ì² ê°, ìë©í¸, ì ì ë±ê³¼ ê°ì ì´ì°ííì ëë ë°°ì¶ììì ë°°ì¶ëë ì´ì°ííìë¥¼ í¬ì§íë ê¸°ì  ì ì©ì ìí ì§êµ¬ ì¨ëí ë¬¸ì  ë° ê¸°íë³í ë¬¸ì ë¥¼ í´ê²°í  ì ìë¤. ëí ê²½ì ì± ìë ì ì¬ììëì§ê° ê°ë°ë  ëê¹ì§ ì§ìë°ì ê°ë¥í íìì°ë£ë¥¼ ìì ì ì¼ë¡ ì¬ì©í  ì ìë íì í¬ì§ ì ì¥ ìì¤íì ê¸°ì  ì ì©ì´ ê°ë¥íê² ëë¤.In the present invention, by driving the absorption heat pump using a high temperature heat source generated from the exhaust heat and the heat recovery system of the fuel cell, the low-temperature heat source of the absorption heat pump is recovered to reduce the economic efficiency of the carbon dioxide collection and storage system. Can improve. By using the heat energy from the absorption heat pump to drive the regeneration tower of the carbon dioxide storage system, which requires a lot of energy, it is possible to achieve early practical use by increasing the capacity and economical efficiency of the carbon capture storage system.By doing so, the problem of global warming and climate change caused by the application of technology to capture carbon dioxide emitted from large-scale carbon dioxide sources such as power plants, steel, cement, refinery, etc. can be solved. In addition, it becomes possible to apply the technology of carbon capture storage system that can stably use sustainable fossil fuel until economic renewable energy is developed.

**Avaliação do LLM:**
Esta patente KR20140023113A descreve um sistema de captura e armazenamento de CO2 que utiliza uma bomba de calor e uma célula de combustível para otimizar o uso do calor recuperado. A patente foca na recuperação do calor do exaustão e do sistema de recuperação de calor da célula de combustível para alimentar uma bomba de calor de absorção, reduzindo a eficiência energética do sistema de armazenamento de CO2. O sistema visa melhorar a capacidade e a eficiência econômica do sistema de captura e armazenamento de CO2, particularmente em fontes de carbono de grande escala.

**Extração Estruturada:**
- **Problema:** O sistema de captura e armazenamento de CO2 tradicionalmente requer uma grande quantidade de energia para operar, especialmente para a regeneração da torre de absorção. A patente aborda a ineficiência energética associada a este processo.
- **Solução:** A solução proposta é utilizar o calor recuperado do exaustão e do sistema de recuperação de calor da célula de combustível para alimentar uma bomba de calor de absorção, que por sua vez alimenta a torre de regeneração da torre de absorção de CO2. Isso reduz a necessidade de energia externa e melhora a eficiência do sistema.
- **Maturidade:** Intermediária

**Achados-chave:**
- Utiliza o calor recuperado da exaustão e do sistema de recuperação de calor da célula de combustível para alimentar uma bomba de calor de absorção.
- A bomba de calor de absorção é usada para recuperar o calor da torre de regeneração da torre de absorção de CO2, reduzindo o consumo de energia.

**Vantagens alegadas:**
- Redução do consumo de energia no sistema de captura e armazenamento de CO2.
- Melhora da capacidade e da eficiência econômica do sistema de captura e armazenamento de CO2.
- Possibilidade de uso de combustíveis fósseis sustentáveis até que a energia renovável seja desenvolvida economicamente.

**Limitações:**
- A patente não detalha especificamente a escala ou o tipo de fonte de calor utilizada para alimentar a bomba de calor.
- A eficiência da bomba de calor de absorção pode ser influenciada por fatores como a temperatura do calor recuperado e o design da torre de absorção.

**Aplicações potenciais:**
- Captura e armazenamento de CO2 em usinas de energia, refinarias e outras instalações industriais.
- Redução das emissões de gases de efeito estufa.
- Utilização de combustíveis fósseis sustentáveis em aplicações de energia.

**Evidências citadas:**
> AbstractTranslated fromKoreanë³¸ ë°ëªììë ì°ë£ì ì§ì ë°°ì´(Exhaust Heat) ë° ì´íììì¤í(Heat Recovery System)ìì ë°ìíë ê³ ì¨ì ì´ìì ì´ì©íì¬ í¡ìì íí¸ííë¥¼ êµ¬ëìí´ì¼ë¡ì¨, í¡ìì íí¸ííì ì ì¨ì´ìì íìíì¬ ì´ì°ííì í¬ì§ ì ì¥ ìì¤íì ê²½ì ì±ì í¥ììí¬ ì ìë¤.
> By using the heat energy from the absorption heat pump to drive the regeneration tower of the carbon dioxide storage system, which requires a lot of energy, it is possible to achieve early practical use by increasing the capacity and economical efficiency of the carbon capture storage system.

---

### 11. 1. AU2019901965 - A System to Improve Performance of Transcritical Carbon Dioxide Cooling by Integration of Ice Thermal Storage for Subcooling

| Campo | Valor |
|-------|-------|
| **Record ID** | `rec_5cb75be738eb` |
| **Family ID** | `family:f2562110d58e9c2be7e7177585da03af0dd8bffa` |
| **ID** | `AU244427549` |
| **Inventores** | N/A |
| **Titular** | IceCap; Thermal; Energy; Pty Ltd; KALDORBULL PTY LTD |
| **Data** | 20.06.2019 |
| **Fonte** | Patentscope |
| **URL** | [AU244427549](https://patentscope.wipo.int/search/en/detail.jsf;jsessionid=2511917E8505F03BC8500F97357E5851.wapp2nC?docId=AU244427549&_cid=P22-MNMOEY-15419-1) |
| **Triagem** | review |
| **Rota** | manual_review |
| **Motivo da rota** | Triagem indicou revisão humana. |
| **Score de Triagem** | 7.2/10 |
| **Score de Relevância** | 6.5/10 |
| **Nível de Inovação** | Incremental |
| **Domínio Técnico** | Refrigeração, Armazenamento Térmico, Ciclo Transcíclico |
| **Cluster Temático** | Armazenamento Térmico de CO2 em Sistemas de Refrigeração |
| **Confiança** | 0.79 |
| **Revisão Manual** | Sim |
| **Erro LLM** | N/A |

**Avaliação do LLM:**
Esta patente descreve um sistema para melhorar o desempenho de sistemas de refrigeração transcíclica utilizando armazenamento térmico de gelo para sub-refrigeração do dióxido de carbono. A integração de gelo visa otimizar a eficiência do ciclo transcíclico, aproveitando o armazenamento de energia térmica do gelo. A patente explora a utilização de CO2 como fluido refrigerante em conjunto com armazenamento de gelo.

**Extração Estruturada:**
- **Problema:** O sistema de refrigeração transcíclica enfrenta desafios na manutenção da sub-refrigeração do CO2, impactando a eficiência do ciclo.
- **Solução:** A solução proposta é a integração de um armazenamento térmico de gelo para fornecer sub-refrigeração ao CO2, otimizando o ciclo transcíclico e potencialmente melhorando o desempenho do sistema de refrigeração.
- **Maturidade:** Inicial

**Achados-chave:**
- Utilização de gelo para sub-refrigeração do CO2 em sistemas transcíclicos.
- Integração de armazenamento térmico de gelo como componente chave para otimizar o ciclo transcíclico.

**Vantagens alegadas:**
- Melhora no desempenho do sistema de refrigeração transcíclica.
- Potencial aumento da eficiência energética.

**Limitações:**
- Dependência da disponibilidade e gestão do gelo para o armazenamento térmico.
- A eficácia pode variar dependendo das condições operacionais e do tamanho do sistema de armazenamento de gelo.

**Aplicações potenciais:**
- Sistemas de refrigeração transcíclica.
- Aplicações de refrigeração industrial e comercial.

**Evidências citadas:**
> AU2019901965 - A System to Improve Performance of Transcritical Carbon Dioxide Cooling by Integration of Ice Thermal Storage for Subcooling

---

### 12. 2. US20240229681 - Calcination system with thermal energy storage system

| Campo | Valor |
|-------|-------|
| **Record ID** | `rec_0d58733a5389` |
| **Family ID** | `family:a5909788b69b641216917fdfccb844df018cba89` |
| **ID** | `US433566429` |
| **Inventores** | John Setel O'Donnell, Peter Emery von Behrens, Chiaki Treynor, Matthieu Jonemann, Robert Ratz, Yusef Desjardins Ferhani |
| **Titular** | Rondo; Energy; , Inc. |
| **Data** | 11.07.2024 |
| **Fonte** | Patentscope |
| **URL** | [US433566429](https://patentscope.wipo.int/search/en/detail.jsf;jsessionid=2511917E8505F03BC8500F97357E5851.wapp2nC?docId=US433566429&_cid=P22-MNMOEY-15419-1) |
| **Triagem** | exclude |
| **Rota** | screen_only |
| **Motivo da rota** | Patente excluída na triagem. |
| **Score de Triagem** | 3.5/10 |
| **Score de Relevância** | 0.0/10 |
| **Nível de Inovação** | N/A |
| **Domínio Técnico** | Armazenamento de Energia Térmica, Engenharia Química |
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

### 13. 3. US20230203968 - Methods for material activation with thermal energy storage system

| Campo | Valor |
|-------|-------|
| **Record ID** | `rec_3da6b58fde67` |
| **Family ID** | `family:05206822f399c166b617cf99088b736afdf59e4b` |
| **ID** | `US400261922` |
| **Inventores** | John Setel O'Donnell, Peter Emery von Behrens, Chiaki Treynor, Jeremy Quentin Keller, Matthieu Jonemann, Robert Ratz, Yusef Desjardins Ferhani |
| **Titular** | Rondo; Energy; , Inc. |
| **Data** | 29.06.2023 |
| **Fonte** | Patentscope |
| **URL** | [US400261922](https://patentscope.wipo.int/search/en/detail.jsf;jsessionid=2511917E8505F03BC8500F97357E5851.wapp2nC?docId=US400261922&_cid=P22-MNMOEY-15419-1) |
| **Triagem** | exclude |
| **Rota** | screen_only |
| **Motivo da rota** | Patente excluída na triagem. |
| **Score de Triagem** | 3.5/10 |
| **Score de Relevância** | 0.0/10 |
| **Nível de Inovação** | N/A |
| **Domínio Técnico** | Armazenamento de Energia Térmica, Geração de Energia |
| **Cluster Temático** | Armazenamento de calor de fontes renováveis e aplicações de alta temperatura |
| **Confiança** | 0.79 |
| **Revisão Manual** | Não |
| **Erro LLM** | N/A |

**Abstract:**
> (EN)Anenergystoragesystem converts variable renewable electricity (VRE) to continuous heat at over 1000° C. Intermittent electricalenergyheats a solid medium. Heat from the solid medium is delivered continuously on demand. An array of bricks incorporating internal radiation cavities is directly heated bythermalradiation. The cavities facilitate rapid, uniform heating via reradiation. Heat delivery via flowing gas establishes a thermocline which maintains high outlet temperature throughout discharge. Gas flows through structured pathways within the array, delivering heat which may be used for processes including calcination, hydrogen electrolysis, steam generation, andthermalpower generation and cogeneration. Groups ofthermalstoragearrays may be controlled and operated at high temperatures withoutthermalrunaway via deep-discharge sequencing. Forecast-based control enables continuous, year-round heat supply using current and advance information of weather and VRE availability. High-voltage DC power conversion and distribution circuitry improves the efficiency of VRE power transfer into the system.

**Evidências citadas:**
> An energystoragesystem converts variable renewable electricity (VRE) to continuous heat at over 1000° C.
> Heat from the solid medium is delivered continuously on demand.

---

### 14. 4. US20240229682 - Methods for material activation with thermal energy storage system

| Campo | Valor |
|-------|-------|
| **Record ID** | `rec_d53841fc186a` |
| **Family ID** | `family:5759c6bc508072e5f9d303a96f846c77f3fcfe07` |
| **ID** | `US433566430` |
| **Inventores** | John Setel O'Donnell, Peter Emery von Behrens, Matthieu Jonemann, Yusef Desjardins Ferhani |
| **Titular** | Rondo; Energy; , Inc. |
| **Data** | 11.07.2024 |
| **Fonte** | Patentscope |
| **URL** | [US433566430](https://patentscope.wipo.int/search/en/detail.jsf;jsessionid=2511917E8505F03BC8500F97357E5851.wapp2nC?docId=US433566430&_cid=P22-MNMOEY-15419-1) |
| **Triagem** | exclude |
| **Rota** | screen_only |
| **Motivo da rota** | Patente excluída na triagem. |
| **Score de Triagem** | 3.5/10 |
| **Score de Relevância** | 0.0/10 |
| **Nível de Inovação** | N/A |
| **Domínio Técnico** | Armazenamento de Energia, Termodinâmica, Engenharia de Processos |
| **Cluster Temático** | Armazenamento de Energia Térmica com Fontes Renováveis |
| **Confiança** | 0.79 |
| **Revisão Manual** | Não |
| **Erro LLM** | N/A |

**Abstract:**
> (EN)Anenergystoragesystem converts variable renewable electricity (VRE) to continuous heat at over 1000° C. Intermittent electricalenergyheats a solid medium. Heat from the solid medium is delivered continuously on demand. An array of bricks incorporating internal radiation cavities is directly heated bythermalradiation. The cavities facilitate rapid, uniform heating via reradiation. Heat delivery via flowing gas establishes a thermocline which maintains high outlet temperature throughout discharge. Gas flows through structured pathways within the array, delivering heat which may be used for processes including calcination, hydrogen electrolysis, steam generation, andthermalpower generation and cogeneration. Groups ofthermalstoragearrays may be controlled and operated at high temperatures withoutthermalrunaway via deep-discharge sequencing. Forecast-based control enables continuous, year-round heat supply using current and advance information of weather and VRE availability. High-voltage DC power conversion and distribution circuitry improves the efficiency of VRE power transfer into the system.

**Evidências citadas:**
> Anenergystoragesystem converts variable renewable electricity (VRE) to continuous heat at over 1000° C.
> Heat from the solid medium is delivered continuously on demand.
> Heat delivery via flowing gas establishes a thermocline which maintains high outlet temperature throughout discharge.

---

### 15. 5. US20220282638 - Material activation system with thermal energy storage system

| Campo | Valor |
|-------|-------|
| **Record ID** | `rec_e94308d296fb` |
| **Family ID** | `family:edd5cd46beac8cd878fb34bf81f89eeab14f618e` |
| **ID** | `US373267798` |
| **Inventores** | John Setel O'Donnell, Peter Emery von Behrens, Chiaki Treynor, Jeremy Quentin Keller, Matthieu Jonemann, Robert Ratz, Yusef Desjardins Ferhani |
| **Titular** | Rondo; Energy; , Inc. |
| **Data** | 08.09.2022 |
| **Fonte** | Patentscope |
| **URL** | [US373267798](https://patentscope.wipo.int/search/en/detail.jsf;jsessionid=2511917E8505F03BC8500F97357E5851.wapp2nC?docId=US373267798&_cid=P22-MNMOEY-15419-1) |
| **Triagem** | exclude |
| **Rota** | screen_only |
| **Motivo da rota** | Patente excluída na triagem. |
| **Score de Triagem** | 3.5/10 |
| **Score de Relevância** | 0.0/10 |
| **Nível de Inovação** | N/A |
| **Domínio Técnico** | Armazenamento de Energia Térmica, Termodinâmica, Geração de Energia |
| **Cluster Temático** | Armazenamento de Energia em Meios Sólidos e Transferência de Calor |
| **Confiança** | 0.66 |
| **Revisão Manual** | Não |
| **Erro LLM** | N/A |

**Abstract:**
> (EN)Anenergystoragesystem converts variable renewable electricity (VRE) to continuous heat at over 1000° C. Intermittent electricalenergyheats a solid medium. Heat from the solid medium is delivered continuously on demand. An array of bricks incorporating internal radiation cavities is directly heated bythermalradiation. The cavities facilitate rapid, uniform heating via reradiation. Heat delivery via flowing gas establishes a thermocline which maintains high outlet temperature throughout discharge. Gas flows through structured pathways within the array, delivering heat which may be used for processes including calcination, hydrogen electrolysis, steam generation, andthermalpower generation and cogeneration. Groups ofthermalstoragearrays may be controlled and operated at high temperatures withoutthermalrunaway via deep-discharge sequencing. Forecast-based control enables continuous, year-round heat supply using current and advance information of weather and VRE availability. High-voltage DC power conversion and distribution circuitry improves the efficiency of VRE power transfer into the system.

**Evidências citadas:**
> An energystoragesystem converts variable renewable electricity (VRE) to continuous heat at over 1000° C.
> Heat from the solid medium is delivered continuously on demand.

---

### 16. 6. US20230243278 - Energy storage system and applications

| Campo | Valor |
|-------|-------|
| **Record ID** | `rec_03c5b1d3f782` |
| **Family ID** | `family:4cd4dbe1e17c542beed694e6d94568e60cc63440` |
| **ID** | `US403483831` |
| **Inventores** | John Setel O'Donnell, Peter Emery Von Behrens, Chiaki Treynor, Matthieu Jonemann, Robert Ratz, Yusef Desjardins Ferhani |
| **Titular** | Rondo; Energy; , Inc. |
| **Data** | 03.08.2023 |
| **Fonte** | Patentscope |
| **URL** | [US403483831](https://patentscope.wipo.int/search/en/detail.jsf;jsessionid=2511917E8505F03BC8500F97357E5851.wapp2nC?docId=US403483831&_cid=P22-MNMOEY-15419-1) |
| **Triagem** | exclude |
| **Rota** | screen_only |
| **Motivo da rota** | Patente excluída na triagem. |
| **Score de Triagem** | 3.5/10 |
| **Score de Relevância** | 0.0/10 |
| **Nível de Inovação** | N/A |
| **Domínio Técnico** | Armazenamento de Energia Térmica, Termodinâmica |
| **Cluster Temático** | Armazenamento de Energia Renovável com Calor |
| **Confiança** | 0.75 |
| **Revisão Manual** | Não |
| **Erro LLM** | N/A |

**Abstract:**
> (EN)Anenergystoragesystem converts variable renewable electricity (VRE) to continuous heat at over 1000° C. Intermittent electricalenergyheats a solid medium. Heat from the solid medium is delivered continuously on demand. An array of bricks incorporating internal radiation cavities is directly heated bythermalradiation. The cavities facilitate rapid, uniform heating via reradiation. Heat delivery via flowing gas establishes a thermocline which maintains high outlet temperature throughout discharge. Gas flows through structured pathways within the array, delivering heat which may be used for processes including calcination, hydrogen electrolysis, steam generation, andthermalpower generation and cogeneration. Groups ofthermalstoragearrays may be controlled and operated at high temperatures withoutthermalrunaway via deep-discharge sequencing. Forecast-based control enables continuous, year-round heat supply using current and advance information of weather and VRE availability. High-voltage DC power conversion and distribution circuitry improves the efficiency of VRE power transfer into the system.

**Evidências citadas:**
> An energystoragesystem converts variable renewable electricity (VRE) to continuous heat at over 1000° C.
> Heat from the solid medium is delivered continuously on demand. An array of bricks incorporating internal radiation cavities is directly heated by thermal radiation.

---

### 17. 7. US20220341349 - Solid oxide electrolysis system with thermal energy storage system

| Campo | Valor |
|-------|-------|
| **Record ID** | `rec_a0be2c132979` |
| **Family ID** | `family:7a32923049f7f0c024f142c370e853e015901c61` |
| **ID** | `US377255809` |
| **Inventores** | John Setel O'Donnell, Peter Emery von Behrens, Chiaki Treynor, Jeremy Quentin Keller, Matthieu Jonemann, Robert Ratz, Yusef Desjardins Ferhani |
| **Titular** | Rondo; Energy; , Inc. |
| **Data** | 27.10.2022 |
| **Fonte** | Patentscope |
| **URL** | [US377255809](https://patentscope.wipo.int/search/en/detail.jsf;jsessionid=2511917E8505F03BC8500F97357E5851.wapp2nC?docId=US377255809&_cid=P22-MNMOEY-15419-1) |
| **Triagem** | exclude |
| **Rota** | screen_only |
| **Motivo da rota** | Patente excluída na triagem. |
| **Score de Triagem** | 3.5/10 |
| **Score de Relevância** | 0.0/10 |
| **Nível de Inovação** | N/A |
| **Domínio Técnico** | Armazenamento de Energia, Eletroquímica, Engenharia Térmica |
| **Cluster Temático** | Armazenamento de Energia em Meio Sólido, Conversão de Energia Renovável |
| **Confiança** | 0.70 |
| **Revisão Manual** | Não |
| **Erro LLM** | N/A |

**Abstract:**
> (EN)Anenergystoragesystem converts variable renewable electricity (VRE) to continuous heat at over 1000° C. Intermittent electricalenergyheats a solid medium. Heat from the solid medium is delivered continuously on demand. An array of bricks incorporating internal radiation cavities is directly heated bythermalradiation. The cavities facilitate rapid, uniform heating via reradiation. Heat delivery via flowing gas establishes a thermocline which maintains high outlet temperature throughout discharge. Gas flows through structured pathways within the array, delivering heat which may be used for processes including calcination, hydrogen electrolysis, steam generation, andthermalpower generation and cogeneration. Groups ofthermalstoragearrays may be controlled and operated at high temperatures withoutthermalrunaway via deep-discharge sequencing. Forecast-based control enables continuous, year-round heat supply using current and advance information of weather and VRE availability. High-voltage DC power conversion and distribution circuitry improves the efficiency of VRE power transfer into the system.

**Evidências citadas:**
> An energystoragesystem converts variable renewable electricity (VRE) to continuous heat at over 1000° C.
> Heat from the solid medium is delivered continuously on demand.

---

### 18. 8. EP4509205 - ENERGY STORAGE SYSTEM AND APPLICATIONS

| Campo | Valor |
|-------|-------|
| **Record ID** | `rec_8c7a8466eb20` |
| **Family ID** | `family:74b492b60eb4176834516f685e60904730c0b046` |
| **ID** | `EP449228070` |
| **Inventores** | O'DONNELL JOHN SETEL, VON BEHRENS PETER EMERY, TREYNOR CHIAKI, KELLER JEREMY QUENTIN, JONEMANN MATTHIEU, RATZ ROBERT, FERHANI YUSEF DESJARDINS |
| **Titular** | RONDO; ENERGY; INC |
| **Data** | 19.02.2025 |
| **Fonte** | Patentscope |
| **URL** | [EP449228070](https://patentscope.wipo.int/search/en/detail.jsf;jsessionid=2511917E8505F03BC8500F97357E5851.wapp2nC?docId=EP449228070&_cid=P22-MNMOEY-15419-1) |
| **Triagem** | exclude |
| **Rota** | screen_only |
| **Motivo da rota** | Patente excluída na triagem. |
| **Score de Triagem** | 3.5/10 |
| **Score de Relevância** | 0.0/10 |
| **Nível de Inovação** | N/A |
| **Domínio Técnico** | Armazenamento de Energia Térmica, Termodinâmica |
| **Cluster Temático** | Armazenamento de Energia Renovável com Calor |
| **Confiança** | 0.63 |
| **Revisão Manual** | Não |
| **Erro LLM** | N/A |

**Abstract:**
> (EN)Anenergystoragesystem converts variable renewable electricity (VRE) to continuous heat at over 1000°C. Intermittent electricalenergyheats a solid medium Heat from the solid medium is delivered continuously on demand. An array of bricks incorporating internal radiation cavities is directly heated bythermalradiation. The cavities facilitate rapid, uniform heating via reradiation. Heat delivery via flowing gas establishes a thermocline which maintains high outlet temperature throughout discharge. Gas flows through structured pathways within the array, delivering heat which may be used for processes including calcination, hydrogen electrolysis, steam generation, andthermalpower generation and cogeneration. Groups ofthermalstoragearrays may be controlled and operated at high temperatures withoutthermalrunaway via deep-discharge sequencing. Forecast-based control enables continuous, year-round heat supply using current and advance information of weather and VRE availability. High-voltage DC power conversion and distribution circuitry improves the efficiency of VRE power transfer into the system.

**Evidências citadas:**
> An energystoragesystem converts variable renewable electricity (VRE) to continuous heat at over 1000°C.
> Heat from the solid medium is delivered continuously on demand.

---

### 19. 9. US20240218811 - Thermal energy storage system with deep discharge

| Campo | Valor |
|-------|-------|
| **Record ID** | `rec_706a46dd0158` |
| **Family ID** | `family:431c79fed9b723f85e4fa9485440c200bb5ba5b7` |
| **ID** | `US432849550` |
| **Inventores** | John Setel O'Donnell, Peter Emery von Behrens, Chiaki Treynor, Matthieu Jonemann, Robert Ratz |
| **Titular** | Rondo; Energy; , Inc. |
| **Data** | 04.07.2024 |
| **Fonte** | Patentscope |
| **URL** | [US432849550](https://patentscope.wipo.int/search/en/detail.jsf;jsessionid=2511917E8505F03BC8500F97357E5851.wapp2nC?docId=US432849550&_cid=P22-MNMOEY-15419-1) |
| **Triagem** | exclude |
| **Rota** | screen_only |
| **Motivo da rota** | Patente excluída na triagem. |
| **Score de Triagem** | 3.5/10 |
| **Score de Relevância** | 0.0/10 |
| **Nível de Inovação** | N/A |
| **Domínio Técnico** | Armazenamento de Energia Térmica, Geração de Energia |
| **Cluster Temático** | Armazenamento de Energia Renovável e Calor |
| **Confiança** | 0.79 |
| **Revisão Manual** | Não |
| **Erro LLM** | N/A |

**Abstract:**
> (EN)Anenergystoragesystem converts variable renewable electricity (VRE) to continuous heat at over 1000° C. Intermittent electricalenergyheats a solid medium. Heat from the solid medium is delivered continuously on demand. An array of bricks incorporating internal radiation cavities is directly heated bythermalradiation. The cavities facilitate rapid, uniform heating via reradiation. Heat delivery via flowing gas establishes a thermocline which maintains high outlet temperature throughout discharge. Gas flows through structured pathways within the array, delivering heat which may be used for processes including calcination, hydrogen electrolysis, steam generation, andthermalpower generation and cogeneration. Groups ofthermalstoragearrays may be controlled and operated at high temperatures withoutthermalrunaway via deep-discharge sequencing. Forecast-based control enables continuous, year-round heat supply using current and advance information of weather and VRE availability. High-voltage DC power conversion and distribution circuitry improves the efficiency of VRE power transfer into the system.

**Evidências citadas:**
> An energystoragesystem converts variable renewable electricity (VRE) to continuous heat at over 1000° C.
> Heat from the solid medium is delivered continuously on demand.

---

### 20. 10. US20220259988 - Thermal energy storage system with steam generation system including flow control and energy cogeneration

| Campo | Valor |
|-------|-------|
| **Record ID** | `rec_b021e183b191` |
| **Family ID** | `family:3e68d62068b4f6209c84fad2eefd3398a2f68ae0` |
| **ID** | `US371833683` |
| **Inventores** | John Setel O'Donnell, Peter Emery von Behrens, Chiaki Treynor, Jeremy Quentin Keller, Matthieu Jonemann, Robert Ratz, Yusef Desjardins Ferhani |
| **Titular** | Rondo; Energy; , Inc. |
| **Data** | 18.08.2022 |
| **Fonte** | Patentscope |
| **URL** | [US371833683](https://patentscope.wipo.int/search/en/detail.jsf;jsessionid=2511917E8505F03BC8500F97357E5851.wapp2nC?docId=US371833683&_cid=P22-MNMOEY-15419-1) |
| **Triagem** | exclude |
| **Rota** | screen_only |
| **Motivo da rota** | Patente excluída na triagem. |
| **Score de Triagem** | 3.5/10 |
| **Score de Relevância** | 0.0/10 |
| **Nível de Inovação** | N/A |
| **Domínio Técnico** | Armazenamento de Energia Térmica, Geração de Vapor, Cogeração |
| **Cluster Temático** | Armazenamento de Energia Renovável com Geração de Vapor |
| **Confiança** | 0.79 |
| **Revisão Manual** | Não |
| **Erro LLM** | N/A |

**Abstract:**
> (EN)Anenergystoragesystem converts variable renewable electricity (VRE) to continuous heat at over 1000° C. Intermittent electricalenergyheats a solid medium. Heat from the solid medium is delivered continuously on demand. An array of bricks incorporating internal radiation cavities is directly heated bythermalradiation. The cavities facilitate rapid, uniform heating via reradiation. Heat delivery via flowing gas establishes a thermocline which maintains high outlet temperature throughout discharge. Gas flows through structured pathways within the array, delivering heat which may be used for processes including calcination, hydrogen electrolysis, steam generation, andthermalpower generation and cogeneration. Groups ofthermalstoragearrays may be controlled and operated at high temperatures withoutthermalrunaway via deep-discharge sequencing. Forecast-based control enables continuous, year-round heat supply using current and advance information of weather and VRE availability. High-voltage DC power conversion and distribution circuitry improves the efficiency of VRE power transfer into the system.

**Evidências citadas:**
> An energystoragesystem converts variable renewable electricity (VRE) to continuous heat at over 1000° C.
> Heat from the solid medium is delivered continuously on demand. Gas flows through structured pathways within the array, delivering heat which may be used for processes including steam generation,...

---

## 🧾 Fila de Revisão Manual

- rec_de31b088dc2d (CN114930087A) | rota=manual_review | motivo=Triagem indicou revisão humana. | erro_llm=N/A
- rec_d32965bf3945 (US20200182095A1) | rota=manual_review | motivo=Triagem indicou revisão humana. | erro_llm=N/A
- rec_090110e4a3fb (KR20140023113A) | rota=manual_review | motivo=Triagem indicou revisão humana. | erro_llm=N/A
- rec_5cb75be738eb (AU244427549) | rota=manual_review | motivo=Triagem indicou revisão humana. | erro_llm=N/A

---

## 🔬 Análise Comparativa

### 1. Panorama Geral

- O conjunto incluído contém 7 patente(s) e não deve ser tratado como um bloco homogêneo; ele combina arquiteturas centradas em armazenamento explícito de CO2 com soluções mais adjacentes de transferência/distribuição térmica usando CO2 como fluido de trabalho [IDs: CN118934113A, CN117318319B, CN115234318A, CN117266954B, CN116164573B, US20230029186A1, WO2021081541A1]
- O subgrupo mais diretamente alinhado ao núcleo da query é CN118934113A, CN117318319B, CN115234318A, CN117266954B, com foco em armazenamento de CO2, compressão/expansão e controle termodinâmico do meio armazenado [IDs: CN118934113A, CN117318319B, CN115234318A, CN117266954B]
- CN115234318A, CN117266954B, US20230029186A1, WO2021081541A1 tratam CO2 principalmente como fluido de trabalho em transferência térmica ou distribuição de energia; nesses casos o armazenamento aparece como subsistema associado ou contexto operacional, não necessariamente como o núcleo arquitetural [IDs: CN115234318A, CN117266954B, US20230029186A1, WO2021081541A1]
- A menção a armazenamento subterrâneo ou subaquático aparece apenas em CN118934113A, US20230029186A1, WO2021081541A1 e não deve ser generalizada para todo o conjunto incluído [IDs: CN118934113A, US20230029186A1, WO2021081541A1]

## Análise Comparativa de Patentes: Armazenamento Térmico de Energia com Dióxido de Carbono

### 2. Tendências Identificadas

*   **Ciclos Termodinâmicos com CO2:** As patentes demonstram uma variedade de ciclos termodinâmicos utilizando CO2, incluindo expansão e compressão, evaporação e condensação, e a exploração da mudança de fase do dry ice [IDs: CN118934113A, CN115234318A, WO2021081541A1, US20230029186A1, CN117266954B, CN117318319B, CN116164573B].
*   **Integração com Usinas Termelétricas:**  Há um interesse crescente na integração de sistemas de armazenamento de energia com CO2 em usinas termelétricas, visando otimizar o uso da energia e reduzir picos de demanda [IDs: CN115234318A, US20230029186A1, CN117318319B].
*   **Armazenamento de Energia Térmica Subterrânea:** Várias patentes utilizam o armazenamento de energia térmica subterrânea como parte de seus sistemas de armazenamento de energia com CO2 [IDs: CN117266954B, CN116164573B, WO2021081541A1].
*   **Dry Ice como Meio de Armazenamento:** O uso de dry ice (dióxido de carbono sólido) como meio de armazenamento de energia térmica é uma tendência proeminente, explorando a mudança de fase para absorver e liberar calor [IDs: CN116164573B, CN117318319B].

### 3. Lacunas e Oportunidades

*   **Otimização de Ciclos Complexos:**  Ainda há espaço para otimizar ciclos termodinâmicos mais complexos que maximizem a eficiência do armazenamento de energia e a densidade de energia.  A pesquisa poderia se concentrar em ciclos que combinem diferentes fases do CO2 para melhorar o desempenho [IDs: CN118934113A, CN117266954B].
*   **Integração com Fontes Renováveis:** A integração de sistemas de armazenamento de energia com CO2 com fontes de energia renováveis (solar, eólica) ainda não é totalmente explorada.  O desenvolvimento de sistemas híbridos que combinem diferentes tecnologias de armazenamento de energia pode ser uma área de oportunidade [IDs: CN115234318A, WO2021081541A1].
*   **Controle e Monitoramento:**  Melhorar os sistemas de controle e monitoramento para otimizar o desempenho e a confiabilidade dos sistemas de armazenamento de energia com CO2 é uma área de oportunidade [IDs: Todas].
*   **Escalabilidade:** A escalabilidade de sistemas de armazenamento de energia com CO2, especialmente aqueles que utilizam dry ice, precisa ser melhorada para permitir a implementação em larga escala [IDs: CN116164573B, CN117318319B].

### 4. Recomendações

*   **Foco em Ciclos Híbridos:**  Investigar a combinação de diferentes ciclos termodinâmicos com CO2 para otimizar o desempenho em diferentes condições de operação.
*   **Análise de Custo-Benefício:**  Realizar análises de custo-benefício detalhadas para diferentes configurações de sistemas de armazenamento de energia com CO2, considerando fatores como custo de capital, custo operacional e desempenho.
*   **Desenvolvimento de Materiais:**  Pesquisar novos materiais para componentes de sistemas de armazenamento de energia com CO2, como materiais de alta eficiência para trocadores de calor e materiais resistentes à corrosão para o CO2.
*   **Simulação e Modelagem:** Utilizar simulação e modelagem computacional para otimizar o design de sistemas de armazenamento de energia com CO2 e prever seu desempenho em diferentes cenários.

### 5. Ranking Final

1. **CN118934113A** — armazenamento explícito de CO2 como núcleo da arquitetura; score 10.0/10 [IDs: CN118934113A]
2. **CN117318319B** — armazenamento explícito de CO2 como núcleo da arquitetura; score 9.6/10 [IDs: CN117318319B]
3. **CN115234318A** — armazenamento explícito de CO2 como núcleo da arquitetura; CO2 usado principalmente como fluido de trabalho para transferência térmica; score 9.4/10 [IDs: CN115234318A]
4. **CN117266954B** — armazenamento explícito de CO2 como núcleo da arquitetura; ênfase em refrigeração/sub-resfriamento, mais adjacente ao núcleo da query; score 9.2/10 [IDs: CN117266954B]
5. **CN116164573B** — alinhamento técnico sustentado pelas evidências extraídas; score 8.7/10 [IDs: CN116164573B]
6. **US20230029186A1** — CO2 usado principalmente como fluido de trabalho para transferência térmica; armazenamento subterrâneo aparece como subsistema de suporte; score 8.0/10 [IDs: US20230029186A1]
7. **WO2021081541A1** — CO2 usado principalmente como fluido de trabalho para transferência térmica; armazenamento subterrâneo aparece como subsistema de suporte; score 8.0/10 [IDs: WO2021081541A1]

### 6. Mapa de Evidências por ID

- **Thermal Transfer Mechanisms** [IDs: WO2021081541A1, US20230029186A1, CN117318319B]
- **CO2 Cycle Configurations** [IDs: CN118934113A, CN116164573B]
- **Armazenamento de Energia, Termodinâmica, Engenharia de Usinas Termelétricas** [IDs: CN115234318A]
- **CO2 Phase Properties** [IDs: CN117266954B]

### 7. Ranking por ID

1. **CN118934113A** — score 10.0/10 [IDs: CN118934113A]
2. **CN117318319B** — score 9.6/10 [IDs: CN117318319B]
3. **CN115234318A** — score 9.4/10 [IDs: CN115234318A]
4. **CN117266954B** — score 9.2/10 [IDs: CN117266954B]
5. **CN116164573B** — score 8.7/10 [IDs: CN116164573B]
6. **US20230029186A1** — score 8.0/10 [IDs: US20230029186A1]
7. **WO2021081541A1** — score 8.0/10 [IDs: WO2021081541A1]

---

## ℹ️ Informações do Sistema

- **Gerado por:** Agente de Web Scraping de Patentes
- **Modelo LLM:** gemma3:4b
- **Data de geração:** 06/04/2026 01:16:41
- **Query de busca:** `carbon dioxide thermal energy storage`
- **Status da execução:** completed
- **Tempo total:** 160.8s
- **LLM disponível:** sim
- **Fila de revisão manual:** 4 itens
- **Snapshot hash:** `1e9bbce50647badaf5205971699a7b171c582f6c937e445602e8f9093ec1aac4`
- **Features habilitadas:** require_evidence, enable_thematic_clusters, enable_prisma, enable_snapshot, enable_comparative_analysis, enable_manual_review_queue
- **Features desabilitadas:** nenhum
- **Versão do pipeline:** 1.1
- **Thresholds snapshot:** include=7.0, review=4.5
- **Cache LLM:** 0 hits, 32 misses, 32 entradas
- **Status do rascunho:** ready