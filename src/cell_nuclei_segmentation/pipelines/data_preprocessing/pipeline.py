from kedro.pipeline import Pipeline, node, pipeline

from .nodes import get_train_test_data_and_params, preprocess_data


def create_pipeline(**kwargs) -> Pipeline:
    """Function creating Data Processing pipeline.

    Returns:
        Pipeline: Created Data Processing pipeline.
    """
    return pipeline(
        [
            node(
                func=get_train_test_data_and_params,
                inputs=["CellNucleiRaw", "params:preprocessing"],
                outputs=[
                    "train_preprocessing_params",
                    "train_data_raw",
                    "test_preprocessing_params",
                    "test_data_raw",
                ],
                name="data_preprocessing",
            ),
            node(
                func=preprocess_data,
                inputs=["train_data_raw", "train_preprocessing_params"],
                outputs="train_data",
                name="train_data_preprocessing",
            ),
            node(
                func=preprocess_data,
                inputs=["test_data_raw", "test_preprocessing_params"],
                outputs="test_data",
                name="test_data_preprocessing",
            ),
        ],
        tags=["model_validation", "results_visualization"],
    )
