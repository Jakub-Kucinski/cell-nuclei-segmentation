from operator import itemgetter
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
from stardist.matching import matching_dataset
from tqdm import tqdm

from cell_nuclei_segmentation.extras.datasets.stardist_model import StardistModel


def make_predictions(model: StardistModel, test_data: Dict) -> Tuple[Dict, Dict]:
    """Make predictions using the StarDist model.

    Args:
        model: A StarDist model object (StardistModel).
        test_data: Test data.

    Returns:
        A tuple of dictionaries containing the predictions and the ground truth.
    """
    image_names = test_data["images"].keys()
    X_test = [test_data["images"][img_name] for img_name in image_names]
    predictions = [model.predict_instances(img) for img in X_test]
    predicted_masks = [pred[0] for pred in predictions]
    predicted_details = [pred[1] for pred in predictions]
    return (
        {
            img_name: predicted_mask
            for img_name, predicted_mask in zip(image_names, predicted_masks)
        },
        test_data["masks"],
        predicted_details,
    )


def _average_precision(predictions: List, masks: List, tresholds: np.array) -> float:
    precisions = []
    recalls = []
    for treshold in tresholds:
        matching_results = matching_dataset(
            masks, predictions, thresh=treshold, show_progress=False
        )
        precisions.append(matching_results.precision)
        recalls.append(matching_results.recall)
    ap = 0
    for i in range(len(precisions) - 1):
        ap += precisions[i] * (recalls[i] - recalls[i + 1])
    return ap


def _mean_average_precision(
    predictions: Dict, true_masks: Dict, df: pd.DataFrame, n_tresholds: int
) -> Tuple[Dict, Dict]:
    ap_values = []
    for name, df_class in tqdm(df.groupby("Testset class")):
        preds = itemgetter(*df_class["Image_Name"].values)(predictions)
        masks = itemgetter(*df_class["Image_Name"].values)(true_masks)
        ap = _average_precision(preds, masks, np.linspace(0, 1, n_tresholds))
        ap_values.append(ap)
    return np.array(ap_values).mean()


def calc_metrics(
    model: StardistModel,
    test_data: Dict,
    predictions: Dict,
    masks: Dict,
    evaluation_metrics: Dict,
) -> Dict:
    """Calculate evaluation metrics.

    Args:
        predictions: A dictionary containing the predictions.
        masks: A dictionary containing the ground truth.
        evaluation_metrics: A list of evaluation metrics.

    Returns:
        A dictionary containing the evaluation metrics.
    """
    image_names = masks.keys()
    matching_results = matching_dataset(
        itemgetter(*image_names)(masks), itemgetter(*image_names)(predictions)
    )
    metrics = {}
    for metric in evaluation_metrics["names"]:
        if metric == "DiceCoefficient":
            metrics[metric] = matching_results.f1
        elif metric == "IntersectionOverUnion":
            metrics[metric] = matching_results.tp / (
                matching_results.tp + matching_results.fp + matching_results.fn
            )
        elif metric == "MeanAveragePrecision":
            metrics[metric] = _mean_average_precision(
                predictions, masks, test_data["df"], evaluation_metrics["n_tresholds"]
            )
    print(metrics)
    return metrics
