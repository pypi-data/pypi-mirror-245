import matplotlib.cm as cm
import matplotlib.colors as mcolors
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
from ._contour_base import ContourBase


class PixelContourFig(ContourBase):
    def __init__(self, fig=None, figsize=(7, 7)):
        super().__init__(fig, figsize)

    def set_grid_data(self, X, Y, Z, cbar=True):
        # Draw the pixel contour.
        self._contour = self._axes.pcolormesh(X, Y, Z, shading="flat", cmap="viridis")

        # Because the color bar needs to get the contour axes position, so it must be called after the draw code.
        if cbar:
            self._add_color_axes()

    def set_triangles_data(self, nodes, cells, scalars, cbar=True, clim=None):
        # Create a scalar mappable.
        v_min = 0
        v_max = 0
        if clim is None:
            v_min = np.min(scalars)
            v_max = np.max(scalars)
        else:
            v_min = clim[0]
            v_max = clim[1]
        self._contour = cm.ScalarMappable(cmap=plt.cm.viridis, norm=mcolors.Normalize(v_min, v_max))

        # Draw the pixel contour.
        for i, triangle in enumerate(cells):
            t_coords = np.array([[nodes[triangle[0]][0], nodes[triangle[0]][1]],
                                 [nodes[triangle[1]][0], nodes[triangle[1]][1]],
                                 [nodes[triangle[2]][0], nodes[triangle[2]][1]]])

            triangle_patch = patches.Polygon(t_coords, color=plt.cm.viridis((scalars[i]-v_min)/(v_max-v_min)))
            self._axes.add_patch(triangle_patch)

        # Change the limit of x and y axes.
        self.set_xaxis(lim=(np.min(nodes[:, 0]), np.max(nodes[:, 0])))
        self.set_yaxis(lim=(np.min(nodes[:, 1]), np.max(nodes[:, 1])))

        # Because the color bar needs to get the contour axes position, so it must be called after the draw code.
        if cbar:
            self._add_color_axes()
