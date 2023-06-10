from kedro.pipeline import Pipeline, node, pipeline

from .nodes import create_config, create_model, train_model


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
                outputs="StarDist2D",
                name="create_model",
            ),
            node(
                func=train_model,
                inputs=["StarDist2D", "train_data", "augmenter", "params:StarDist2D"],
                outputs="StarDist2D_trained",
                name="train_model",
            ),
        ]
    )
