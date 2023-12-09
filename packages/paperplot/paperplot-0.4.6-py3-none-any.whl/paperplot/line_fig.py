from ._figure_base import FigureBase
from .line_style import AbstractLineStyle


class LineFig(FigureBase):
    def __init__(self, fig=None, figsize=(7, 7)):
        super().__init__(fig, figsize)

        # initialize
        self._axes.minorticks_on()

    def add_background_grid(self):
        self._axes.grid(color=(235/255, 235/255, 235/255))

    def add_line(self, x, y, style, label=None):
        # check
        if not isinstance(style, AbstractLineStyle):
            raise TypeError("The input style is not a type of 'LineStyle'.")

        # add
        line, = self._axes.plot(x, y)
        style.decorate_line(line)

        if label is not None: line.set_label(label)

    def add_legend(self, loc=(0.5, 0.5), cols=1, cspacing=0, rspacing=0.5, pad=0.4):
        self._axes.legend(loc=loc, ncol=cols, columnspacing=cspacing, labelspacing=rspacing, borderpad=pad)
