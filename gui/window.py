import gi

gi.require_version("Gtk", "3.0")

from gi.repository import Gtk

from gui.mainpane import MainPane
from gui.toolbar import Toolbar
from gui.plots import Plots

from context import Context


class MainWindow(object):

    def __init__(self):
        pass

    def start(self):

        self.builder = Gtk.Builder()
        self.builder.add_from_file("./gui/main_window.glade")
        self.window: Gtk.Widget = self.builder.get_object("main-window")

        self.ctx = Context()

        self.main_pane = MainPane(self, self.ctx)
        self.toolbar = Toolbar(self, self.ctx)
        self.plots = Plots(self, self.ctx)

        self.window.connect("destroy", self.on_destroy)
        self.window.show_all()

        self.ctx.select_img("./proto/eg/0.jpg")
        self.update()

        Gtk.main()

    def update(self):
        print(self.ctx.processor.settings)
        self.ctx.process()
        self.main_pane.update()
        self.plots.update()

    def on_destroy(self, *args):
        Gtk.main_quit()
