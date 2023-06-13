import os
from pathlib import PurePosixPath

import fsspec
import numpy as np
import pandas as pd
from kedro.io import AbstractDataSet
from kedro.io.core import get_filepath_str, get_protocol_and_path
from PIL import Image
import wget
import zipfile


class CellNucleiRawDataset(AbstractDataSet):
    """``CellNucleiRawDataset`` class for loading and saving CellNucleiRaw dataset
    in Kedro data catalog."""

    def __init__(self, path, save_args):
        protocol, path = get_protocol_and_path(path)
        self._protocol = protocol
        self._path = PurePosixPath(path)
        self._fs = fsspec.filesystem(self._protocol)
        self.supported_clouds = ["aws"]
        self.download_source = save_args["source"]
        self.url = save_args["url"] if "url" in save_args else None

    def _load(self):
        def load_images(image_folder_path, df):
            images = dict()
            for image_name in df["Image_Name"].values:
                image_path = image_folder_path / f"{image_name}.tif"
                image = Image.open(str(image_path))
                image = np.array(image)
                images[image_name] = image
            return images

        df = pd.read_csv(self._fs.open(self._path / "image_description.csv"), sep=";")
        train_df = df[df["Train-/Testset split"] == "train"]
        test_df = df[df["Train-/Testset split"] == "test"]
        train_df = train_df.reset_index(drop=True)
        test_df = test_df.reset_index(drop=True)
        train_images = load_images(self._path / "rawimages", train_df)
        test_images = load_images(self._path / "rawimages", test_df)
        train_masks = load_images(self._path / "groundtruth", train_df)
        test_masks = load_images(self._path / "groundtruth", test_df)
        data = dict(
            train=dict(images=train_images, masks=train_masks, df=train_df),
            test=dict(images=test_images, masks=test_masks, df=test_df),
        )
        return data

    def _save(self, data):
        def unzip_and_clean(save_path):
            with zipfile.ZipFile(save_path + "/dataset.zip", "r") as zip_ref:
                zip_ref.extractall(save_path + "/dataset")
            os.remove(save_path + "/dataset.zip")

        def website_download(save_path):
            wget.download(self.url, out=save_path)
            unzip_and_clean(save_path)

        def aws_download(save_path):
            os.system("dvc pull")
            unzip_and_clean(save_path)

        def cloud_download(cloud, save_path):
            if cloud == "aws":
                aws_download(save_path)

        save_path = get_filepath_str(self._path.parent, self._protocol)
        files = os.listdir(save_path)
        if "dataset" in files:
            print("Files already downloaded")
        elif self.download_source == "website":
            if self.url is None:
                raise Exception("Selected download from website, but no url provided.")
            website_download(save_path)
        else:
            if self.download_source in self.supported_clouds:
                cloud_download(self.download_source, save_path)
            else:
                raise Exception(
                    f"Selected download from cloud, but provided cloud name is not "
                    f"supported.\nList of supported clouds: {self.supported_clouds}"
                )

    def _describe(self):
        return dict(filepath=self._path, protocol=self._protocol)
