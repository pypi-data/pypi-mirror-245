DESTDIR ?= /
UT ?=

VENV_DIR = ./venv
VENV = . $(VENV_DIR)/bin/activate;

SHELL = /usr/bin/env bash
PYTHON := $(shell which python3)
PACKAGE := $(shell $(PYTHON) setup.py --name | tr '-' '_')
VERSION := $(shell $(PYTHON) setup.py --version)

# List of files in the repository
TEST_FILES := $(wildcard test/test_*.py)
PKG_FILES := $(shell find $(PACKAGE) -type f -name '*.py')
REQ_FILES := $(wildcard requirements*.txt)

# Inferred targets from file names
LINT_TARGETS := setup.py $(PKG_FILES) $(BIN_FILES) $(shell find test -type f -name '*.py')
TEST_TARGETS := $(TEST_FILES:test/test_%.py=test_%)
EXT_TARGETS := $(wildcard ext/*)

.PHONY: \
	$(EXT_TARGETS) \
	$(REQ_FILES) \
	$(TEST_TARGETS) \
	clean \
	ext \
	format \
	install \
	lint \
	requirements \
	test

default:


clean:
	@rm -rf .pytest_cache
	@rm -rf .eggs
	@rm -rf dist
	@rm -rf build
	@rm -rf $(PACKAGE).egg-info


requirements: $(REQ_FILES)
$(REQ_FILES):
	@$(PYTHON) -m pip install --disable-pip-version-check -r $@


dist: dist/$(PACKAGE)-$(VERSION).tar.gz
dist/$(PACKAGE)-$(VERSION).tar.gz: $(PKG_FILES) setup.py
	$(VENV) pip install --disable-pip-version-check wheel
	$(VENV) python setup.py sdist bdist_wheel

upload: dist
	$(VENV) pip install --disable-pip-version-check twine
	$(VENV) twine upload dist/*$(VERSION)*

upload-test: dist
	@$(PYTHON) -m pip install --disable-pip-version-check twine
	$(PYTHON) -m twine upload --repository testpypi dist/*$(VERSION)*

format:
	@black $(LINT_TARGETS)
lint:
	@flake8 --filename='*' $(LINT_TARGETS)
type-check:
	@mypy $(PACKAGE) test/  example.py


test:
	$(VENV) pytest --log-level=DEBUG -W default -v -s
$(TEST_TARGETS):
	$(VENV) pytest --log-cli-level=DEBUG -W default -v -s test/$(@).py $(if $(UT),-k $(UT),)


install:
	$(VENV) python setup.py install

$(VENV_DIR): requirements.txt
	rm -rf "$(VENV_DIR)"
	python3 -m venv "$(VENV_DIR)"
	$(VENV) pip install wheel
	$(VENV) pip install -r requirements.txt