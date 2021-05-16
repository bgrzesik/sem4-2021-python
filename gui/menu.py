from gi.repository import Gtk, GdkPixbuf
import tkinter.filedialog
import cv2

class Menu(object):

    def __init__(self, window: "MainWindow", ctx: "Context"):
        self.window=window
        self.context=ctx


        self.quit=window.builder.get_object("quit")
        self.quit.connect("activate",window.on_destroy)

        self.new=window.builder.get_object("new") #temporary until it will be different from open
        self.new.connect("activate",self.open_file)

        self.open=window.builder.get_object("open")
        self.open.connect("activate",self.open_file)

        self.save = window.builder.get_object("save")
        self.save.connect("activate", self.save_file)

        self.save_as = window.builder.get_object("save-as")
        self.save_as.connect("activate", self.save_file_as)

        self.about=window.builder.get_object("about")
        self.about.connect("activate",self.info_popup)
    def open_file(self,*args):
        root=tkinter.Tk()
        root.withdraw()
        file_name=tkinter.filedialog.askopenfilename(filetypes=(("JPEG Images",["*.jpg","*.jpeg","*.jpe"]),
                                                     ("PNG Images","*.png"),("TIFF Images",["*.tiff","*.tif"])))
        self.context.select_img(file_name)
        self.window.update()
        root.destroy()

    def save_file(self,*args):
        cv2.imwrite(self.context.file_name,self.context.dest)
    def save_file_as(self,*args):
        root = tkinter.Tk()
        root.withdraw()
        file_name = tkinter.filedialog.asksaveasfilename(defaultextension=".jpg",filetypes=(("JPEG Images", ["*.jpg", "*.jpeg", "*.jpe"]),
                                                                  ("PNG Images", "*.png"),
                                                                  ("TIFF Images", ["*.tiff", "*.tif"])))
        if file_name=="": return
        if not "*.*" in file_name: return
        cv2.imwrite(file_name, self.context.dest)
    def info_popup(self,*args):
        dialog=Gtk.MessageDialog(buttons=Gtk.ButtonsType.OK,message_format="Program powstał w ramach realizacji projektu z języka Python. Autorami są Bartłomiej Grzesik oraz Władysław Cholewa")
        dialog.connect("response",self.dialog_response)
        dialog.show()

    def dialog_response(self,widget,response_id):
        widget.destroy()