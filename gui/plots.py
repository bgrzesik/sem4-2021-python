
from gi.repository import Gtk, Gdk, GdkPixbuf


from matplotlib.backends.backend_gtk3agg import (
    FigureCanvasGTK3Agg as FigureCanvas)

from matplotlib.figure import Figure

import numpy as np


class Plots(object):

    def __init__(self, window: "MainWindow"):
        self.frame: Gtk.ScrolledWindow = window.builder.get_object("figure")

        self.fig = Figure(figsize=(2, 2), dpi=100)
        self.ax = self.fig.add_subplot()

        x = np.linspace(0, 2 * np.pi, 100)
        y = np.sin(x)

        self.ax.plot(x, y)

        self.canvas = FigureCanvas(self.fig)
        self.canvas.set_size_request(100, 100)
        self.frame.add_with_viewport(self.canvas)
