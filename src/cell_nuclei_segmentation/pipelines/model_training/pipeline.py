from kedro.pipeline import Pipeline, node, pipeline

from .nodes import create_config, create_model, test_model


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=create_config,
                inputs="params:Config2D",
                outputs="Config2D",
                name="create_config",
            ),
            node(
                func=create_model,
                inputs=["Config2D", "params:StarDist2D"],
                outputs="StardistModel",
                name="create_model",
            ),
            node(
                func=test_model,
                inputs=["StardistModel"],
                outputs=None,
                name="test_model",
            ),
        ]
    )
