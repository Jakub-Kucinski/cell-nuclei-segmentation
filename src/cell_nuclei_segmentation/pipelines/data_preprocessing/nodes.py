from typing import Dict, List

import cv2
from csbdeep.utils import normalize
from stardist import fill_label_holes


def preprocess_data(data: Dict, transformations: List) -> Dict:
    """Preprocess data with provided list of transforms.

    Args:
        data (Dict): Dataset.
        transformations (List): list of transformations

    Raises:
        ValueError: Transformation is a string different to `fill_label_holes`
        ValueError: Transformation is different than `normalize` and `rescale`

    Returns:
        Dict: Preprocessed data divided into images, masks and data frame
    """
    images_dict = data["images"]
    masks_dict = data["masks"]
    images_dict = {
        name: cv2.cvtColor(img, cv2.COLOR_RGB2GRAY) if len(img.shape) == 3 else img
        for name, img in images_dict.items()
    }
    df = data["df"]
    for transformation in transformations:
        if isinstance(transformation, str):
            if transformation == "fill_label_holes":
                for name, mask in masks_dict.items():
                    mask = fill_label_holes(mask)
                    masks_dict[name] = mask
            else:
                raise ValueError("Unknown transformation")
        elif isinstance(transformation, dict):
            transformation_name = next(iter(transformation))
            params = transformation[transformation_name]
            if transformation_name == "normalize":
                if isinstance(params, dict):
                    for name, img in images_dict.items():
                        img = normalize(img, **params)
                        images_dict[name] = img
                elif isinstance(params, list):
                    for name, img in images_dict.items():
                        img = normalize(img, *params)
                        images_dict[name] = img
            elif transformation_name == "rescale":
                for name, img in images_dict.items():
                    old_magnification = int(
                        df[df["name"] == name]["magnification"].values[0][:-1]
                    )
                    new_magnification = int(params["magnification"][:-1])
                    interpolation = (
                        getattr(cv2, params["interpolation"])
                        if "interpolation" in params
                        else cv2.INTER_LINEAR
                    )
                    img = cv2.resize(
                        img,
                        None,
                        fx=new_magnification / old_magnification,
                        fy=new_magnification / old_magnification,
                        interpolation=interpolation,
                    )
                    images_dict[name] = img
                for name, mask in masks_dict.items():
                    old_magnification = int(
                        df[df["name"] == name]["magnification"].values[0][:-1]
                    )
                    new_magnification = int(params["magnification"][:-1])
                    interpolation = (
                        getattr(cv2, params["interpolation"])
                        if "interpolation" in params
                        else cv2.INTER_LINEAR
                    )
                    mask = cv2.resize(
                        mask,
                        None,
                        fx=new_magnification / old_magnification,
                        fy=new_magnification / old_magnification,
                        interpolation=interpolation,
                    )
                    masks_dict[name] = mask
            else:
                raise ValueError("Unknown transformation")
    return {"images": images_dict, "masks": masks_dict, "df": df}


def get_train_test_data_and_params(data: Dict, params: Dict) -> Dict:
    """Method returning train and tests sets with their parameters.

    Args:
        data (Dict): Dataset.
        params (Dict): Preprocessing parameters.

    Returns:
        train_preprocessing_params: Train preprocessing parameters.
        train_data: Train data.
        test_preprocessing_params: Test preprocessing parameters.
        test_data: Test data.
    """
    train_preprocessing_params = params["train"]
    test_preprocessing_params = params["test"]
    train_data = data["train"]
    test_data = data["test"]
    return train_preprocessing_params, train_data, test_preprocessing_params, test_data
