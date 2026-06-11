# Relatório Consolidado das Melhorias de 05/04/2026

## Escopo

- **Data de referência deste relatório:** 05/04/2026
- **Query de validação usada nos runs comparáveis:** `carbon dioxide thermal energy storage`
- **Run final auditado neste relatório:** `output/live_eval_round4/patentes_carbon_dioxide_thermal_energy_storage_20260405_001454.md`
- **Versão anterior de comparação principal:** modelo anterior às mudanças de 02/04/2026 em `output/modelo_antigo_relatorio.md`
- **Versão intermediária de comparação:** modelo já modificado em 02/04/2026 em `output/modelo_atual_relatorio.md`

## Resumo Executivo

O trabalho de 05/04/2026 teve quatro objetivos centrais:

1. estabilizar o uso do Ollama no pipeline;
2. tornar o estado do run e o relatório finais confiáveis;
3. endurecer a triagem para reduzir falso positivo técnico;
4. obrigar a análise comparativa a se apoiar em evidência rastreável por ID.

O resultado final melhorou de forma material em relação ao modelo de 02/04/2026 e, mais ainda, em relação ao modelo anterior a 02/04/2026. O sistema agora:

- roda de ponta a ponta com `gemma3:4b` local sem falha de LLM;
- expõe telemetria operacional por etapa;
- diferencia `include`, `review` e `exclude` com muito mais rigor;
- não marca mais relatório final com metadado stale;
- gera análise comparativa completa, sem fallback, com seções finais completas e suporte por ID.

Mesmo assim, o modelo ainda **não está 100% coeso do ponto de vista analítico**. O pipeline está coeso operacionalmente, mas o texto comparativo ainda apresenta pelo menos duas fragilidades:

- supergeneraliza uma característica de “armazenamento subterrâneo” para o conjunto incluído;
- a seção livre de ranking final repete `CN118934113A` duas vezes, embora o apêndice determinístico por ID esteja correto.

Conclusão objetiva: o modelo atual está **coeso para operação assistida e revisão técnica supervisionada**, mas **ainda não está no ponto ideal para aceitar a síntese comparativa como verdade final sem leitura humana**.

## O Que Foi Feito Hoje e Por Que

### 1. Endurecimento do Ollama

Foi feito porque a integração local estava operacional para chamadas simples, mas falhava na análise comparativa em texto e ainda reportava alguns estados de forma enganosa.

Principais mudanças:

- remoção do caminho que enviava `format="text"` ao Ollama e provocava `HTTP 500` na comparativa textual;
- retry com geração reduzida para respostas textuais;
- healthcheck real com correspondência exata de modelo, não apenas match por prefixo;
- telemetria por operação (`healthcheck`, `screening`, `evaluation`, `comparative`);
- circuit breaker e modo degradado para evitar que falha de infraestrutura fosse confundida com exclusão técnica;
- correção da chave de cache e da contagem de `misses`.

Motivo técnico:

- o modelo precisava parar de transformar instabilidade do backend em decisão metodológica;
- a observabilidade do LLM precisava deixar de ser implícita;
- a comparativa precisava sair do estado de fallback silencioso.

### 2. Verdade do Estado do Pipeline e do Relatório

Foi feito porque o relatório de 02/04/2026 ainda podia sair com `status=running` e `tempo total=0.0s`, mesmo depois do run terminar, o que tornava a evidência operacional pouco confiável.

Principais mudanças:

- regravação do relatório após a finalização do estado;
- revisão da lógica que marcava etapas como `ok` mesmo quando o conteúdo era fallback;
- padronização da fila de revisão manual com `record_id`, motivo e erro associado.

Motivo técnico:

- em revisão técnica, metadado incorreto invalida a confiança no artefato, mesmo quando o corpo do texto parece bom.

### 3. Identidade e Casamento Interno de Registros

Foi feito porque o pipeline dependia demais de `patent_id`, o que é frágil quando o ID vem faltando, duplicado ou com ruído de scraping.

Principais mudanças:

