from kedro.pipeline import Pipeline, node, pipeline

from .nodes import dummy_download


def create_pipeline(**kwargs) -> Pipeline:
    """Function creating Data Download pipeline.

    Returns:
        Pipeline: Created Data Download pipeline.
    """
    return pipeline(
        [
            node(
                dummy_download,
                inputs=None,
                outputs="CellNucleiRaw",
                name="dummy_download",
            )
        ],
        tags=["model_validation", "results_visualization"],
    )
