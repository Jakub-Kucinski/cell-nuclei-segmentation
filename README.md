[![Pytest](https://github.com/Jakub-Kucinski/cell-nuclei-segmentation/actions/workflows/test-action.yml/badge.svg)](https://github.com/Jakub-Kucinski/cell-nuclei-segmentation/actions/workflows/test-action.yml)
# cell-nuclei-segmentation


# Table of Contents
- [cell-nuclei-segmentation](#cell-nuclei-segmentation)
- [Table of Contents](#table-of-contents)
- [Nuclear images dataset](#nuclear-images-dataset)
- [Libraries and tools](#libraries-and-tools)
- [Installation](#installation)
  - [Environment setup](#environment-setup)
  - [Dependencies update](#dependencies-update)
  - [Pre-commit installation](#pre-commit-installation)
  - [AWS access configuration](#aws-access-configuration)
- [Kedro visualization of pipelines](#kedro-visualization-of-pipelines)
- [Pipelines](#pipelines)
  - [Dataset download](#dataset-download)

# Nuclear images dataset
[An annotated fluorescence image dataset for training nuclear segmentation methods](https://www.ebi.ac.uk/biostudies/bioimages/studies/S-BSST265)


|  |  |
| -------- | -------- |
| Accession     | S-BSST265     |
| Description     | This dataset contains annotated fluorescent nuclear images of different tissue origins and sample preparation types and can be used to train machine-learning based nuclear image segmentation algorithms.     |
| Organism     | Homo sapiens     |
| Experimental design     | Preparation and immunofluorescence (IF) staining of different human cell and tissue types. Samples of in vitro cultivated normal and neuroblastoma human cell line, bone marrow and fresh primary tumor of neuroblastoma patients, and freshly frozen tumor tissue of a ganglioneuroma patient were processed properly for further IF stainings. At each staining, 4, 6-diamino-2-phenylindole (DAPI), a blue fluorescent dye, conventionally used for cellular imaging techniques, was applied to stain the nuclei. Microscopy images were acquired and subjected to nuclear image annotation by biology and pathology experts.     |


# Libraries and tools
- [Kedro](https://kedro.org/) - for reproducible, maintainable and modular data science code
- [Poetry](https://python-poetry.org/) - for dependency management
- [PyTorch](https://pytorch.org/) - for building and training neural networks
- [Lightning](https://www.pytorchlightning.ai/index.html) - for easier implementation of models and training
- [AWS S3](https://aws.amazon.com/s3/) - for storing and downloading datasets
- [DVC](https://dvc.org/) - for versioning of datasets and models
- [pytest](https://docs.pytest.org/en/stable/) - for testing

# Installation

## Environment setup

### Requirements

We strongly recommend using Linux as OS and VS Code as code editor.
In order to run following code the machine must meet following requirements:
- `Docker` installed (https://docs.docker.com/engine/install/ubuntu/#installation-methods)
- `Dev Containers` extension installed in VS Code (https://code.visualstudio.com/docs/devcontainers/tutorial#_install-the-extension)

### Opening DevContainer

In VS Code open Comman Palette (`Ctrl+Alt+P`) and type 'Open Folder in Container`. Choose following command and select directory with project. Wait for all the software to install.

In order to rebuild container to e.g. apply changes in environment type `Rebuild Container` in Comman Palette.


## Dependencies update

```shell
poetry update
```

## Pre-commit installation

```shell
pre-commit install
pre-commit autoupdate
```
To check all files without committing simply run:
```shell
pre-commit run --all-files
```

## AWS access configuration

```shell
export AWS_SHARED_CREDENTIALS_FILE="$(pwd)/conf/local/aws/credentials"
export AWS_CONFIG_FILE="$(pwd)/conf/base/aws/config"
export LOCAL_PROFILE_NAME={profile_name}
export AWS_PROFILE=$LOCAL_PROFILE_NAME
aws configure set aws_access_key_id {aws_access_key_id} --profile $LOCAL_PROFILE_NAME
aws configure set aws_secret_access_key {aws_secret_access_key} --profile $LOCAL_PROFILE_NAME
```

# Kedro visualization of pipelines
Not available yet
# Pipelines

## Dataset download
