from typing import Dict

from stardist.models import Config2D, StarDist2D

from cell_nuclei_segmentation.extras.datasets.stardist_model import StardistModel
from cell_nuclei_segmentation.pipelines.data_augmentations.nodes import Augmenter


def create_config(config_params: Dict) -> Config2D:
    """Create a StarDist config object from a dictionary of parameters.

    Args:
        config_params: Dictionary of parameters to be used to create the config object.

    Returns:
        A StarDist config object (Config2D).
    """
    return Config2D(**config_params)


def create_model(config: Config2D, model_config: Dict) -> StarDist2D:
    """Create a StarDist model object from a config object.

    Args:
        config: A StarDist config object (Config2D).
        model_config: Dictionary of parameters to be used to create the model object.

    Returns:
        A StarDist model object (StarDist2D).
    """
    if "pretrained" in model_config and model_config["pretrained"] is True:
        if "name" not in model_config:
            raise RuntimeError("Pretrained model requires a name to be specified.")
        model = StarDist2D.from_pretrained(
            model_config["name"],
        )
    else:
        raise NotImplementedError
    return model


def model_training(
    model: StardistModel, train_data: Dict, augmenter: Augmenter, training_params: Dict
):
    """Train the StarDist model.

    Args:
        model: A StarDist model object (StardistModel).
        train_data: Training data.

    Returns:
        None
    """
    image_names = train_data["images"].keys()
    X_train = [train_data["images"][img_name] for img_name in image_names]
    Y_train = [train_data["masks"][img_name] for img_name in image_names]
    model.train(
        X_train,
        Y_train,
        validation_data=(X_train, Y_train),
        **training_params,
        augmenter=augmenter
    )
    return model


def treshold_optimization(model: StardistModel, train_data: Dict, test_data: Dict):
    """Optimize the treshold for the StarDist model.

    Args:
        model: A StarDist model object (StardistModel).
        train_data: Training data.
        test_data: Test data.

    Returns:
        None
    """
    image_names = train_data["images"].keys()
    X_val = [train_data["images"][img_name] for img_name in image_names]
    Y_val = [train_data["masks"][img_name] for img_name in image_names]
    optimized_tresholds = model.optimize_thresholds(X_val, Y_val)
    return optimized_tresholds
