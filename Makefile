PYTHON ?= venv/bin/python
QUERY ?= carbon dioxide thermal energy storage
MAX_RESULTS ?= 5
OLLAMA_MODEL ?= gemma3:27b

.PHONY: test test-frozen benchmark-frozen smoke-ollama run ci \
        docker-build docker-up docker-down docker-pull-model docker-test docker-logs

test:
	$(PYTHON) -m unittest tests.test_architecture tests.test_frozen_pipeline

test-frozen:
	$(PYTHON) -m unittest tests.test_frozen_pipeline

benchmark-frozen:
	$(PYTHON) main.py --ablation --query "$(QUERY)" --max-results $(MAX_RESULTS) --benchmark-file benchmarks/frozen_ablation_benchmark.json

smoke-ollama:
	$(PYTHON) -c "from evaluator.llm_evaluator import OllamaEvaluator; ev = OllamaEvaluator(); print('check_connection=', ev.check_connection())"

run:
	$(PYTHON) main.py --query "$(QUERY)" --max-results $(MAX_RESULTS)

ci: test

docker-build:
	docker compose build

docker-up:
	docker compose up -d

docker-down:
	docker compose down

docker-pull-model:
	docker compose exec ollama ollama pull $(OLLAMA_MODEL)

docker-test:
	docker compose run --rm --entrypoint python app \
	  -m unittest tests.test_architecture tests.test_frozen_pipeline

docker-logs:
	docker compose logs -f app
