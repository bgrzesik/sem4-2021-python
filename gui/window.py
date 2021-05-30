import gi

gi.require_version("Gtk", "3.0")

from gi.repository import Gtk

from gui.mainpane import MainPane
from gui.toolbar import Toolbar
from gui.plots import Plots
from gui.menu import Menu
from gui.handler_find import HandlerFinder
from context import Context


class MainWindow(object):

    def __init__(self):
        pass

    def start(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("./gui/main_window.glade")
        self.window: Gtk.Widget = self.builder.get_object("main-window")

        self.ctx = Context(self.post_process)

        self.main_pane = MainPane(self, self.ctx)
        self.menu = Menu(self, self.ctx)
        self.toolbar = Toolbar(self, self.ctx)
        self.plots = Plots(self, self.ctx)

        self.builder.connect_signals(HandlerFinder([self.main_pane, self.menu, self.toolbar, self.plots, self]))
        self.window.connect("destroy", self.on_destroy)
        self.window.show_all()

        Gtk.main()


    def post_process(self):
        self.toolbar.refresh_ranges()
        self.main_pane.update()
        # self.plots.update()

    def on_destroy(self, *args):
        Gtk.main_quit()
