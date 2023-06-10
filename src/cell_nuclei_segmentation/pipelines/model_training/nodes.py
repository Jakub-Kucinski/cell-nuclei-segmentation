from typing import Dict

from stardist import gputools_available
from stardist.models import Config2D, StarDist2D

from src.cell_nuclei_segmentation.pipelines.data_augmentations.nodes import Augmenter


def create_config(config_params: Dict) -> Config2D:
    """Create a StarDist config object from a dictionary of parameters.

    Args:
        config_params: Dictionary of parameters to be used to create the config object.

    Returns:
        A StarDist config object (Config2D).
    """
    if "use_gpu" in config_params and config_params["use_gpu"] is True:
        if not gputools_available():
            raise RuntimeError(
                "GPU or gputools not available, cannot use use_gpu=True."
            )
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
            model_config["name"], basedir="data/06_models"
        )
    else:
        name = model_config["name"] if "name" in model_config else "stardist"
        model = StarDist2D(config, name=name, basedir="data/06_models")
    return model


def train_model(
    model: StarDist2D, train_data: Dict, augmenter: Augmenter, model_config: Dict
) -> StarDist2D:
    """Train a StarDist model object from a config object.

    Args:
        model: A StarDist model object (StarDist2D).
        train_data: A StarDist data object (StarDistData2D) for training.
        augmenter: An augmenter object (Augmenter) for data augmentation.
        model_config: Dictionary of parameters to be used to train the model object.

    Returns:
        A StarDist model object (StarDist2D).
    """
    if "finetune" in model_config and model_config["finetune"] is True:
        model.train(train_data["images"], train_data["masks"], augmenter=augmenter)
    return model
