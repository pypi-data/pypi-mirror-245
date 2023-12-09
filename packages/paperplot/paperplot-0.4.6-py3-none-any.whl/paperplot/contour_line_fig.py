import numpy as np
from ._contour_base import ContourBase


class ContourLineFig(ContourBase):
    def __init__(self, fig=None, figsize=(7, 7)):
        super().__init__(fig, figsize=figsize)

    def set_grid_data(self, X, Y, Z, value):
        self._axes.contour(X, Y, Z, levels=[value], colors="#7CFC00", linewidths=1.5)
