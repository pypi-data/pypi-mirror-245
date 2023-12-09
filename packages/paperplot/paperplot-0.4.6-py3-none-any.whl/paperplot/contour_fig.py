import numpy as np
from ._contour_base import ContourBase


class ContourFig(ContourBase):
    def __init__(self, figsize=(7, 7)):
        super().__init__(figsize=figsize)

        # Control parameters.
        self._level_num = 900

    def set_grid_data(self, X, Y, Z, cbar=True):
        # Draw the contour.
        self._contour = self._axes.contourf(X, Y, Z, self._level_num, cmap=self._cmap)

        # Because the color bar needs to get the contour axes position, so it must be called after the draw code.
        if cbar:
            self._add_color_axes()

    def set_points_data(self, x, y, z, cbar=True):
        # Draw the contour.
        self._contour = self._axes.tricontourf(x, y, z, cmap=self._cmap)

        # Because the color bar needs to get the contour axes position, so it must be called after the draw code.\
        if cbar:
            self._add_color_axes()

    def set_level_num(self, num):
        self._level_num = num
