# Base or Root Directory Setup
BASEDIR := .

# Cache Directories
PROJ_CACHE_HOME := $(BASEDIR)/.cache
MYPY_CACHE_DIR := $(PROJ_CACHE_HOME)/.mypy_cache
PYTEST_CACHE_DIR := $(PROJ_CACHE_HOME)/.pytest_cache
NETRC := $(PROJ_CACHE_HOME)/.netrc

# Virtual Folder. Use .venv so Visual Studio Code recognize the packages
VENV := $(BASEDIR)/.venv

# Requirements directory and files
REQUIREMENTS_BASEDIR := $(BASEDIR)/requirements
REQUIREMENTS_INPUT := $(wildcard $(REQUIREMENTS_BASEDIR)/*.in)

# Versions
PYTHON_VERSION := $(shell cat .python-version)
PYPROJECT_PYTHON_VERSION := $(shell cat .python-version | cut -d"." -f1,2)

# Python Installation Commands
INSTALL_PY_ENV_COMMAND := pyenv install $(PYTHON_VERSION) --skip-existing
ACTIVATE_PY_ENV_COMMAND := pyenv local

# Bin Setup (This will be different for Windows, Mac, and Unix)
BIN :=$(VENV)/bin

# Get Local Machine Name
LOCALHOST := $$($(BIN)/python -c "import socket; s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM); s.connect(('8.8.8.8', 80)); print(s.getsockname()[0]);")

# Command to figure out the version of each pypi package.
PIP_COMPILE := $(BIN)/python -m piptools compile -q --no-header --strip-extras --allow-unsafe --resolver=backtracking --no-emit-index-url

# Command to get local dev version for the wheel
RELEASE_VERSION := $$($(BIN)/python -m setuptools_scm)

# **************************************************************************************************************************
# **** NOTE:
#     Targets 
#        If they are preceeded by .PHONY then you can call the target with the syntax:
#           make <target>
#        If target name followed with a double hash (##), then any text after the double hash is for the `make help` output.
# **************************************************************************************************************************

# ************************************************************************************
# ********************* Build the app ************************************************
# ************************************************************************************

build: deps-keep check-code-quality ## Build the project

rebuild: deps-update check-code-quality ## Rebuild the project

check-code-quality: black pylint mypy pydoclint test-unit ## Check the code quality before checkin (black, pylint, mypy, pydocstyle, and test)

# ************************************************************************************
# ********************* Cleaning Environment *****************************************
# ************************************************************************************
clean-all: clean deps-clean pypack-clean ## Clean the entire environment

clean: ## Clean up local environment.
	@echo "Clean up old environment"
	rm -rf "$(VENV)"
	rm -rf "$(PROJ_CACHE_HOME)"
	rm -rf "$(BASEDIR)/build"
	rm -rf "$(BASEDIR)/cov_html"
	# Remove all pycache
	find . | grep '__pycache__' | xargs rm -rf
	# Remove egg-info
	find . -type d | grep '.egg-info' | xargs rm -rf


# ************************************************************************************
# ********************* Format and linting *******************************************
# ************************************************************************************

format-code: ## Run actually reformat the files using black.
	@echo "-------- Format Code with Black --------- "
	@$(BIN)/python -m black --version
	@$(BIN)/python -m black .

black: ## Perform Black formatter check and show diff.
	@echo "-------- Running Black --------- "
	@$(BIN)/python -m black --version
	@$(BIN)/python -m black --check --diff .

pylint: ## Perform Pylint Gitlab Version.
	@echo "-------- Running pylint-gitlab --------- "
	@$(BIN)/python -m pylint --version
	@$(BIN)/python -m pylint .

mypy: ## Perform MyPy.
	@echo "-------- Running mypy --------- "
	@$(BIN)/python -m mypy --version
	@$(BIN)/python -m mypy .

pydoclint: ## Perform PyDocStyle.
	@echo "-------- Running pydocstyle --------- "
	@$(BIN)/python -m pydocstyle --version | xargs echo "Version: "
	@echo "Checking python files for documentation standards."
	@$(BIN)/python -m pydocstyle --verbose src/.
	@$(BIN)/python -m pydocstyle --verbose test/.

# ************************************************************************************
# ********************* Testing ******************************************************
# ************************************************************************************

test-unit: ## Run PyTest.
	@echo "-------- Running tests --------- "
	rm -rf "$(BASEDIR)/cov_html"
	$(BIN)/python -m pytest --version
	$(BIN)/python -m pytest .

# ************************************************************************************
# ********************* Versioning ***************************************************
# ************************************************************************************

release-version: ## Version that will be released.
	@echo "Version we expect to deploy"
	@echo "$(RELEASE_VERSION)"

update-pyproject:
	@echo "-------- Python Package (sdist and wheel) --------- "
	@. "$(BIN)/activate"; \
	update-toml --path project.requires-python --value ">=${PYPROJECT_PYTHON_VERSION}" pyproject.toml;

# Create a new virtual environment ready for build, rebuild, or deps update.
prep-environment: install-python clean localenv

# Install pyenv
install-python: 
	@echo Install Python Version: $(PYTHON_VERSION)
	$(INSTALL_PY_ENV_COMMAND)
	@echo Activate Python Version: $(PYTHON_VERSION)
	$(ACTIVATE_PY_ENV_COMMAND)

# Creates or updates a virtual ennviroment with base tools
localenv:
	@echo "-------- Set up basic virtual environment --------"
	python -m venv $(VENV)
	# Install keyring from pypi directly to avoid a bootstrap issue, see GITLAB-964 for background
	$(BIN)/python -m pip install pip pip-tools keyring --upgrade

# ************************************************************************************
# ********************* Dependency Stuff *********************************************
# ************************************************************************************

deps-clean: 
	@echo "-------- Clean dependency directory --------"
	rm -rf $(REQUIREMENTS_BASEDIR)/constraints.txt $(REQUIREMENTS_INPUT:in=txt) $(REQUIREMENTS_INPUT:in=in-no-args)
	rm -rf src/*.egg-info

# Keep the current dependencies and don't do anything else.
deps-keep: prep-environment deps-install

# Forces all requirements .txt files to be rebuilt from scratch and installed into the venv.
# venv will be created if it doesn't exist. A basic venv is needed to make sure we have updated versions
# of core tooling installed, like pip and pip-tools.
deps-update: prep-environment deps-clean deps-resolve-all deps-install ## Perform clean the requirements dir, resolve the deps, and install them.

# Find dependency conflicts
deps-show: ## Show dependency tree with potential conflicts
	@echo "Show dependency pypi package tree with potential conflict. New in version 2 of pipdeptree"
	$(BIN)/python -m pipdeptree

deps-show-dev: ## Show dependency tree with potential conflicts
	@echo "Show dependency pypi package tree with potential conflict. New in version 2 of pipdeptree"
	$(BIN)/python -m pipdeptree

deps-show-reverse: ## Show dependency tree with potential conflicts
	@echo "Show dependency pypi package tree with potential conflict. New in version 2 of pipdeptree"
	$(BIN)/python -m pipdeptree --reverse

deps-show-reverse-dev: ## Show dependency tree with potential conflicts
	@echo "Show dependency pypi package tree with potential conflict. New in version 2 of pipdeptree"
	$(BIN)/python -m pipdeptree --reverse

# Rebuild the constraints file from all *.in files in the Requirements dir
# $@ is target name, @^ is the prerequisites (the *.in files).
$(REQUIREMENTS_BASEDIR)/constraints.txt: $(REQUIREMENTS_INPUT)
	@echo "-------- Rebuild the constraints file from *.in files --------"
	CONSTRAINTS=/dev/null $(PIP_COMPILE) --strip-extras -o $@ $^

# Rebuild the requirements files from all *.in files in the Requirements dir, taking constraints into account
# $@ is target name, @< is the first prerequisite (the *.in files).
# For each *.in file, create an additional *.in-no-args file that doesn't include any arguments (-c).
# This is used to include softer-pinned dependencies in pyproject.toml (only for libraries).
$(REQUIREMENTS_BASEDIR)/%.txt: $(REQUIREMENTS_BASEDIR)/%.in $(REQUIREMENTS_BASEDIR)/constraints.txt
	@echo "-------- Resolve dependencies across all files, incorporating layered constraints --------"
	CONSTRAINTS=constraints.txt $(PIP_COMPILE) --no-annotate -o $@ $<
	@grep -v -E '^-.*' $< > $(addsuffix .in-no-args, $(basename $<))

# Alias to collect all .txt files, including constraints
deps-resolve-all: $(REQUIREMENTS_BASEDIR)/constraints.txt $(REQUIREMENTS_INPUT:in=txt)

# Installs dependencies from txt files into venv
deps-install: ## Install the dependencies
	@echo "-------- Install dependencies into virtual environment --------"
	$(BIN)/python -m pip install '.[development]'
	$(BIN)/python -m pip install -e .

# ************************************************************************************
# ********************* Show all the variables used in this make file ****************
# ************************************************************************************
test-variables: ## Test the variables used in this make file
	@echo "List of variables used in this make file are:"
	@echo "  LOCALHOST: $(LOCALHOST)"
	@echo "  BASEDIR: $(BASEDIR)"
	@echo "  PROJ_CACHE_HOME: $(PROJ_CACHE_HOME)"
	@echo "  MYPY_CACHE_DIR: $(MYPY_CACHE_DIR)"
	@echo "  PYTEST_CACHE_DIR: $(PYTEST_CACHE_DIR)"
	@echo "  VENV: $(VENV)"
	@echo "  REQUIREMENTS_BASEDIR: $(REQUIREMENTS_BASEDIR)"
	@echo "  REQUIREMENTS_INPUT: $(REQUIREMENTS_INPUT)"
	@echo "  PYTHON_VERSION: $(PYTHON_VERSION)"
	@echo "  DOCKER_PYTHON_VERSION: $(DOCKER_PYTHON_VERSION)"
	@echo "  INSTALL_PY_ENV_COMMAND: $(INSTALL_PY_ENV_COMMAND)"
	@echo "  ACTIVATE_PY_ENV_COMMAND: $(ACTIVATE_PY_ENV_COMMAND)"
	@echo "  BIN: $(BIN)"
	@echo "  USER: $(USER)"
	@echo "  PACKAGE_NAME: $(PACKAGE_NAME)"
	@echo "  DOCKER_PACKAGE_NAME: $(DOCKER_PACKAGE_NAME)"
	@echo "  PIP_COMPILE: $(PIP_COMPILE)"
	@echo "  SCM_VERSION: $(SCM_VERSION)"

# ************************************************************************************
# ********************* Help Menu ****************************************************
# ************************************************************************************
help: ## Display this help
	@printf "\nusage : make <commands> \n\nthe following commands are available : \n"
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  \033[36m\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-25s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
	@printf "\n"
