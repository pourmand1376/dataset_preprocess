.ONESHELL:

SHELL = /bin/bash
CONDA_ACTIVATE = source $$(conda info --base)/etc/profile.d/conda.sh ; conda activate ; conda activate

workers = 1
device = 0

.PHONY: help
help: update
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m  %-30s\033[0m %s\n", $$1, $$2}'

update: ## activate conda environment
	git pull

install: update## create conda environment and install packages
	source $$(conda info --base)/etc/profile.d/conda.sh ; conda activate ;
	conda create -n dicom_aneurysm python=3.9
	$(CONDA_ACTIVATE) dicom_aneurysm
	conda install opencv
	pip install -r requirements.txt

merge: update	## merge files from one channel to 3 channels 
	@echo "you have to make a complete copy of the folder before you can use merge!"
	@echo "do it with cp -r then change database.yaml file address"
	@echo "=============================="
	$(CONDA_ACTIVATE) dicom_aneurysm
	python merge.py \
		'/mnt/new_ssd/projects/Anevrism/Data/brain_cta/output_mosaic_3d/database.yaml'
	
parse: update ## parse files from dicom to png
	$(CONDA_ACTIVATE) dicom_aneurysm
	python parser.py \
		'/mnt/new_ssd/projects/Anevrism/Data/brain_cta/Split' \
		--output-folder '/mnt/new_ssd/projects/Anevrism/Data/brain_cta/output_png' \
		--cores 10

exp=exp29
task=val
min=2
val_patient_normal_dataset: update ## see the results patient-wise
	python val.py  /mnt/new_ssd/projects/Anevrism/Data/brain_cta/output_folder/$(task)		\
		/mnt/new_ssd/projects/Anevrism/Models/pourmand/yolov5/runs/val/$(exp)/labels/	\
		--min-count=$(min)

val_patient_trimmed_dataset: update ## see the results patient-wise
	python val.py  /mnt/new_ssd/projects/Anevrism/Data/brain_cta/output_trimmed/$(task)		\
		/mnt/new_ssd/projects/Anevrism/Models/pourmand/yolov5/runs/val/$(exp)/labels/	\
		--min-count=$(min)