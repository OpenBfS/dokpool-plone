### Defensive settings for make:
#     https://tech.davis-hansson.com/p/make/
SHELL:=bash
.ONESHELL:
.SHELLFLAGS:=-xeu -o pipefail -O inherit_errexit -c
.SILENT:
.DELETE_ON_ERROR:
MAKEFLAGS+=--warn-undefined-variables
MAKEFLAGS+=--no-builtin-rules

# We like colors
# From: https://coderwall.com/p/izxssa/colored-makefile-for-golang-projects
RED=`tput setaf 1`
GREEN=`tput setaf 2`
RESET=`tput sgr0`
YELLOW=`tput setaf 3`

IMAGE_NAME=git.starzel.de:5050/bfs/dokpool

# get branch name if not running in CI
ifndef CI_COMMIT_REF_NAME
	CI_COMMIT_REF_NAME=$$(git rev-parse --abbrev-ref HEAD)
endif
IMAGE_TAG=${CI_COMMIT_REF_NAME}

# get rev if not running in CI
ifndef CI_COMMIT_SHORT_SHA
	CI_COMMIT_SHORT_SHA=$$(git rev-parse --short HEAD)
endif

# Python checks
UV?=uv

# installed?
ifeq (, $(shell which $(UV) ))
  $(error "UV=$(UV) not found in $(PATH)")
endif

REPOSITORY_SETTINGS := $(shell uvx repoplone settings dump)

PLONE_SITE_ID=Plone
BACKEND_FOLDER=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
PYTHON_VERSION := $(shell echo '$(REPOSITORY_SETTINGS)' | jq -r '.backend.python_version')
PLONE_VERSION := $(shell echo '$(REPOSITORY_SETTINGS)' | jq -r '.backend.base_package_version')
PACKAGE_NAME := $(shell echo '$(REPOSITORY_SETTINGS)' | jq -r '.backend.name')

VENV_FOLDER=$(BACKEND_FOLDER)/.venv
export VIRTUAL_ENV=$(VENV_FOLDER)
BIN_FOLDER=$(VENV_FOLDER)/bin

# Environment variables to be exported
export PYTHONWARNINGS := ignore
export DOCKER_BUILDKIT := 1

all: build

# Add the following 'help' target to your Makefile
# And add help text after each target name starting with '\#\#'
.PHONY: help
help: ## This help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: debug-settings
debug-settings:  ## Debug settings
	@echo "Virtual Environment: $(VENV_FOLDER)"
	@echo "PYTHON_VERSION: $(PYTHON_VERSION)"
	@echo "PLONE_VERSION: $(PLONE_VERSION)"
	@echo "PACKAGE_NAME: $(PACKAGE_NAME)"
	@echo "EXAMPLE_CONTENT_FOLDER: $(EXAMPLE_CONTENT_FOLDER)"
	@echo "IMAGE_NAME: $(IMAGE_NAME)"

mxdev:
	@echo "$(GREEN)==> Run mxdev to get deps from source$(RESET)"
	@uvx mxdev[uv] -c mx.ini

############################################
# Config
############################################
instance/etc/zope.ini instance/etc/zope.conf: instance.yaml ## Create instance configuration
	@echo "$(GREEN)==> Create instance configuration$(RESET)"
	@uvx cookiecutter -f --no-input -c 2.4.1 --config-file instance.yaml gh:plone/cookiecutter-zope-instance
	@uvx cookiecutter -f --no-input -c 2.4.1 --config-file instance_relstorage.yaml gh:plone/cookiecutter-zope-instance
	cp templates/zope.ini instance/etc/zope.ini
	cp templates/zope.ini instance_relstorage/etc/zope.ini
	@echo "<zodb_db temporary>">>instance/etc/zope.conf
	@echo "    <temporarystorage>">>instance/etc/zope.conf
	@echo "    name Temporary database (for sessions)">>instance/etc/zope.conf
	@echo "    </temporarystorage>">>instance/etc/zope.conf
	@echo "    mount-point /temp_folder">>instance/etc/zope.conf
	@echo "    container-class Products.TemporaryFolder.TemporaryContainer">>instance/etc/zope.conf
	@echo "</zodb_db>">>instance/etc/zope.conf
	@echo "<zodb_db temporary>">>instance_relstorage/etc/zope.conf
	@echo "    <temporarystorage>">>instance_relstorage/etc/zope.conf
	@echo "    name Temporary database (for sessions)">>instance_relstorage/etc/zope.conf
	@echo "    </temporarystorage>">>instance_relstorage/etc/zope.conf
	@echo "    mount-point /temp_folder">>instance_relstorage/etc/zope.conf
	@echo "    container-class Products.TemporaryFolder.TemporaryContainer">>instance_relstorage/etc/zope.conf
	@echo "</zodb_db>">>instance_relstorage/etc/zope.conf

