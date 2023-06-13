import os
from pathlib import PurePosixPath

import fsspec
import numpy as np
import pandas as pd
from kedro.io import AbstractDataSet
from kedro.io.core import get_filepath_str, get_protocol_and_path
from stardist.models import StarDist2D


class StardistModel(AbstractDataSet):
    """``StardistModel`` class for loading and saving Stardist model
    in Kedro data catalog."""

    def __init__(self, path):
        protocol, path = get_protocol_and_path(path)
        self._protocol = protocol
        self._path = PurePosixPath(path)
        self._fs = fsspec.filesystem(self._protocol)

    def _load(self):
        # at the beginning of the node
        model = StarDist2D(None, name=self.name, basedir=str(self._path))

    def _save(self, model):
        # at the end of the node
        self.logdir = model.logdir
        self.name = model.name
        os.system(f"cp -r {str(model.logdir)} {str(self._path)}")

    def _describe(self):
        return dict(filepath=self._path, protocol=self._protocol)
