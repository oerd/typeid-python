# Main project-related automations
VENV	  ?= .venv
VENV_BIN  ?= $(VENV)/bin
RUFF	  ?= $(VENV_BIN)/ruff
PRECOMMIT ?= $(VENV_BIN)/pre-commit

BINARIES  := $(RUFF) $(PRECOMMIT)

usage:                    				## Show this help
	@grep -Fh "##" $(MAKEFILE_LIST) | grep -Fv fgrep | sed -e 's/:.*##\s*/##/g' | awk -F'##' '{ printf "%-25s %s\n", $$1, $$2 }'

sync: pyproject.toml
	uv sync --all-extras --dev --group=build

$(BINARIES): sync

init-precommit: $(PRECOMMIT)  $(TERRAFORM)				## Install git pre-commit hooks
	$(PRECOMMIT) install

precommit: init-precommit $(PRECOMMIT) $(TERRAFORM)		## Install pre-commit on all files
	$(PRECOMMIT) run --all-files

check-linting: precommit    ## Run lint checks (via pre-commit)
	$(PRECOMMIT) run --all-files

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
