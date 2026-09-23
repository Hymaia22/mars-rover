PYTHON := $(shell [ -x .venv/bin/python ] && echo .venv/bin/python || echo python3)
DEPLOY_DIR := .deploy

.PHONY: test run fix-start fix-end deploy rollback

test:
	$(PYTHON) -m pytest

run:
	$(PYTHON) -m examples.run_demo

fix-start:
	@mkdir -p .claude
	@touch .claude/fix-mode
	@echo "Mode correction activé : les fichiers de tests sont protégés."

fix-end:
	@rm -f .claude/fix-mode
	@echo "Mode correction désactivé."

deploy:
	@if [ -z "$(ENV)" ]; then echo "ENV requis, ex: make deploy ENV=staging" >&2; exit 1; fi
	@mkdir -p $(DEPLOY_DIR)
	@new=$$(git rev-parse --short HEAD); \
	if [ -f $(DEPLOY_DIR)/$(ENV).current ]; then \
		old=$$(cat $(DEPLOY_DIR)/$(ENV).current); \
		cp $(DEPLOY_DIR)/$(ENV).current $(DEPLOY_DIR)/$(ENV).previous; \
	else \
		old="(aucune)"; \
	fi; \
	echo "$$new" > $(DEPLOY_DIR)/$(ENV).current; \
	echo "deploy $(ENV): $$old -> $$new"

rollback:
	@if [ -z "$(ENV)" ]; then echo "ENV requis, ex: make rollback ENV=staging" >&2; exit 1; fi
	@if [ ! -f $(DEPLOY_DIR)/$(ENV).previous ]; then echo "rollback $(ENV): aucune version précédente, impossible de revenir en arrière" >&2; exit 1; fi
	@cur=$$(cat $(DEPLOY_DIR)/$(ENV).current 2>/dev/null || echo "(aucune)"); \
	prev=$$(cat $(DEPLOY_DIR)/$(ENV).previous); \
	cp $(DEPLOY_DIR)/$(ENV).current $(DEPLOY_DIR)/$(ENV).previous; \
	echo "$$prev" > $(DEPLOY_DIR)/$(ENV).current; \
	echo "rollback $(ENV): $$cur -> $$prev"
