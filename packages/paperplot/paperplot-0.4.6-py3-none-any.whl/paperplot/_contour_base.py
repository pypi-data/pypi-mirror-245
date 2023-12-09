from ._figure_base import FigureBase


class ContourBase(FigureBase):
    def __init__(self, fig=None, figsize=(7, 7)):
        super().__init__(fig, figsize)

        # Members.
        self._caxes = None
        self._cbar = None
        self._cmap = "coolwarm"
        self._contour = None

    def remove_color_axes_outline(self):
        self._cbar.outline.set_edgecolor("none")

    def set_caxes(self, title=None, lim=None, ticks=None):
        if title is not None:
            self._cbar.ax.set_title(title, loc="center")

        if lim is not None:
            self._cbar.ax.set_ylim(lim)
            self._contour.set_clim(lim)

        if ticks is not None:
            self._cbar.set_ticks(ticks)

    def set_cmap(self, name):
        self._cmap = name

    def _add_color_axes(self):
        axes_pos = self._axes.get_position()
        self._caxes = self._fig.add_axes([axes_pos.x1 + 0.02, axes_pos.y0, 0.02, axes_pos.height])
        self._cbar = self._fig.colorbar(self._contour, cax=self._caxes, orientation='vertical')
