from kedro.pipeline import Pipeline, node, pipeline

from .nodes import create_augmenter


def create_pipeline(**kwargs) -> Pipeline:
    """Function creating Data Augmentation pipeline.

    Returns:
        Pipeline: Created Data Augmentation pipeline.
    """
    return pipeline(
        [
            node(
                func=create_augmenter,
                inputs="params:augmentations",
                outputs="augmenter",
                name="create_augmenter",
            )
        ],
    )
