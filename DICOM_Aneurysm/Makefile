.ONESHELL:

SHELL = /bin/bash
CONDA_ACTIVATE = source $$(conda info --base)/etc/profile.d/conda.sh ; conda activate ; conda activate

workers = 1
device = 0

.PHONY: help
help:
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m  %-30s\033[0m %s\n", $$1, $$2}'

activate: ## activate conda environment
	$(CONDA_ACTIVATE) dicom_aneursym

install: ## create conda environment and install packages
	source $$(conda info --base)/etc/profile.d/conda.sh ; conda activate ;
	conda create -n dicom_aneursym python=3.9
	$(CONDA_ACTIVATE) dicom_aneursym
	pip install -r requirements.txt

merge: activate	## merge files from one channel to 3 channels 
	@echo "you have to make a complete copy of the folder before you can use merge!"
	@echo "do it with cp -r then change database.yaml file address"
	@echo "=============================="
	python merge.py \
		'/mnt/new_ssd/projects/Anevrism/Data/brain_cta/output_mosaic_3d/database.yaml'
	
parse: activate ## parse files from dicom to png
	python parser.py \
		'/mnt/new_ssd/projects/Anevrism/Data/brain_cta/Split' \
		--output-folder '/mnt/new_ssd/projects/Anevrism/Data/brain_cta/output_png' \
		--cores 10

