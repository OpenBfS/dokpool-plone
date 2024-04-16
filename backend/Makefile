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

BACKEND_FOLDER=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

PLONE_VERSION=$$(cat version.txt)

CODE_QUALITY_VERSION=2.1
ifndef LOG_LEVEL
	LOG_LEVEL=INFO
endif
CURRENT_USER=$$(whoami)
USER_INFO=$$(id -u ${CURRENT_USER})
LINT=docker run --rm -e LOG_LEVEL="${LOG_LEVEL}" -v "${BACKEND_FOLDER}":/github/workspace plone/code-quality:${CODE_QUALITY_VERSION} check
FORMAT=docker run --rm --user="${USER_INFO}" -e LOG_LEVEL="${LOG_LEVEL}" -v "${BACKEND_FOLDER}":/github/workspace plone/code-quality:${CODE_QUALITY_VERSION} format

IMAGE_NAME=git.starzel.de:5050/bfs/dokpool
IMAGE_TAG=${CI_COMMIT_REF_NAME}

# Python checks
PYTHON?=python3

# installed?
ifeq (, $(shell which $(PYTHON) ))
  $(error "PYTHON=$(PYTHON) not found in $(PATH)")
endif

# version ok?
PYTHON_VERSION_MIN=3.11
PYTHON_VERSION_OK=$(shell $(PYTHON) -c "import sys; print((int(sys.version_info[0]), int(sys.version_info[1])) >= tuple(map(int, '$(PYTHON_VERSION_MIN)'.split('.'))))")
ifeq ($(PYTHON_VERSION_OK),False)
  $(error "Need python $(PYTHON_VERSION) >= $(PYTHON_VERSION_MIN)")
endif


# Add the following 'help' target to your Makefile
# And add help text after each target name starting with '\#\#'
.PHONY: help
help: ## This help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: clean
clean: clean-build clean-pyc clean-test clean-venv clean-instance ## remove all build, test, coverage and Python artifacts

.PHONY: clean-instance
clean-instance: ## remove existing instance
	rm -fr instance etc inituser var

.PHONY: clean-venv
clean-venv: ## remove virtual environment
	rm -fr bin include lib lib64

.PHONY: clean-build
clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -rf {} +

.PHONY: clean-pyc
clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

.PHONY: clean-test
clean-test: ## remove test and coverage artifacts
	rm -f .coverage
	rm -fr htmlcov/

bin/pip:
	@echo "$(GREEN)==> Setup Virtual Env$(RESET)"
	$(PYTHON) -m venv .
	bin/pip install -U "pip" "wheel" "cookiecutter==2.6.0" "mxdev==4.0.2"

.PHONY: config
config: bin/pip  ## Create instance configuration
	@echo "$(GREEN)==> Create instance configuration$(RESET)"
	./bin/cookiecutter -f --no-input --config-file ./instance.yaml -c 2.0.0 gh:plone/cookiecutter-zope-instance
	./bin/cookiecutter -f --no-input --config-file ./instance_relstorage.yaml -c 2.0.0 gh:plone/cookiecutter-zope-instance

# i18n
bin/i18ndude: bin/pip
	@echo "$(GREEN)==> Install translation tools$(RESET)"
	bin/pip install i18ndude

.PHONY: i18n
i18n: bin/i18ndude ## Update locales
	@echo "$(GREEN)==> Updating locales$(RESET)"
	bin/update_locale

# TODO `make build`
# build:

sources/contentimport:  ## checkout contentimport
	git clone --branch=distribution gitlab@git.starzel.de:bfs/contentimport.git sources/contentimport

.PHONY: build-dev
build-dev: config sources/contentimport ## pip install Plone packages
	@echo "$(GREEN)==> Setup Build$(RESET)"
	bin/mxdev -c mx.ini
	bin/pip install -r requirements-mxdev.txt

.PHONY: build-dev-develop
build-dev-develop: config ## pip install Plone packages with debug-tools
	@echo "$(GREEN)==> Setup Build$(RESET)"
	bin/mxdev -c mx_develop.ini
	bin/pip install -r requirements-mxdev.txt


