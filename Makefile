check-linting:
	uv run isort --check --profile black typeid/ tests/
	uv run flake8 --exit-zero typeid/ tests/ --exit-zero
	uv run black --check --diff typeid/ tests/ --line-length 119
	uv run mypy typeid/ --pretty


fix-linting:
	uv run isort --profile black typeid/ tests/
	uv run black typeid/ tests/ --line-length 119


artifacts: test
	python -m build


clean:
	rm -rf dist build *.egg-info


build:
	uv build


test:
	uv run pytest -v
