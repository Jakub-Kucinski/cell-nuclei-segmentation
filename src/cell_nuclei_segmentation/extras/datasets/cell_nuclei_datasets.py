import os
from pathlib import PurePosixPath

import fsspec
from kedro.io import AbstractDataSet
from kedro.io.core import get_filepath_str, get_protocol_and_path


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
        return set()

    def _save(self, data):
        def unzip_and_clean(save_path):
            os.system(
                "unzip -q " + save_path + "/dataset.zip -d " + save_path + "/dataset"
            )
            os.system("rm " + save_path + "/dataset.zip")

        def website_download(save_path):
            os.system("wget " + self.url + " -P " + save_path)
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