- criação de `record_id` interno estável;
- dedupe e rastreabilidade aprimorados;
- contrato explícito para a fila de revisão manual.

Motivo técnico:

- evitar casar avaliação errada com patente errada;
- tornar o estado do run auditável e estável.

### 4. Diagnóstico dos Scrapers

Foi feito porque a coleta ainda gerava falso positivo de bloqueio e tinha fallback mal comunicado.

Principais mudanças:

- separação entre `blocked_or_captcha`, `layout_break` e `discovery_empty`;
- remoção de sinal fraco que gerava falso positivo;
- clareza maior no fallback do Patentscope e do Google Patents.

Motivo técnico:

- “zero resultados” e “fonte bloqueou” são diagnósticos muito diferentes e não podem ser tratados como a mesma coisa.

### 5. Benchmark, Testes e Reprodutibilidade

Foi feito porque o projeto estava forte em experimento manual, mas ainda pouco protegido contra regressão real.

Principais mudanças:

- benchmark congelado;
- testes adicionais para triagem, comparativa, block detection, relatório e pipeline congelado;
- CI;
- `README.md` e `Makefile`.

Motivo técnico:

- reduzir regressão silenciosa;
- permitir reproduzir o comportamento do pipeline sem depender de run vivo toda vez.

### 6. Endurecimento da Triagem e Abertura da Escala de Score

Foi feito porque as rodadas anteriores ainda aceitavam patentes genericamente ligadas a armazenamento térmico, mesmo sem aderência distintiva à query com `CO2`.

Principais mudanças:

- guardrails de alinhamento com a query;
- exigência de aderência distintiva para `include`;
- recalibração dos scores de relevância para abrir mais a escala;
- análise comparativa limitada ao conjunto realmente incluído.

Motivo técnico:

- reduzir falso positivo de patente apenas tangencial;
- melhorar a utilidade do ranking final.

### 7. Comparativa Forçada por Evidência

Foi feito porque a análise comparativa ainda conseguia soar convincente mesmo quando estava incompleta, genérica ou sem ancoragem explícita em IDs.

Principais mudanças:

- prompt comparativo exigindo referência explícita aos IDs;
- mapa de evidências por ID;
- ranking por ID;
- seções finais determinísticas para completar a estrutura quando o modelo truncar ou encerrar cedo.

Motivo técnico:

- tornar a comparativa mais auditável;
- reduzir alucinação estrutural;
- evitar que uma síntese bonita esconda pouca sustentação factual.

### 8. Atualização complementar desta sessão: comparativa determinística e logger estruturado ponta a ponta

Depois do fechamento do run auditado acima, foi feito um complemento estrutural adicional no código para atacar exatamente as fragilidades remanescentes identificadas no `round4` e para fechar a recomendação que ainda estava pendente sobre logging estruturado.

Principais mudanças:

- reescrita determinística do `Panorama Geral` e do `Ranking Final` da comparativa, em vez de confiar nesses trechos livres do LLM;
- remoção do risco de ranking livre inconsistente ou duplicado quando o modelo textual devolver ordenação ruim;
- regra explícita para não generalizar características como `armazenamento subterrâneo` para todo o conjunto quando a evidência sustenta apenas um subconjunto;
- inclusão de `observability_metrics` estruturadas por rota, por fonte e por tipo de falha no estado e no relatório;
- adoção de logger estruturado em JSON em `main.py`, `pipeline/orchestrator.py`, `evaluator/llm_evaluator.py`, `report/generator.py`, `scraper/google_patents.py` e `scraper/patentscope.py`;
- extensão do mesmo padrão para os scrapers, fechando o gap entre diagnóstico de coleta e emissão operacional de logs;
- testes adicionais cobrindo formatter estruturado, ranking comparativo determinístico, escopo correto de alegações comparativas e integridade do pipeline congelado.

Motivo técnico:

