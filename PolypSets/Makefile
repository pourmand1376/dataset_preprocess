.ONESHELL:

SHELL = /bin/bash
CONDA_ACTIVATE = source $$(conda info --base)/etc/profile.d/conda.sh ; conda activate ; conda activate


.PHONY: help
help: update
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m  %-30s\033[0m %s\n", $$1, $$2}'

update: ## activate conda environment
	git pull

download: ## download the dataset
	./download.sh

install: update ## install required packages
	pip install -r requirements.txt


