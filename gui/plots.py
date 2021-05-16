
import numpy as np
from gi.repository import Gtk
from matplotlib.backends.backend_gtk3agg import (
    FigureCanvasGTK3Agg as FigureCanvas)
from matplotlib.figure import Figure
import cv2


class Plots(object):

    def __init__(self, window: "MainWindow", ctx: "Context"):
        self.ctx = ctx
        self.frame: Gtk.ScrolledWindow = window.builder.get_object("figure")

        self.fig = Figure(figsize=(2, 2), dpi=100)
        self.ax = self.fig.add_subplot()

        self.canvas = FigureCanvas(self.fig)
        self.canvas.set_size_request(100, 100)
        self.frame.add_with_viewport(self.canvas)

    def update(self):
        dest = cv2.cvtColor(self.ctx.img, cv2.COLOR_RGB2GRAY)

        self.ax.clear()

        x = np.arange(256)
        y, x = np.histogram(dest, x)
        self.ax.hist(x[:-1],x,weights=y)
        self.canvas.draw()

