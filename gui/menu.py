import gi
from gi.repository import Gtk, GdkPixbuf

import os
from context import Context
import json

class Menu(object):

    def __init__(self, window: "MainWindow", ctx: "Context"):
        self.window = window
        self.context = ctx

        self.accepted_extensions = ["jpg", "jpeg", "png", "tif", "tiff"]
        self.view_stack: Gtk.Stack= \
            window.builder.get_object("stack1")

    def switch_page(self,child):
        self.view_stack.set_visible_child(child)

    def open_range(self,*args):
        self.open_file_dialog(self.add_json_filter,self.open_json_file)
        
    def save_range(self,*args):
        self.file_save_dialog(self.validate_json_name,self.save_json_file)

    def open_file(self, *args):
        self.open_file_dialog(self.add_image_filters,self.open_file_response)

    def open_file_response(self,path):
        self.context.select_img(path)
        self.window.toolbar.refresh_ranges()
        self.window.update()

    def save_file(self, *args):
        result = self.context.file_name
        result = result.split(".")

        result[-2] += "_out"
        result = '.'.join(result)
        print(result)
        self.context.save_img(result)

    def save_file_as(self, *args):
        self.file_save_dialog(self.validate_image_name,self.context.save_img)

    def info_popup(self, *args):
        dialog = Gtk.MessageDialog(parent=None,buttons=Gtk.ButtonsType.OK,
                                   message_format="Program powstał w ramach realizacji projektu z języka Python. Autorami są Bartłomiej Grzesik oraz Władysław Cholewa")
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

    def add_json_filter(self,dialog):
        filter_json = Gtk.FileFilter()
        filter_json.set_name("JSON files")
        filter_json.add_mime_type("application/json")
        dialog.add_filter(filter_json)

    def validate_image_name(self, file_text):
        splitted = file_text.split(".")
        return splitted[-1] in self.accepted_extensions

    def validate_json_name(self,file_text):
        splitted=file_text.split(".")
        return splitted[-1]=="json"

    def save_json_file(self,path):
        with open(path,"w") as file:
            ranges=[]
            for range in self.context.processor.settings.ranges:
                ranges.append((range.gray_min,range.gray_max,range.threshold))
            json.dump(ranges,file)

    def open_json_file(self,path):
        with open(path,"r") as file:
            loaded=json.load(file)
            print(type(loaded))
            print(type(loaded[0]))
            print(type(loaded[0][0]))
            if isinstance(loaded,list) and len(loaded)>0:
                self.context.processor.settings.clear_range()
                for range in loaded:
                    if isinstance(range, list) and len(range)==3 and isinstance(range[0],int) and isinstance(range[1],int) and isinstance(range[2],int):
                        self.context.processor.settings.add_range(range[0],range[1],range[2])
                self.window.toolbar.refresh_ranges()
                self.window.update()

    def file_save_dialog(self,validation_function,creator_function):
        dialog = Gtk.FileChooserDialog(
            title="Please choose a folder",
            transient_for=self.window.window,
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
            entry.set_text("Example.*")
            entry.set_size_request(250, 50)
            dialog_box.pack_end(entry, True, True, 0)
            dialog_window.show_all()
            entry_response = dialog_window.run()
            pureFile = entry.get_text()
            dialog_window.destroy()
            if entry_response == Gtk.ResponseType.OK and validation_function(pureFile):
                separator = "/"
                if os.name == "nt":
                    separator = "\\"
                creator_function(dialog.get_filename() + separator + pureFile)
            else:
                pass
        elif response == Gtk.ResponseType.CANCEL:
            pass

        dialog.destroy()

    def open_file_dialog(self,filter_adder,response_function):
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
