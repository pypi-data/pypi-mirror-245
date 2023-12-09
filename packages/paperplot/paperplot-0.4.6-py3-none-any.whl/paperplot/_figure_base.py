import matplotlib as mpl
import matplotlib.pyplot as plt


class FigureBase:
    def __init__(self, figure=None, figsize=(7, 7)):
        # initialization
        if figure:
            if not isinstance(figure, FigureBase):
                raise TypeError("The input figure must be a type of 'FigureBase'.")

            self._fig = figure.get_fig()
            self._axes = figure.get_axes()
        else:
            self._fig = plt.figure(figsize=figsize)
            self._axes = self._fig.add_subplot()

    def add_minor_ticks(self):
        self._axes.minorticks_on()

    def get_fig(self):
        return self._fig

    def get_axes(self):
        return self._axes

    def remove_axes(self):
        self._axes.axis("Off")

    def remove_axes_outline(self):
        self._axes.spines['top'].set_visible(False)
        self._axes.spines['right'].set_visible(False)
        self._axes.spines['left'].set_visible(False)
        self._axes.spines['bottom'].set_visible(False)

    def save_fig(self, filename, dpi):
        self._fig.savefig(filename, dpi=dpi)

    def set_content_margin(self, left, bottom, right, top):
        self._fig.subplots_adjust(left, bottom, right, top)

    def set_xaxis(self, label=None, lim=None, labelpad=None):
        if label is not None:
            if not isinstance(label, str):
                raise TypeError("The label type is not 'str'.")
            else:
                self._axes.set_xlabel(label)

        if lim is not None:
            self._axes.set_xlim(lim)

        if labelpad is not None:
            self._axes.xaxis.labelpad = labelpad

    def set_xticks(self, ticks=None, direction=None):
        if ticks is not None:
            self._axes.xaxis.set_ticks(ticks)

        if direction is not None:
            self._axes.tick_params(axis="x", direction=direction, which="both")

    def set_yaxis(self, label=None, lim=None, labelpad=None):
        if label is not None:
            if not isinstance(label, str):
                raise TypeError("The label type is not 'str'.")
            else:
                self._axes.set_ylabel(label)
        if lim is not None:
            self._axes.set_ylim(lim)

        if labelpad is not None:
            self._axes.yaxis.labelpad = labelpad

    def set_yticks(self, ticks=None, direction=None):
        if ticks is not None:
            self._axes.yaxis.set_ticks(ticks)

        if direction is not None:
            self._axes.tick_params(axis="y", direction=direction, which="both")

    def show_fig(self):
        plt.show()