- transformar observabilidade em contrato explícito, não em texto solto de console;
- reduzir a dependência do trecho livre gerado pelo LLM exatamente onde a síntese era mais frágil;
- preparar o pipeline para auditoria e automação sem perder granularidade operacional;
- fechar uma recomendação que ainda estava em aberto no projeto.

Importante:

- essas mudanças **já estão implementadas no código**;
- elas **ainda não substituem o diagnóstico do run `round4` acima**, porque esse artefato auditado foi gerado antes desta sessão complementar;
- portanto, o efeito delas sobre o relatório final em produção ainda precisa ser confirmado por **novo run comparável**.

## Sequência dos Runs de 05/04/2026

| Run | Arquivo | Resultado principal | Leitura |
| --- | --- | --- | --- |
| `round2` | `output/live_eval_round2/patentes_carbon_dioxide_thermal_energy_storage_20260405_000140.md` | `3 include / 3 review / 4 exclude`, média `9.2`, sem falha de LLM | Corrigiu metadado stale e falso bloqueio, mas ainda achata score e exagera na comparativa |
| `round3` | `output/live_eval_round3/patentes_carbon_dioxide_thermal_energy_storage_20260405_001006.md` | `4 include / 2 review / 4 exclude`, média `8.85`, comparativa com apêndice de IDs | Abriu parte da escala, mas ainda havia fechamento incompleto de seções e resultado menos conservador |
| `round4` | `output/live_eval_round4/patentes_carbon_dioxide_thermal_energy_storage_20260405_001454.md` | `3 include / 3 review / 4 exclude`, média `8.67`, comparativa completa com IDs | Melhor equilíbrio entre rigor de triagem, estabilidade do Ollama e completude do relatório |

## Output do Run Final de 05/04/2026

Trecho do terminal:

```text
Patentes encontradas: 10
Triadas: 10
Incluídas: 3
Revisão manual: 3
Score médio de relevância: 8.7/10

Top 3 Patentes mais relevantes:
1. [10.0] CN118934113A
2. [8.0] WO2021081541A1
3. [8.0] US20210123608A1

Tempo total: 86.9s
```

Resultado final da triagem:

- **Incluídas:** `CN118934113A`, `WO2021081541A1`, `US20210123608A1`
- **Revisão manual:** `US20200182095A1`, `CN115234318A`, `AU244427549`
- **Excluídas:** `US433566429`, `US400261922`, `US433566430`, `US373267798`

Leitura técnica do conjunto:

- os quatro registros da Rondo foram corretamente excluídos como armazenamento térmico genérico sem aderência distintiva à query;
- as patentes diretamente orientadas a `CO2` mas ainda ambíguas do ponto de vista metodológico foram deslocadas para `review`;
- o conjunto incluído ficou muito mais defensável do que nas versões anteriores.

## Comparação com o Modelo Anterior a 02/04/2026 e com o Modelo de 02/04/2026

### Tabela Comparativa

| Dimensão | Antes de 02/04/2026 | Modelo de 02/04/2026 | Modelo atual de 05/04/2026 |
| --- | --- | --- | --- |
| Patentes no conjunto | `10` | `10` | `10` |
| Regime de triagem | inexistente | `8 include / 1 review / 1 exclude` | `3 include / 3 review / 4 exclude` |
| Score de relevância | todas as `10` com `9.0` | ainda concentrado em `9.0-10.0` para muitos casos fracos | incluídos em `10.0`, `8.0`, `8.0`; reviews em `6.5`; excluídos em `0.0` |
| Comparativa | longa, mas sem rastreabilidade operacional | fallback: `⚠️ Não foi possível gerar a análise comparativa.` | completa, sem fallback, com seções `1-7` e suporte por ID |
| Estado do run | não havia estado estruturado confiável | `status=running`, `tempo=0.0s` no artefato salvo | `status=completed`, `tempo=86.9s` |
| Telemetria do LLM | inexistente | inexistente | presente por operação |
| Diagnóstico de scraping | muito limitado | ainda com ruído | `Nenhum sinal relevante detectado` no Google e `discovery_empty` explícito no fallback do Patentscope |
| Fila de revisão manual | inexistente | presente, mas ainda simples | estruturada com `record_id`, motivo e erro |

