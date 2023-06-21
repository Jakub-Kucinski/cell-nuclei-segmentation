from kedro.pipeline import Pipeline, node, pipeline

from .nodes import calc_metrics, make_predictions


def create_pipeline(**kwargs) -> Pipeline:
    """Function creating Model Evaluation pipeline.

    Returns:
        Pipeline: Created Model Evaluation pipeline.
    """
    return pipeline(
        [
            node(
                make_predictions,
                inputs=["StardistModelFineTuned", "test_data"],
                outputs=["Test_prediction", "Test_masks", "Test_details"],
                name="make_predictions",
            ),
            node(
                calc_metrics,
                inputs=[
                    "test_data",
                    "Test_prediction",
                    "Test_masks",
                    "params:EvaluationMetrics",
                ],
                outputs="metrics",
                name="calc_metrics",
            ),
        ],
        tags="model_validation",
    )
