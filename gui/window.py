import gi

gi.require_version("Gtk", "3.0")

from gi.repository import Gtk

from gui.mainpane import MainPane
from gui.toolbar import Toolbar
from gui.plots import Plots


class MainWindow(object):

    def __init__(self):
        pass

    def start(self):

        self.builder = Gtk.Builder()
        self.builder.add_from_file("./gui/main_window.glade")
        self.window: Gtk.Widget = self.builder.get_object("main-window")

        self.main_pane = MainPane(self)
        self.toolbar = Toolbar(self)
        self.plots = Plots(self)

        self.window.connect("destroy", self.on_destroy)
        self.window.show_all()

        Gtk.main()

    def on_destroy(self, *args):
        Gtk.main_quit()
