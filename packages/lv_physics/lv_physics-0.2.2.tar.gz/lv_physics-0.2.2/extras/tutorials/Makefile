.PHONY: build-env install pdf clean reset

activate-env := . env/bin/activate

build-env:
	python -m venv env
	$(call activate-env) && python -m pip install --upgrade pip

install:
	$(call activate-env) && pip install -r requirements.txt

clean:
	rm -rf env
	find . -name "*.pyc" -exec rm -f {} +
	find . -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

reset: clean build-env install
