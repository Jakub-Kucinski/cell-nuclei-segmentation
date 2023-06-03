[![Pytest](https://github.com/Jakub-Kucinski/cell-nuclei-segmentation/actions/workflows/test-action.yml/badge.svg)](https://github.com/Jakub-Kucinski/cell-nuclei-segmentation/actions/workflows/test-action.yml)
# cell-nuclei-segmentation


# Table of Contents
- [cell-nuclei-segmentation](#cell-nuclei-segmentation)
- [Table of Contents](#table-of-contents)
- [Nuclear images dataset](#nuclear-images-dataset)
- [Libraries and tools](#libraries-and-tools)
- [Installation](#installation)
  - [Development in VS Code DevContainer](#development-in-vs-code-devcontainer)
    - [Requirements](#requirements)
      - [Docker](#docker)
      - [NVIDIA drivers](#nvidia-drivers)
      - [NVIDIA docker](#nvidia-docker)
      - [VS Code](#vs-code)
  - [Environment setup](#environment-setup)
  - [Additional functionalities](#additional-functionalities)
    - [Dependencies update](#dependencies-update)
    - [Pre-commit](#pre-commit)
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

## Development in VS Code DevContainer

For high reproducibility and ease of development we recommend using VS Code DevContainer. It is a Docker container with all the necessary software installed. It can be run on any machine with Docker and NVIDIA GPU available.

### Requirements

#### Docker

https://docs.docker.com/engine/install/ubuntu/#installation-methods

#### NVIDIA drivers

https://docs.nvidia.com/datacenter/tesla/tesla-installation-notes/index.html#ubuntu-lts

#### NVIDIA docker

https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html#setting-up-nvidia-container-toolkit

#### VS Code

https://code.visualstudio.com/ with extension: `Dev Containers`

## Environment setup

With all the requirements installed, open VS Code and press `Ctrl+Shift+P` to open Command Palette. Type `Open Folder in Container` and select the project directory. Wait for the container to build and install all the necessary software.

## Additional functionalities
### Dependencies update

```shell
poetry update
```

### Pre-commit

To check all files without committing simply run:
```shell
pre-commit run --all-files
```

### AWS access configuration

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
