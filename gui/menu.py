import gi
from gi.repository import Gtk, GdkPixbuf

from context import Context
import os
import json
import dataclasses
from processor import ImageProcessorSettings, OtsuRange


class Menu(object):

    def __init__(self, window: "MainWindow", ctx: "Context"):
        self.window = window
        self.context = ctx

        self.accepted_extensions = [".jpg", ".jpeg", ".png", ".tif", ".tiff"]

        self.view_stack: Gtk.Stack = \
            window.builder.get_object("stack1")

    def switch_page(self, child):
        self.view_stack.set_visible_child(child)

    def open_range(self, *args):
        if self.context.image_loaded():
            self.open_file_dialog(self.add_json_filter, self.open_json_file)

    def save_range(self, *args):
        if self.context.image_loaded():
            self.file_save_dialog(self.validate_json_name, self.save_json_file, self.add_json_filter)

    def open_file(self, *args):
        self.open_file_dialog(self.add_image_filters, self.open_file_response)

    def open_file_response(self, path):
        self.context.select_img(path)
        self.window.update_plots = True
        with self.context.change_settings() as settings:
            settings.clear_ranges()
        self.window.toolbar.clear_selected()
        self.window.toolbar.update_toolbar()

    def save_file(self, *args):
        if self.context.image_loaded():
            result = self.context.file_name
            result = result.split(".")

            result[-2] += "_out"
            result = '.'.join(result)
            print(result)
            self.context.save_img(result)

    def save_file_as(self, *args):
        if self.context.image_loaded():
            self.file_save_dialog(self.validate_image_name, self.context.save_img, self.add_image_filters)

    def info_popup(self, *args):
        dialog = Gtk.MessageDialog(parent=None, buttons=Gtk.ButtonsType.OK,
                                   message_format="Program powstał w ramach realizacji projektu z języka Python. "
                                                  "Autorami są Bartłomiej Grzesik oraz Władysław Cholewa")

        dialog.connect("response", self.dialog_response)
        dialog.show()

    def dialog_response(self, widget, response_id):
        widget.destroy()

    def add_image_filters(self, dialog):
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

    def add_json_filter(self, dialog):
        filter_json = Gtk.FileFilter()
        filter_json.set_name("JSON files")
        filter_json.add_mime_type("application/json")
        dialog.add_filter(filter_json)

    def validate_image_name(self, file_text):
        rfind_result = file_text.rfind(".")
        return rfind_result != -1 and file_text[rfind_result:] in self.accepted_extensions

    def validate_json_name(self, file_text):
        rfind_result = file_text.rfind(".")
        return rfind_result != -1 and file_text[file_text.rfind("."):] == ".json"

    def save_json_file(self, path):
        with open(path, "w") as file:
            settings = dataclasses.asdict(self.context.settings)
            json.dump(settings, file)

    def open_json_file(self, path):
        with open(path, "r") as file:
            loaded = json.load(file)

            ranges = []
            for rang in loaded["ranges"]:
                ranges.append(OtsuRange(**rang))

            loaded["ranges"] = ranges

            with self.context.change_settings() as settings:
                for field, value in loaded.items():
                    setattr(settings, field, value)

            print(self.context.settings)
            self.window.toolbar.update_toolbar()

    def file_save_dialog(self, validation_function, creator_function, filter_adder):
        dialog = Gtk.FileChooserDialog(
            title="Please choose a file",
            transient_for=self.window.window,
            action=Gtk.FileChooserAction.SAVE,
        )
        dialog.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_SAVE, Gtk.ResponseType.OK
        )
        filter_adder(dialog)
        dialog.set_default_size(800, 400)

        response = dialog.run()
        if response == Gtk.ResponseType.OK and validation_function(dialog.get_filename()):
            creator_function(dialog.get_filename())
        elif response == Gtk.ResponseType.OK:
            filter_name = dialog.get_filter().get_name()
            extension_binding = {"JPEG files": ".jpg", "PNG files": ".png", "TIFF files": ".tiff",
                                 "JSON files": ".json"}
            creator_function(dialog.get_filename() + extension_binding[filter_name])
        elif response == Gtk.ResponseType.CANCEL:
            pass

        dialog.destroy()

    def open_file_dialog(self, filter_adder, response_function):
        dialog = Gtk.FileChooserDialog(
            title="Please choose a file", transient_for=self.window.window, action=Gtk.FileChooserAction.OPEN
        )
        dialog.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN,
            Gtk.ResponseType.OK,
        )

        filter_adder(dialog)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            response_function(dialog.get_filename())

        elif response == Gtk.ResponseType.CANCEL:
            pass

        dialog.destroy()
