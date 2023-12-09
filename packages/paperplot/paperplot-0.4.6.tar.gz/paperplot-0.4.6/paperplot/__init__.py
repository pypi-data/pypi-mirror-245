import matplotlib as mpl
from .contour_fig import ContourFig
from .contour_grid_filter import ContourGridFilter
from .contour_line_fig import ContourLineFig
from .contour_points_filter import ContourPointsFilter
from .line_fig import LineFig
from .line_style import LineStyle
from .mesh_fig import MeshFig
from .pixel_contour_fig import PixelContourFig
from .pixel_grid_filter import PixelGridFilter

# Set the global font to 1.
mpl.rcParams["font.family"] = ["Times New Roman"]
# Set the global font size to 20.
mpl.rcParams["font.size"] = 20
# Set the global math font to stix.
mpl.rcParams["mathtext.fontset"] = "stix"
# Set automatic round numbers.
mpl.rcParams["axes.autolimit_mode"] = "round_numbers"
