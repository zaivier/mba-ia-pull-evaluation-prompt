.PHONY: setup pull push evaluate test metrics help

help:
	@echo "Comandos disponíveis:"
	@echo "  make setup    - Cria ambiente virtual com uv e instala dependências"
	@echo "  make pull     - Faz pull dos prompts do LangSmith Hub"
	@echo "  make push     - Faz push dos prompts otimizados para o LangSmith Hub"
	@echo "  make evaluate - Executa avaliação dos prompts"
	@echo "  make metrics  - Executa testes das métricas individualmente"
	@echo "  make test     - Executa testes de validação com pytest"

setup:
	uv venv .venv
	uv pip install -r requirements.txt

pull:
	uv run python src/pull_prompts.py

push:
	uv run python src/push_prompts.py

evaluate:
	uv run python src/evaluate.py

metrics:
	uv run python src/metrics.py

test:
	uv run pytest tests/test_prompts.py -v