.PHONY: config
config: instance/etc/zope.ini

############################################
# Installation / Cleanup
############################################
.PHONY: update-constraints
update-constraints: ## Update backend constraints
	@echo "$(GREEN)==> Update backend constraints$(RESET)"
	@uvx repoplone deps constraints

.PHONY: sync
sync: update-constraints ## Sync project dependencies
	@echo "$(GREEN)==> Sync project dependencies$(RESET)"
	@uv sync

.PHONY: install
install: mxdev sync config ## Install Plone and dependencies

.PHONY: clean
clean: ## Clean installation and instance
	@echo "$(RED)==> Cleaning environment and build$(RESET)"
	@rm -rf $(VENV_FOLDER) pyvenv.cfg .installed.cfg instance/etc instance_relstorage/etc .venv .pytest_cache .ruff_cache constraints* requirements*

.PHONY: remove-data
remove-data: ## Remove all content
	@echo "$(RED)==> Removing all content$(RESET)"
	rm -rf $(VENV_FOLDER) instance/var

############################################
# Server Actions
############################################
.PHONY: start
start: $(VENV_FOLDER) instance/etc/zope.ini ## Start a Plone instance on localhost:8080
	@uv run runwsgi instance/etc/zope.ini config_file=zope.conf

.PHONY: start-relstorage
start-relstorage: $(VENV_FOLDER) instance_relstorage/etc/zope.ini ## Start a Plone instance on localhost:8080
	@uv run runwsgi instance_relstorage/etc/zope.ini config_file=zope.conf

.PHONY: console
console: $(VENV_FOLDER) instance/etc/zope.ini ## Start a console into a Plone instance
	@uv run zconsole debug instance/etc/zope.conf config_file=zope.conf

.PHONY: create-site
create-site: $(VENV_FOLDER) instance/etc/zope.ini ## Create a new site from scratch
	@uv run zconsole run instance/etc/zope.conf ./scripts/create_site.py

