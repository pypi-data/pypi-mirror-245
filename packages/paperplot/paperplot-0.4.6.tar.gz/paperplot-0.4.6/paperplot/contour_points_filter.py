import numpy as np
from ._data_filter_base import DataFilterBase


class ContourPointsFilter(DataFilterBase):
    def __init__(self):
        super().__init__()


    def filter(self):
        return self._data[:, 0], self._data[:, 1], self._data[:, 3]

