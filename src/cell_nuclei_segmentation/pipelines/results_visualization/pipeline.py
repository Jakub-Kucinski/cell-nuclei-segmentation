from kedro.pipeline import Pipeline, node, pipeline

from .nodes import create_images, predict


def create_pipeline(**kwargs) -> Pipeline:
    """Function creating Results Visualization pipeline.

    Returns:
        Pipeline: Created Results Visualization pipeline.
    """
    return pipeline(
        [
            node(
                predict,
                inputs=["StardistModelFineTuned", "test_data", "params:ImageNames"],
                outputs="Predictions",
                name="predict",
            ),
            node(
                create_images,
                inputs=[
                    "Predictions",
                    "test_data",
                    "params:ImageNames",
                ],
                outputs=None,
                name="create_images",
            ),
        ],
        tags=["results_visualization"],
    )
