# Relatório de Whitespace

**Data:** 06/04/2026
**Escopo auditado:** código-fonte, testes, docs e benchmarks do repositório
**Escopo excluído:** `venv/`, `output/`, `.git/`, `__pycache__/`, arquivos binários

## Resumo

- **44** linhas com trailing whitespace
- **42** dessas linhas são linhas vazias contendo apenas espaços
- **2** linhas têm trailing whitespace em linha com código
- **5** ocorrências de tab
- **0** ocorrências de whitespace Unicode suspeito (`NBSP`, `ZWSP`, `ZWNJ`, `ZWJ`, `BOM`)
- **0** arquivos sem newline final

## Classificação

### 1. Trailing whitespace em linhas vazias

- [scraper/google_patents.py](/home/murilo/Documentos/RevisaoTecnica/scraper/google_patents.py): linhas `53, 139, 177, 204, 209, 221, 234, 310, 327, 334, 347, 365, 380, 394`
- [scraper/patentscope.py](/home/murilo/Documentos/RevisaoTecnica/scraper/patentscope.py): linhas `129, 169, 195, 201, 218, 228, 231, 234, 248, 256, 261, 274, 283, 288, 292, 357, 367, 373, 380`
- [Arquitetura.md](/home/murilo/Documentos/RevisaoTecnica/Arquitetura.md): linhas `15, 20, 23, 26, 28, 32, 40`
- [test_gp_json.py](/home/murilo/Documentos/RevisaoTecnica/test_gp_json.py): linhas `10, 18`

### 2. Trailing whitespace em linhas com código

- [scraper/patentscope.py](/home/murilo/Documentos/RevisaoTecnica/scraper/patentscope.py#L351): espaço ao final da linha após o operador `and`
- [scraper/patentscope.py](/home/murilo/Documentos/RevisaoTecnica/scraper/patentscope.py#L355): espaço ao final da linha após o operador `and`

Trechos observados:

```python
label_el = soup.find(lambda tag: tag.name in ["span", "div", "b", "label"] and 
label_el = soup.find(lambda tag: tag.name in ["span", "div", "b", "label"] and 
```

### 3. Tabs encontrados

- [Makefile](/home/murilo/Documentos/RevisaoTecnica/Makefile#L8)
- [Makefile](/home/murilo/Documentos/RevisaoTecnica/Makefile#L11)
- [Makefile](/home/murilo/Documentos/RevisaoTecnica/Makefile#L14)
- [Makefile](/home/murilo/Documentos/RevisaoTecnica/Makefile#L17)
- [Makefile](/home/murilo/Documentos/RevisaoTecnica/Makefile#L20)

Observação: esses tabs são **esperados** em receitas de `Makefile`; não configuram defeito de formatação.

## Conclusão

O repositório não apresenta problema estrutural amplo de whitespace. O que existe é majoritariamente ruído de edição em linhas vazias, concentrado em `scraper/google_patents.py`, `scraper/patentscope.py`, `Arquitetura.md` e `test_gp_json.py`. Os únicos casos materialmente relevantes são dois trailing spaces em linhas de código de `scraper/patentscope.py`.
