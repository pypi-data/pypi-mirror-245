.ONESHELL:
.SILENT:
.SHELLFLAGS := -c
.DEFAULT_GOAL =


VENV := .venv
PROJECT_NAME := $(notdir $(CURDIR))
PACKAGE_NAME := $(subst -,_,$(PROJECT_NAME))
GIT_TAG := $(shell git describe --tags --abbrev=0)
CURRENT_BRANCH := $(shell git branch --show-current)
CLEANED_TAG := $(subst v,,$(GIT_TAG))

CLEAN_DIRS = build dist __pycache__ .pdm-build .pytest_cache .mypy_cache .ruff_cache __pypackages__



ifeq ($(OS),Windows_NT)
	SHELL = cmd
	bin := $(VENV)\Scripts
	python_exec := $(bin)\python
	pip_exec := $(bin)\pip
    # VERSION_RAW := $(shell powershell -noprofile -Command "(Get-Content src\$(PACKAGE_NAME)\__version__.py -Raw) -replace '__version__ = ',''")
	# VERSION_RAW := $(shell findstr "^__version__" src\$(PACKAGE_NAME)\__about__.py)

.PHONY: clean
clean:
	if exist $(PACKAGE_NAME).egg-info rd /s /q $(PACKAGE_NAME).egg-info
	for %%i in ($(CLEAN_DIRS)) do ( if exist %%i rd /s /q %%i )

.PHONY: set_venv
set_venv:
	python -m venv .venv

else
	bin := $(VENV)/bin
	python_exec := $(bin)/python3
	pip_exec := $(bin)/pip
    # VERSION_RAW := $(shell cat src/$(PACKAGE_NAME)/__version__.py | awk -F "'" '/__version__/ {print $$2}')
	# VERSION_RAW := $(shell grep -E "^__version__" src/$(PACKAGE_NAME)/__about__.py)

.PHONY: clean
clean:
	rm -rf $(PACKAGE_NAME).egg-info
	for dir in $(CLEAN_DIRS); do \
		rm -rf $$dir; \
	done

.PHONY: set_venv
set_venv:
	python3 -m venv .venv

endif

# VERSION := $(subst ',,$(subst ",,$(subst __version__ = ,,$(VERSION_RAW))))


.PHONY: info latest_tag setup list fmt test lint release
info:
	@echo "project name is: $(PROJECT_NAME)"
	@echo "package name is: $(PACKAGE_NAME)"
	@echo "__version__.py file's version is: $(VERSION)"

latest_tag:
	@echo "Latest Git tag (cleaned): $(CLEANED_TAG)"

setup:
	$(python_exec) -m pip install --upgrade pip
	$(python_exec) -m pip install -r requirements.txt

list:
	$(python_exec) -m pip list

lint:
	$(python_exec) -m mypy src/ tests/
	$(python_exec) -m ruff check .

fmt:
	$(python_exec) -m ruff format .
	$(python_exec) -m ruff check . --fix

test:
	$(python_exec) -m pytest

build:
	$(python_exec) -m build

upload:
	$(python_exec) -m twine upload dist/* --config-file .pypirc

test_upload:
	$(python_exec) -m twine upload --repository testpypi dist/* --config-file .pypirc

release:
	git add .
	git commit -m "release v$(VERSION)"
	git push origin $(CURRENT_BRANCH)
	git tag -a v$(VERSION) -m "release v$(VERSION)"
	git push origin v$(VERSION)

pypi: clean lint fmt test build upload

testpypi: clean lint fmt test build test_upload
