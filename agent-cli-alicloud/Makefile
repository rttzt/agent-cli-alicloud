.PHONY: verify test lint typecheck

verify: test lint typecheck

test:
	uv run pytest

lint:
	uv run ruff check

typecheck:
	uv run mypy src/agent_cli_alicloud/
