"""Project pipelines."""
from typing import Dict

# from kedro.framework.project import find_pipelines
from kedro.pipeline import Pipeline

from cell_nuclei_segmentation.pipelines import (
    data_augmentations,
    data_download,
    data_preprocessing,
    model_evaluation,
    model_training,
)


def register_pipelines() -> Dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from pipeline names to ``Pipeline`` objects.
    """
    # pipelines = find_pipelines()
    # pipelines["__default__"] = sum(pipelines.values())
    # return pipelines
    data_download_pipeline = data_download.create_pipeline()
    data_augmentations_pipeline = data_augmentations.create_pipeline()
    data_processing_pipeline = data_preprocessing.create_pipeline()
    model_training_pipeline = model_training.create_pipeline()
    model_evaluation_pipeline = model_evaluation.create_pipeline()

    return {
        "__default__": data_download_pipeline
        + data_augmentations_pipeline
        + data_processing_pipeline
        + model_training_pipeline
        + model_evaluation_pipeline,
        "data_download": data_download_pipeline,
        "data_augmentations": data_augmentations_pipeline,
        "data_processing_pipeline": data_processing_pipeline,
        "model_training": model_training_pipeline,
        "model_evaluation": model_evaluation_pipeline,
    }