### Exemplos Qualitativos

#### Antes de 02/04/2026

O modelo antigo era o menos confiável metodologicamente. Ele não tinha triagem real e tratava praticamente tudo como relevante. Exemplos claros do ruído incluído no conjunto:

- `WO2024040002A1` sobre `CO2 thermal swing adsorption`;
- `US10458681B1` sobre integração térmica de queimador catalítico e unidade de remoção de CO2;
- `WO2020204933A1` sobre `thermocline thermal energy storage in multiple tanks`;
- itens da Rondo sobre calcinação e ativação de materiais com armazenamento térmico.

Em termos práticos, a pergunta de busca e o corpus retornado ainda estavam semanticamente desalinhados.

#### Modelo de 02/04/2026

O modelo de 02/04/2026 já tinha avanço estrutural importante, mas ainda errava feio na filtragem. Foram incluídos casos como:

- `CN214660665U` de sistema fotovoltaico com armazenamento eletrotérmico;
- `US20240339953A1` de acoplamento multienergia;
- `KR101978330B1` de sistema de suprimento de combustível para célula a combustível;
- todos os itens da Rondo com armazenamento térmico genérico.

Além disso:

- a análise comparativa falhava e virava fallback;
- o artefato final podia sair como se o run ainda estivesse em execução;
- não havia telemetria suficiente do LLM para diferenciar falha operacional de falha metodológica.

#### Modelo Atual de 05/04/2026

O modelo atual é muito mais seletivo e muito mais honesto sobre incerteza:

- só três patentes ficaram em `include`;
- três itens tecnicamente próximos, mas ainda ambíguos, foram jogados para `review`;
- os quatro casos genericamente térmicos foram excluídos.

Esse comportamento é significativamente melhor para uma revisão técnica séria, porque o pipeline deixou de converter “parecido com o tema” em “claramente aderente ao tema”.

## Seção Específica Sobre o Ollama

### Problemas Que Existiam

Antes das correções de 05/04/2026, o uso do Ollama tinha quatro fragilidades centrais:

- a comparativa textual podia falhar com `HTTP 500`;
- o pipeline podia marcar a etapa como `ok` mesmo entregando apenas fallback;
- a contagem de cache estava incorreta;
- não existia telemetria suficiente para saber onde exatamente o backend estava degradando.

### O Que Mudou

- a checagem de conexão passou a exigir o modelo exato e a testar geração real;
- a trilha de texto livre foi endurecida com retry e redução de geração;
- o estado do LLM agora é refletido no relatório final;
- falha de infraestrutura não vira mais exclusão silenciosa;
- a comparativa ganhou pós-processamento determinístico para completar estrutura e anexar evidência por ID.

### Comportamento do Ollama no Run Final de 05/04/2026

`gemma3:4b` local em `http://localhost:11434`

| Operação | Chamadas | Falhas | Média por chamada | Tempo total | Prompt chars | Response chars |
| --- | --- | --- | --- | --- | --- | --- |
| `healthcheck` | `1` | `0` | `0.326s` | `0.326s` | `35` | `15` |
| `screening` | `10` | `0` | `1.331s` | `13.305s` | `26340` | `8854` |
| `evaluation` | `6` | `0` | `3.175s` | `19.047s` | `20514` | `14844` |
| `comparative` | `1` | `0` | `6.498s` | `6.498s` | `3707` | `4210` |

Síntese:

- `degraded=false`
- `total_failures=0`
- nenhuma etapa do run final falhou por indisponibilidade do Ollama

Isso mostra que, no estado atual, o Ollama deixou de ser o gargalo operacional principal do pipeline. O gargalo remanescente agora é mais metodológico do que infraestrutural.

## O Modelo Está Coeso?

### Coesão Operacional

**Sim.**

O pipeline atual está coeso operacionalmente porque:

