export PATH := $(PATH):node_modules/.bin

SOURCES = \
	$(wildcard src/docpooltheme/*) \
	webpack.config.js

.PHONY: all
all: build

.PHONY: build
build: clean node_modules $(SOURCES)
	yarn run build

.PHONY: watch
watch: clean node_modules $(SOURCES)
	yarn run watch

.PHONY: clean
clean:
	$(RM) -r theme

.PHONY: purge
purge: clean
	$(RM) -r .plone

node_modules: package.json
	yarn install
	touch node_modules
