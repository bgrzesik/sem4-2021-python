
from gi.repository import Gtk, GdkPixbuf


class MainPane(object):

    def __init__(self, window: "MainWindow"):

        self.image: Gtk.Image = window.builder.get_object("main-image")
        self.pixbuf: GdkPixbuf.Pixbuf = GdkPixbuf.Pixbuf.new_from_file(
            "./proto/eg/0.jpg")

        self.image.set_from_pixbuf(self.pixbuf)
