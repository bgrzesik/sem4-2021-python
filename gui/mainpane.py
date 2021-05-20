from gi.repository import Gtk, GdkPixbuf

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
        self.grayscale_image: Gtk.Image = \
            window.builder.get_object("src-grayscale")

        self.src_pixbuf = None
        self.grayscale_pixbuf = None
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
            grayscale = cv2.cvtColor(self.ctx.processor.gray, cv2.COLOR_GRAY2RGB)
            self.src_pixbuf = self.to_pixbuf(img)
            self.src_image.set_from_pixbuf(self.src_pixbuf)
            self.grayscale_pixbuf = self.to_pixbuf(grayscale)
            self.grayscale_image.set_from_pixbuf(self.grayscale_pixbuf)

        if self.ctx.regions is not None:
            img = cv2.cvtColor(self.ctx.regions, cv2.COLOR_BGR2RGB)
            self.regions_pixbuf = self.to_pixbuf(img)
            self.regions_image.set_from_pixbuf(self.regions_pixbuf)

        if self.ctx.dest is not None:
            img = cv2.cvtColor(self.ctx.dest, cv2.COLOR_GRAY2RGB)
            self.dest_pixbuf = self.to_pixbuf(img)
            self.dest_image.set_from_pixbuf(self.dest_pixbuf)
