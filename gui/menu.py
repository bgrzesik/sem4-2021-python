import gi
from gi.repository import Gtk, GdkPixbuf

gi.require_version("Gtk", "3.0")
import cv2
import os


class Menu(object):

    def __init__(self, window: "MainWindow", ctx: "Context"):
        self.window = window
        self.context = ctx

        self.accepted_extensions = ["jpg", "jpeg", "png", "tif", "tiff"]
        self.view_stack: Gtk.Stack= \
            window.builder.get_object("stack1")

    def switch_page(self,child):
        self.view_stack.set_visible_child(child)

    def open_file(self, *args):
        dialog = Gtk.FileChooserDialog(
            title="Please choose a file", parent=None, action=Gtk.FileChooserAction.OPEN
        )
        dialog.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN,
            Gtk.ResponseType.OK,
        )

        self.add_filters(dialog)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.context.select_img(dialog.get_filename())
            self.window.toolbar.refresh_ranges()
            self.window.update()

        elif response == Gtk.ResponseType.CANCEL:
            pass

        dialog.destroy()

    def save_file(self, *args):
        result = self.context.file_name
        result = result.split(".")

        result[-2] += "_out"
        result = '.'.join(result)
        print(result)
        cv2.imwrite(result, self.context.dest)

    def save_file_as(self, *args):
        dialog = Gtk.FileChooserDialog(
            title="Please choose a folder",
            parent=None,
            action=Gtk.FileChooserAction.SELECT_FOLDER,
        )
        dialog.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, "Select", Gtk.ResponseType.OK
        )
        dialog.set_default_size(800, 400)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:

            dialog_window = Gtk.MessageDialog(dialog, message_type=Gtk.MessageType.QUESTION,
                                              flags=Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT,
                                              buttons=Gtk.ButtonsType.OK_CANCEL,
                                              title="Podaj nazwę pliku")

            dialog_box = dialog_window.get_content_area()

            entry = Gtk.Entry()
            entry.set_text("Example.jpg")
            entry.set_size_request(250, 50)
            dialog_box.pack_end(entry, True, True, 0)
            dialog_window.show_all()
            entry_response = dialog_window.run()
            pureFile = entry.get_text()
            dialog_window.destroy()
            if entry_response == Gtk.ResponseType.OK and self.validate_text(pureFile):
                separator = "/"
                if os.name == "nt":
                    separator = "\\"
                cv2.imwrite(dialog.get_filename() + separator + pureFile, self.context.dest)
            else:
                pass
        elif response == Gtk.ResponseType.CANCEL:
            pass

        dialog.destroy()

    def info_popup(self, *args):
        dialog = Gtk.MessageDialog(buttons=Gtk.ButtonsType.OK,
                                   message_format="Program powstał w ramach realizacji projektu z języka Python. Autorami są Bartłomiej Grzesik oraz Władysław Cholewa")
        dialog.connect("response", self.dialog_response)
        dialog.show()

    def dialog_response(self, widget, response_id):
        widget.destroy()

    def add_filters(self, dialog):
        filter_jpg = Gtk.FileFilter()
        filter_jpg.set_name("JPEG files")
        filter_jpg.add_mime_type("image/jpeg")
        dialog.add_filter(filter_jpg)

        filter_py = Gtk.FileFilter()
        filter_py.set_name("PNG files")
        filter_py.add_mime_type("image/png")
        dialog.add_filter(filter_py)

        filter_any = Gtk.FileFilter()
        filter_any.set_name("TIFF files")
        filter_any.add_mime_type("image/tiff")
        dialog.add_filter(filter_any)

    def validate_text(self, file_text):
        splitted = file_text.split(".")
        return splitted[-1] in self.accepted_extensions
