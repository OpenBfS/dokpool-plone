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

# Set distributions still in development
DISTRIBUTIONS="docpooldemo"
ALLOWED_DISTRIBUTIONS="docpooldemo"

IMAGE_NAME=git.starzel.de:5050/bfs/dokpool

IMAGE_TAG_VARNISH=varnish

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

PLONE_SITE_ID=Plone
BACKEND_FOLDER=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
PLONE_VERSION=$(shell cat $(BACKEND_FOLDER)/version.txt)
EXAMPLE_CONTENT_FOLDER=${BACKEND_FOLDER}/src/dokpool/setuphandlers/examplecontent

VENV_FOLDER=$(BACKEND_FOLDER)/.venv
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

requirements-mxdev.txt: pyproject.toml mx.ini ## Generate constraints file
	@echo "$(GREEN)==> Generate constraints file$(RESET)"
	@echo '-c https://dist.plone.org/release/$(PLONE_VERSION)/constraints.txt' > requirements.txt
	@uvx mxdev -c mx.ini

$(VENV_FOLDER): requirements-mxdev.txt ## Install dependencies
	@echo "$(GREEN)==> Install environment$(RESET)"
	@uv venv $(VENV_FOLDER)
	@uv pip install -r requirements-mxdev.txt

.PHONY: sync
sync: $(VENV_FOLDER) ## Sync project dependencies
	@echo "$(GREEN)==> Sync project dependencies$(RESET)"
	@uv pip install -r requirements-mxdev.txt

instance/etc/zope.ini instance/etc/zope.conf instance_relstorage/etc/zope.ini instance_relstorage/etc/zope.conf: instance.yaml ## Create instance configuration
	@echo "$(GREEN)==> Create instance configuration$(RESET)"
	@uvx cookiecutter -f --no-input -c 2.1.1 --config-file instance.yaml gh:plone/cookiecutter-zope-instance
	@uvx cookiecutter -f --no-input -c 2.1.1 --config-file instance_relstorage.yaml gh:plone/cookiecutter-zope-instance

.PHONY: config
config: instance/etc/zope.ini

.PHONY: install
install: $(VENV_FOLDER) config ## Install Plone and dependencies

.PHONY: clean
clean: ## Clean installation and instance
	@echo "$(RED)==> Cleaning environment and build$(RESET)"
	@rm -rf $(VENV_FOLDER) pyvenv.cfg .installed.cfg instance/etc .venv .pytest_cache .ruff_cache constraints* requirements*

.PHONY: remove-data
remove-data: ## Remove all content
	@echo "$(RED)==> Removing all content$(RESET)"
	rm -rf $(VENV_FOLDER) instance/var

.PHONY: start
start: $(VENV_FOLDER) instance/etc/zope.ini ## Start a Plone instance on localhost:8080
	@uv run runwsgi instance/etc/zope.ini

.PHONY: start-relstorage
start-relstorage: $(VENV_FOLDER) instance_relstorage/etc/zope.ini ## Start a Plone instance on localhost:8080
	@uv run runwsgi instance_relstorage/etc/zope.ini

.PHONY: console
console: $(VENV_FOLDER) instance/etc/zope.ini ## Start a console into a Plone instance
	@uv run zconsole debug  instance/etc/zope.conf instance/etc/zope.conf

.PHONY: create-site
create-site: $(VENV_FOLDER) instance/etc/zope.ini ## Create a new site from scratch
	DEVELOP_DISTRIBUTIONS=$(DISTRIBUTIONS) ALLOWED_DISTRIBUTIONS=$(DISTRIBUTIONS) uv run zconsole run instance/etc/zope.conf ./scripts/create_site.py

