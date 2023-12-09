import numpy as np
from scipy.interpolate import griddata
from ._data_filter_base import DataFilterBase


class ContourGridFilter(DataFilterBase):
    def __init__(self):
        super().__init__()

    def filter(self, x_params, y_params):
        x = self._data[:, 0]
        y = self._data[:, 1]
        z = self._data[:, 3]
        xi = np.linspace(x_params[0], x_params[1], x_params[2])
        yi = np.linspace(y_params[0], y_params[1], y_params[2])
        Xi, Yi = np.meshgrid(xi, yi)
        Zi = griddata((x, y), z, (Xi, Yi), method="cubic")

        return Xi, Yi, Zi
