.PHONY: install reinstall clean test test-student test-solutions security-check bandit pip-audit run-tp1 check-env

VENV ?= .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
FIND_PYTHON := ./scripts/find_python.sh

STUDENT_TPS := tp2-injections/tests tp3-auth/tests tp4-web-api/tests tp6-challenge/tests
SOLUTION_TPS := instructor/solutions/tp2-injections/tests instructor/solutions/tp3-auth/tests instructor/solutions/tp4-web-api/tests instructor/solutions/tp6-challenge/tests

check-env:
	@test -x $(PYTHON) || (echo "Environnement absent. Lancez: make install" && exit 1)
	@$(PYTHON) -c "import flask" || ( \
		echo "Environnement cassé (python et pip ne correspondent pas)."; \
		echo "Lancez: make reinstall"; \
		exit 1)

install:
	@chmod +x $(FIND_PYTHON)
	@if [ -x "$(PYTHON)" ] && ! "$(PYTHON)" -c "import flask" 2>/dev/null && $(PIP) show flask >/dev/null 2>&1; then \
		echo "Environnement incohérent (python ≠ pip). Lancez: make reinstall"; \
		exit 1; \
	fi
	@if [ ! -x "$(PYTHON)" ]; then \
		PY=$$($(FIND_PYTHON)); \
		echo "Création du venv avec $$PY ($$($$PY --version))"; \
		"$$PY" -m venv "$(VENV)"; \
	fi
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	@$(PYTHON) -c "import flask; print('OK — Flask', flask.__version__)"

reinstall:
	@chmod +x $(FIND_PYTHON)
	@PY=$$($(FIND_PYTHON)); \
	echo "Recréation du venv avec $$PY ($$($$PY --version))"; \
	rm -rf "$(VENV)"; \
	"$$PY" -m venv "$(VENV)"; \
	$(PIP) install --upgrade pip; \
	$(PIP) install -r requirements.txt; \
	$(PYTHON) -c "import flask; print('OK — Flask', flask.__version__)"

clean:
	rm -rf $(VENV)

run-tp1: check-env
	$(PYTHON) tp1-audit/app/vulnerable_app.py

test-student: check-env
	$(PYTHON) -m pytest $(STUDENT_TPS) -v

test-solutions: check-env
	$(PYTHON) -m pytest $(SOLUTION_TPS) -v

test: test-student

bandit: check-env
	$(VENV)/bin/bandit -r tp5-sast/sample_project -ll

pip-audit: check-env
	$(VENV)/bin/pip-audit -r requirements.txt

security-check: bandit pip-audit
	@echo "Security checks completed."
