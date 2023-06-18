from kedro.pipeline import Pipeline, node, pipeline

from .nodes import create_config, create_model, model_training, threshold_optimization


def create_pipeline(**kwargs) -> Pipeline:
    """Function creating Model Training pipeline.

    Returns:
        Pipeline: Created Model Training pipeline.
    """
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
                func=model_training,
                inputs=[
                    "StardistModel",
                    "train_data",
                    "augmenter",
                    "params:TrainingParams",
                ],
                outputs="StardistModelFineTuned",
                name="model_training",
            ),
            node(
                func=threshold_optimization,
                inputs=["StardistModelFineTuned", "train_data", "test_data"],
                outputs="optimized_thresholds",
                name="threshold_optimization",
            ),
        ],
    )