- executa setup, scraping, triagem, extração, comparativa e relatório até o fim;
- salva estado final consistente;
- reporta duração real;
- não mascara falha de LLM;
- produz comparativa sem fallback;
- expõe telemetria suficiente para auditoria.

### Coesão Metodológica

**Parcialmente.**

Ele melhorou muito, mas ainda não está totalmente coeso do ponto de vista analítico. Os principais sinais disso no run final são:

1. a comparativa afirma integração com armazenamento subterrâneo para as três patentes incluídas, o que é mais forte do que a evidência sustenta;
2. a seção livre `### 5. Ranking Final` repete `CN118934113A` como item `1` e item `3`, embora a seção determinística `### 7. Ranking por ID` esteja correta;
3. a escala abriu mais na relevância final, mas a triagem dos incluídos ainda continua comprimida em `9.2`.

Observação complementar desta sessão:

- os itens `1` e `2` acima foram atacados diretamente no código após este run auditado, com pós-processamento determinístico da comparativa e escopo explícito por subconjunto;
- como ainda não houve novo `live_eval` comparável depois desse patch, eles continuam valendo como diagnóstico do artefato `round4`, mas não mais como descrição do estado atual do código.

Portanto, o modelo atual está:

- **coeso o suficiente para operar como assistente de revisão técnica**;
- **ainda não coeso o suficiente para dispensar leitura crítica humana da síntese comparativa**.

## Está Como o Esperado?

### O Que Está Dentro do Esperado

- estabilidade do Ollama local com `gemma3:4b`;
- exclusão dos casos genericamente térmicos;
- deslocamento de casos ambíguos para `review`;
- relatório final consistente;
- comparativa completa com IDs.

### O Que Ainda Está Abaixo do Esperado

- validação em novo run comparável do pós-processamento determinístico da comparativa;
- comprovação em artefato real da nova camada de logger estruturado ponta a ponta;
- maior diversidade de score na triagem dos incluídos.

## Conclusão Final

Comparado ao modelo anterior a 02/04/2026, o pipeline atual ficou claramente melhor em quatro eixos:

- seletividade;
- rastreabilidade;
- estabilidade do Ollama;
- confiabilidade do artefato final.

Comparado ao modelo de 02/04/2026, a melhora principal foi transformar um pipeline que já era mais estruturado, porém ainda frouxo e parcialmente enganoso, em um pipeline mais rígido, auditável e operacionalmente honesto.

Depois da sessão complementar registrada neste mesmo relatório, o código também passou a ter:

- comparativa com partes críticas determinísticas;
- observabilidade estruturada por rota, fonte e falha;
- logger estruturado de ponta a ponta, incluindo scrapers.

Esses ganhos já valem para o estado do código, mas ainda precisam ser confirmados em um novo artefato `live_eval` comparável para substituir formalmente o diagnóstico do `round4`.

Veredito final:

- **Operacionalmente no código atual:** sim, o modelo está coeso e mais observável do que na versão auditada originalmente.
- **Metodologicamente no último artefato auditado:** melhorou bastante, mas ainda não estava totalmente coeso.
- **Próximo passo obrigatório para fechar o ciclo:** gerar um novo `live_eval` comparável pós-patch.
- **Uso recomendado agora:** revisão técnica assistida, com validação humana da análise comparativa final até esse novo run ser auditado.

## Artefatos Referenciados

- `output/modelo_antigo_relatorio.md`
- `output/modelo_antigo_relatorio.json`
- `output/modelo_atual_relatorio.md`
- `output/modelo_atual_relatorio.json`
- `output/live_eval_round2/patentes_carbon_dioxide_thermal_energy_storage_20260405_000140.md`
- `output/live_eval_round3/patentes_carbon_dioxide_thermal_energy_storage_20260405_001006.md`
- `output/live_eval_round4/patentes_carbon_dioxide_thermal_energy_storage_20260405_001454.md`
- `output/live_eval_round4/patentes_carbon_dioxide_thermal_energy_storage_20260405_001454.json`
- `output/live_eval_round4/run_state_latest.json`
