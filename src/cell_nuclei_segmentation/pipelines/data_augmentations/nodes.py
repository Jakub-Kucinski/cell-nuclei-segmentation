from typing import Tuple

import numpy as np


class Augmenter:
    """Augmenter class for augmenting images and masks."""

    def __init__(self, augmentation_config: dict):
        """Initialize Augmenter class.

        Args:
            probability: Probability of applying augmentation.
        """
        self.augmentation_config = augmentation_config

    def random_flip(
        self, img: np.ndarray, mask: np.ndarray, probability: float = 0.5
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Randomly flip image and mask horizontally or vertically.

        Args:
            img: Image to be flipped.
            mask: Mask to be flipped.

        Returns:
            Tuple of flipped image and mask in the same orientation.
        """
        if np.random.rand() < probability:
            img = np.flip(img, axis=0)
            mask = np.flip(mask, axis=0)

        if np.random.rand() < probability:
            img = np.flip(img, axis=1)
            mask = np.flip(mask, axis=1)

        return img, mask

    def random_rotate(
        self, img: np.ndarray, mask: np.ndarray, probability: float = 0.5
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Randomly rotate image and mask.

        Args:
            img: Image to be rotated.
            mask: Mask to be rotated.

        Returns:
            Tuple of rotated image and mask in the same orientation.
        """
        if np.random.rand() < probability:
            axes = tuple(range(mask.ndim))
            perm = tuple(np.random.permutation(axes))
            img = img.transpose(perm + tuple(range(mask.ndim, img.ndim)))
            mask = mask.transpose(perm)

        return img, mask

    def random_intensity_change(
        self,
        img: np.ndarray,
        mask: np.ndarray,
        img_intensity_scale_range: Tuple[float, float] = (0.6, 2.0),
        img_intensity_bias_range: Tuple[float, float] = (-0.2, 2.0),
    ) -> Tuple[np.ndarray, np.ndarray]:
        img = img * np.random.uniform(*img_intensity_scale_range) + np.random.uniform(
            *img_intensity_bias_range
        )
        return img, mask

    def __call__(
        self, img: np.ndarray, mask: np.ndarray
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Apply augmentations to image and mask.

        Args:
            img: Image to be augmented.
            mask: Mask to be augmented.

        Returns:
            Tuple of augmented image and mask.
        """
        for augmentation in self.augmentation_config:
            if isinstance(augmentation, str):
                img, mask = getattr(self, augmentation)(img, mask)
            elif isinstance(augmentation, dict):
                augmentation_name = next(iter(augmentation))
                augmentation_method = getattr(self, augmentation_name)
                params = augmentation[augmentation_name]
                if isinstance(params, dict):
                    img, mask = augmentation_method(img, mask, **params)
                elif isinstance(params, list):
                    img, mask = augmentation_method(img, mask, *params)

        return img, mask


def create_augmenter(augmentation_config: dict) -> Augmenter:
    """Create augmenter function.

    Args:
        probability: Probability of applying augmentation.

    Returns:
        Augmenter function.
    """
    return Augmenter(augmentation_config)
