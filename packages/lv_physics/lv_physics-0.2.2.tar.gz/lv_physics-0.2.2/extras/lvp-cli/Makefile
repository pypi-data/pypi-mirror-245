.PHONY: activate-env build-env install install-pkg install-dev test clean reset

activate-env:=. env/bin/activate

build-env:
	python -m venv env
	$(call activate-env) && pip install --upgrade pip;
	echo "source env/bin/activate" > .activate # call `source .activate` to activate the env

install: install-pkg install-dev install-local

install-pkg:
	$(call activate-env) && pip install -r requirements.txt;
	$(call activate-env) && pip install -e .;

install-dev:
	$(call activate-env) && pip install -r requirements-dev.txt;

install-local:
	$(call activate-env) && pip install -r requirements-local.txt;

lint:
	$(call activate-env) && black --check lvp_cli/;
	$(call activate-env) && isort --check lvp_cli/;

lint-do:
	$(call activate-env) && black lvp_cli/;
	$(call activate-env) && isort lvp_cli/;

test:
	$(call activate-env) && pytest -vv -s tests;

clean:
	rm -rf env;
	find . -name "*.pyc" -exec rm -f {} \;
	find . -wholename "build" -exec rm -rf {} \;

reset: clean build-env install