############################################
# Distribution
############################################
.PHONY: update-distribution
update-distribution: $(VENV_FOLDER) ## Export example content inside package
	@echo "$(GREEN)==> Export distribution content into docpool.distribution $(RESET)"
	if [ -d src/docpool.distribution/src/docpool/distribution/distributions/docpooldemo/content ]; then rm -r src/docpool.distribution/src/docpool/distribution/distributions/docpooldemo/content/* ;fi
	@$(BIN_FOLDER)/export-distribution instance/etc/zope.conf $(PLONE_SITE_ID)

############################################
# QA
############################################
.PHONY: lint
lint: ## Check and fix code base according to Plone standards
	@echo "$(GREEN)==> Lint codebase$(RESET)"
	@uvx ruff@latest check --fix --config $(BACKEND_FOLDER)/pyproject.toml
	@uvx pyroma@latest -d .
	@uvx check-python-versions@latest .
	@uvx zpretty@latest --check src
	npm run prettier

.PHONY: format
format: ## Check and fix code base according to Plone standards
	@echo "$(GREEN)==> Format codebase$(RESET)"
	@uvx ruff@latest check --select I --fix --config $(BACKEND_FOLDER)/pyproject.toml
	@uvx ruff@latest format --config $(BACKEND_FOLDER)/pyproject.toml
	@uvx zpretty@latest -i src
	npm run prettier:fix

############################################
# i18n
############################################
.PHONY: i18n
i18n: $(VENV_FOLDER) ## Update locales
	@echo "$(GREEN)==> Updating locales$(RESET)"
	@uv pip install i18ndude
	@ls src |xargs uv run python ./scripts/update_locales.py

############################################
# Tests
############################################
.PHONY: test
test: $(VENV_FOLDER) ## run tests
	@$(BIN_FOLDER)/zope-testrunner --auto-color --auto-progress \
	--test-path src/docpool.base \
	--test-path src/docpool.api/src \
	--test-path src/docpool.base \
	--test-path src/elan.journal \
	--test-path src/docpool.doksys/src \
	--test-path src/docpool.elan \
	--test-path src/docpool.rei \
	--test-path src/docpool.ui \
	-D

# E2E Tests
.PHONY: install-acceptance
install-acceptance: $(VENV_FOLDER) ## run e2e tests
	@uv run playwright install
	@uv run playwright install-deps

# E2E Tests
.PHONY: test-acceptance
test-acceptance: $(VENV_FOLDER) ## run e2e tests
	@uv run pytest tests/

# E2E Tests
.PHONY: coverage-acceptance
coverage-acceptance: $(VENV_FOLDER) ## run e2e tests
	@uv pip install coverage
	@echo "$(GREEN)==> Erasing old coverage results$(RESET)"
	@uv run coverage erase
	@echo "$(GREEN)==> Running test coverage analysis for playwright tests...$(RESET)"
	@uv run coverage run -p --source=src $(BIN_FOLDER)/pytest tests/
	@uv run coverage combine
	mv .coverage .coverage.acceptance

.PHONY: coverage
coverage: ## generate test-coverage report
	@uv pip install coverage
	@echo "$(GREEN)==> Erasing old coverage results$(RESET)"
	@uv run coverage erase
	@echo "$(GREEN)==> Running test coverage analysis for all packages...$(RESET)"
	@uv run coverage run -p --source=src $(BIN_FOLDER)/zope-testrunner --auto-color --auto-progress \
	--test-path src/docpool.api/src \
	--test-path src/docpool.base \
	--test-path src/elan.journal \
	--test-path src/docpool.elan \
	--test-path src/docpool.rei \
	--test-path src/docpool.doksys/src \
	--test-path src/docpool.ui \
	|| exit 1
	@echo "$(GREEN)==> Creating test coverage report$(RESET)"
	@uv run coverage combine
	mv .coverage .coverage.unit

############################################
# Container images
############################################
.PHONY: build-image
build-image:  ## Build Container Images
	@echo "$(GREEN)==> Building image $(IMAGE_NAME) $(RESET)"
	@DOCKER_BUILDKIT=1 docker build . -t $(IMAGE_NAME):$(IMAGE_TAG) -f Dockerfile --build-arg PYTHON_VERSION=$(PYTHON_VERSION) --build-arg PLONE_VERSION=$(PLONE_VERSION) --build-arg GIT_COMMIT=$(CI_COMMIT_SHORT_SHA)

.PHONY: build-image-ci
build-image-ci: build-image ## Build Docker Image
	@docker push $(IMAGE_NAME):$(IMAGE_TAG)

# Update acceptance base Docker images
# Needed for Plone or deps updates
.PHONY: acceptance-update-image
acceptance-update-image:  ## Build Docker Images
	@DOCKER_BUILDKIT=1 docker build . -t $(IMAGE_NAME):acceptance -f Dockerfile.acceptance --build-arg PLONE_VERSION=$(PLONE_VERSION)

.PHONY: acceptance-push-ci
acceptance-push-ci: acceptance-update-image ## Build Docker Image
	@docker push $(IMAGE_NAME):acceptance

############################################
# Plone CLI
############################################
add: $(VENV_FOLDER)
	@uvx plonecli add $(filter-out $@,$(MAKECMDGOALS))

############################################
# Theme and Webpack stuff
############################################

# uivars
build_dir=$(BACKEND_FOLDER)/src/docpool.ui/docpool/ui/static/build

.PHONY: clean-ui
clean-ui: ## remove  uibuild
	rm -rf $(build_dir)
	mkdir -p $(build_dir)

.PHONY: purge-ui
purge-ui: clean-ui ## Purge build files/node_modules/.plone cache
	rm -rf $(BACKEND_FOLDER)/node_modules

.PHONY: install-ui
install-ui: ## Install js dependencies for webpack
	cd $(BACKEND_FOLDER) && npm install

.PHONY: watch-ui
watch-ui: ## Develop the ui
	cd $(BACKEND_FOLDER) && npm run watch

.PHONY: build-ui
build-ui: ## Build the ui
	cd $(BACKEND_FOLDER) && npm run build
