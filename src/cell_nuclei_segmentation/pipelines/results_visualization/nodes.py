from typing import Dict, List

import matplotlib.pyplot as plt
from stardist import _draw_polygons, random_label_cmap

from cell_nuclei_segmentation.extras.datasets.stardist_model import StardistModel


def predict(model: StardistModel, test_data: Dict, image_names: List) -> List:
    """Make predictions using the StarDist model.

    Args:
        model: A StarDist model object (StardistModel).
        test_data: Test data.

    Returns:
        A tuple of dictionaries containing the predictions and the ground truth.
    """
    images = [test_data["images"][image_name] for image_name in image_names]
    predictions = [model.predict_instances(image) for image in images]
    return predictions


def _example(labels, details, img, file_name, lbl_cmap, show_dist=True):
    plt.figure(figsize=(13, 10))
    img_show = img if img.ndim == 2 else img[..., 0]
    coord, points, prob = details["coord"], details["points"], details["prob"]
    plt.subplot(121)
    plt.imshow(img_show, cmap="gray")
    plt.axis("off")
    a = plt.axis()
    _draw_polygons(coord, points, prob, show_dist=show_dist)
    plt.axis(a)
    plt.subplot(122)
    plt.imshow(img_show, cmap="gray")
    plt.axis("off")
    plt.imshow(labels, cmap=lbl_cmap, alpha=0.5)
    plt.tight_layout()
    plt.savefig(file_name)


def create_images(
    predictions: List,
    test_data: Dict,
    image_names: List,
) -> Dict:
    """Plot predictions and save the images.

    Args:
        predictions (List): model predictions.
        test_data (Dict): Test data provided to the model.
        image_names (List): Names of the tests images.

    Returns:
        Dict:
    """
    lbl_cmap = random_label_cmap()
    for (labels, details), image_name in zip(predictions, image_names):
        _example(
            labels,
            details,
            test_data["images"][image_name],
            f"data/08_reporting/imgs/{image_name}.png",
            lbl_cmap,
        )
    return