.PHONY: format
format: ## Format the codebase according to our standards
	@echo "$(GREEN)==> Format codebase$(RESET)"
	$(FORMAT)

.PHONY: lint
lint: lint-isort lint-black lint-flake8 lint-zpretty ## check code style

.PHONY: lint-black
lint-black: ## validate black formating
	$(LINT) black

.PHONY: lint-flake8
lint-flake8: ## validate black formating
	$(LINT) flake8

.PHONY: lint-isort
lint-isort: ## validate using isort
	$(LINT) isort

.PHONY: lint-pyroma
lint-pyroma: ## validate using pyroma
	$(LINT) pyroma

.PHONY: lint-zpretty
lint-zpretty: ## validate ZCML/XML using zpretty
	$(LINT) zpretty

.PHONY: test
test: ## run tests
	./bin/zope-testrunner --auto-color --auto-progress --test-path src/docpool.api/src --test-path src/elan.journal --test-path src/docpool.elan --test-path src/docpool.rei --test-path src/docpool.doksys/src -D


.PHONY: test_quiet
test_quiet: ## run tests removing deprecation warnings
	PYTHONWARNINGS=ignore ./bin/zope-testrunner --auto-color --auto-progress --test-path src/docpool.api/src --test-path src/elan.journal --test-path src/docpool.elan --test-path src/docpool.rei --test-path src/docpool.doksys/src

.PHONY: create-site
create-site: ## Create a new site from scratch
	DEVELOP_DISTRIBUTIONS=$(DISTRIBUTIONS) ALLOWED_DISTRIBUTIONS=$(DISTRIBUTIONS) PYTHONWARNINGS=ignore ./bin/zconsole run instance/etc/zope.conf scripts/create_site.py

.PHONY: start
start: ## Start a Plone instance on localhost:8080
	PYTHONWARNINGS=ignore ./bin/runwsgi instance/etc/zope.ini

.PHONY: start-relstorage
start-relstorage: ## Start a Plone instance on localhost:8080
	PYTHONWARNINGS=ignore ./bin/runwsgi instance_relstorage/etc/zope.ini

.PHONY: debug
debug: instance/etc/zope.ini ## Run debug console
	PYTHONWARNINGS=ignore ./bin/zconsole debug instance/etc/zope.conf

.PHONY: fg
fg: ## Start a Plone instance in debug-mode on localhost:8080
	PYTHONWARNINGS=ignore ./bin/runwsgi -d instance/etc/zope.ini

.PHONY: build-image
build-image: sources/contentimport  ## Build Docker Image
	@DOCKER_BUILDKIT=1 docker buildx build --load --provenance=false --tag $(IMAGE_NAME):$(IMAGE_TAG) --file Dockerfile --build-arg PLONE_VERSION=$(PLONE_VERSION) .

.PHONY: build-image-ci
build-image-ci: sources/contentimport build-image ## Build Docker Image
	@DOCKER_BUILDKIT=1 docker push $(IMAGE_NAME):$(IMAGE_TAG)

# Theme and Webpack stuff
# theme vars
webpack_dir=$(BACKEND_FOLDER)/src/docpool.theme/docpool/theme/webpack_resources
build_dir=$(webpack_dir)/theme/docpooltheme

.PHONY: clean-theme
clean-theme: ## remove theme build
	rm -rf $(build_dir)
	mkdir -p $(build_dir)

.PHONY: purge-theme
purge-theme:  ## Purge build files/node_modules/.plone cache
	rm -rf $(build_dir)
	mkdir -p $(build_dir)
	rm -rf $(webpack_dir)/node_modules
	rm -rf $(webpack_dir)/.plone

.PHONY: install-theme
install-theme: ## Install js dependencies for webpack
	cd $(webpack_dir) && npm install

.PHONY: watch-theme
watch-theme: ## Develop the theme
	cd $(webpack_dir) && npm run watch

.PHONY: update-bundle
update-bundle: clean-theme  ## Update bundle files
	cd $(webpack_dir) && npm run build

.PHONY: build-theme
build-theme: ## Build the theme
	cd $(webpack_dir) && npm run build

commit-bundle: update-bundle  ## Update and commit bundle
	git add $(build_dir)
	git commit -m 'Update bundle files' $(build_dir)
