# Revisao Tecnica de Patentes

Pipeline de scraping e revisao tecnica de patentes com triagem via Ollama, estado persistido e relatorios em Markdown/JSON.

## Ambiente

Use o Python do `venv` do projeto. O `python3` do sistema pode nao ter as dependencias instaladas.

```bash
venv/bin/python -m unittest tests.test_architecture
```

Para a suíte offline congelada:

```bash
venv/bin/python -m unittest tests.test_frozen_pipeline
```

## Ollama

O pipeline assume:

- servidor em `http://localhost:11434`
- modelo padrão `gemma3:27b` configurado em `config.py`

Exemplo de verificacao manual:

```bash
curl http://localhost:11434/api/tags
```

## Execucao

```bash
venv/bin/python main.py --query "carbon dioxide thermal energy storage" --max-results 5
```

## Comandos uteis

```bash
make test
make test-frozen
make benchmark-frozen
make smoke-ollama
make run QUERY="carbon dioxide thermal energy storage" MAX_RESULTS=5
```
