# Makefile for building the project

### Defensive settings for make:
#     https://tech.davis-hansson.com/p/make/
SHELL:=bash
.ONESHELL:
.SHELLFLAGS:=-xeu -o pipefail -O inherit_errexit -c
.SILENT:
.DELETE_ON_ERROR:
MAKEFLAGS+=--warn-undefined-variables
MAKEFLAGS+=--no-builtin-rules

# Add the following 'help' target to your Makefile
# And add help text after each target name starting with '\#\#'
.PHONY: help
help: .SHELLFLAGS:=-eu -o pipefail -O inherit_errexit -c
help: ## This help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

# Project vars
project_dir=$(CURDIR)
webpack_dir=$(CURDIR)/Plone/src/docpool.theme/docpool/theme/webpack_resources
build_dir=$(webpack_dir)/theme/docpooltheme

all: purge install-deps update-bundle

.PHONY: purge
purge:  ## Purge build files/node_modules/.plone cache
	rm -rf $(build_dir)
	mkdir -p $(build_dir)
	rm -rf $(webpack_dir)/node_modules
	rm -rf $(webpack_dir)/.plone

clean:
	rm -rf $(build_dir)
	mkdir -p $(build_dir)

install-deps: install-npm-deps  ## Install js deps

install-npm-deps:
	cd $(webpack_dir) && npm install

update-bundle: clean  ## Update bundle files
	cd $(webpack_dir) && npm run build

commit-bundle: update-bundle  ## Update and commit bundle
	git add $(build_dir)
	git commit -m 'Update bundle files' $(build_dir)
