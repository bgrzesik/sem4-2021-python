
from gi.repository import Gtk, Gdk, GdkPixbuf

from processor import ImageProcessor
import cv2


class MainPane(object):

    def __init__(self, window: "MainWindow", ctx: "Context"):

        self.ctx = ctx

        self.src_image: Gtk.Image = \
            window.builder.get_object("src-image")
        self.dest_image: Gtk.Image = \
            window.builder.get_object("dest-image")
        self.regions_image: Gtk.Image = \
            window.builder.get_object("regions-image")

        self.src_pixbuf = None
        self.dest_pixbuf = None
        self.regions_pixbuf = None

    def to_pixbuf(self, img):
        return GdkPixbuf.Pixbuf.new_from_data(
            img.tostring(),
            GdkPixbuf.Colorspace.RGB, False, 8,
            img.shape[1], img.shape[0],
            img.shape[2] * img.shape[1])

    def update(self):
        if self.ctx.img is not None:
            img = cv2.cvtColor(self.ctx.img, cv2.COLOR_BGR2RGB)
            self.src_pixbuf = self.to_pixbuf(img)
            self.src_image.set_from_pixbuf(self.src_pixbuf)

        if self.ctx.dest is not None:
            img = cv2.cvtColor(self.ctx.dest, cv2.COLOR_GRAY2RGB)
            self.dest_pixbuf = self.to_pixbuf(img)
            self.dest_image.set_from_pixbuf(self.dest_pixbuf)
