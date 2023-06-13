from typing import Dict

from stardist import gputools_available
from stardist.models import Config2D, StarDist2D

from cell_nuclei_segmentation.pipelines.data_augmentations.nodes import Augmenter
from cell_nuclei_segmentation.extras.datasets.stardist_model import StardistModel


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


def test_model(
    model: StardistModel
):
    return