# Example Content
.PHONY: update-example-content
update-example-content: $(VENV_FOLDER) ## Export example content inside package
	@echo "$(GREEN)==> Export example content into $(EXAMPLE_CONTENT_FOLDER) $(RESET)"
	if [ -d $(EXAMPLE_CONTENT_FOLDER)/content ]; then rm -r $(EXAMPLE_CONTENT_FOLDER)/* ;fi
	@uv run plone-exporter instance/etc/zope.conf $(PLONE_SITE_ID) $(EXAMPLE_CONTENT_FOLDER)

# QA
.PHONY: lint
lint: ## Check and fix code base according to Plone standards
	@echo "$(GREEN)==> Lint codebase$(RESET)"
	@uvx ruff@latest check --fix --config $(BACKEND_FOLDER)/pyproject.toml
	@uvx pyroma@latest -d .
	@uvx check-python-versions@latest .
	@uvx zpretty@latest --check src

.PHONY: format
format: ## Check and fix code base according to Plone standards
	@echo "$(GREEN)==> Format codebase$(RESET)"
	@uvx ruff@latest check --select I --fix --config $(BACKEND_FOLDER)/pyproject.toml
	@uvx ruff@latest format --config $(BACKEND_FOLDER)/pyproject.toml
	@uvx zpretty@latest -i src

# i18n
.PHONY: i18n
i18n: $(VENV_FOLDER) ## Update locales
	@echo "$(GREEN)==> Updating locales$(RESET)"
	@uv pip install i18ndude
	@ls src |xargs uv run python ./scripts/update_locales.py

# Tests
.PHONY: test
test: $(VENV_FOLDER) ## run tests
	@uv run zope-testrunner --auto-color --auto-progress \
	--test-path src/docpool.api/src \
	--test-path src/elan.journal \
	--test-path src/docpool.doksys/src \
	--test-path src/docpool.elan \
	--test-path src/docpool.rei \
	-D

.PHONY: coverage
coverage: ## generate test-coverage report
	@uv pip install coverage
	@echo "$(GREEN)==> Erasing old coverage results$(RESET)"
	@uv run coverage erase
	@echo "$(GREEN)==> Running test coverage analysis for all packages...$(RESET)"
	@uv run coverage run -p --source=src $(VENV_FOLDER)/bin/zope-testrunner --auto-color --auto-progress \
	--test-path src/docpool.api/src \
	--test-path src/elan.journal \
	--test-path src/docpool.elan \
	--test-path src/docpool.rei \
	--test-path src/docpool.doksys/src \
	|| exit 1
	@echo "$(GREEN)==> Creating test coverage report$(RESET)"
	@uv run coverage combine
	@uv run coverage report
	@uv run coverage html

# Build Docker images
.PHONY: build-image
build-image:  ## Build Docker Images
	@docker buildx build --load --provenance=false --tag $(IMAGE_NAME):$(IMAGE_TAG) --file Dockerfile --build-arg PLONE_VERSION=$(PLONE_VERSION) --build-arg GIT_COMMIT=$(CI_COMMIT_SHORT_SHA) .

.PHONY: build-image-ci
build-image-ci: build-image ## Build Docker Image
	@docker push $(IMAGE_NAME):$(IMAGE_TAG)

.PHONY: build-image-varnish
build-image-varnish: ## Build Docker Image
	@docker buildx build --load --provenance=false --tag $(IMAGE_NAME):$(IMAGE_TAG_VARNISH) --file ../devops/varnish-build/Dockerfile .

.PHONY: build-image-varnish-ci
build-image-varnish-ci: build-image-varnish ## Build Docker Image
	@docker push $(IMAGE_NAME):$(IMAGE_TAG_VARNISH)

# Theme and Webpack stuff
# theme vars
build_dir=$(BACKEND_FOLDER)/src/docpool.theme/docpool/theme/static/build

.PHONY: clean-theme
clean-theme: ## remove theme build
	rm -rf $(build_dir)
	mkdir -p $(build_dir)

.PHONY: purge-theme
purge-theme: clean-theme ## Purge build files/node_modules/.plone cache
	rm -rf $(BACKEND_FOLDER)/node_modules

.PHONY: install-theme
install-theme: ## Install js dependencies for webpack
	cd $(BACKEND_FOLDER) && npm install

.PHONY: watch-theme
watch-theme: ## Develop the theme
	cd $(BACKEND_FOLDER) && npm run watch

.PHONY: build-theme
build-theme: ## Build the theme
	cd $(BACKEND_FOLDER) && npm run build
