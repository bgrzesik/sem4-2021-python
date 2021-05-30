from threading import setprofile
from gi.repository import Gtk
from processor import ImageProcessorSettings, OtsuRange
from context import Context


class Toolbar(object):

    def __init__(self, window: "MainWindow", ctx: "Context"):
        self.ctx = ctx
        self.window = window
        self.builder = window.builder

        self.selected = None

        self.update_selected()

    def refresh_ranges(self):
        ranges = self.window.builder.get_object("ranges")
        ranges.clear()

        for i, rn in enumerate(self.ctx.settings.ranges):
            i = i == self.selected
            ranges.append([rn.gray_min, rn.gray_max, rn.threshold, i])


    def select_row(self, cell, idx):
        self.selected = int(idx)

        self.update_selected()
        self.refresh_ranges()

    def update_selected(self, *args):
        blur = self.builder.get_object("blur")
        gray = self.builder.get_object("gray")
        thresh = self.builder.get_object("thresh")

        range_add = self.builder.get_object("range-add")
        range_up = self.builder.get_object("range-up")
        range_down = self.builder.get_object("range-down")
        range_delete = self.builder.get_object("range-delete")

        slider_gray = self.builder.get_object("gray-slider")
        slider_thresh = self.builder.get_object("threshold-slider")


        blur.set_value(self.ctx.settings.blur)

        if self.ctx.file_name and self.selected is not None:
            idx = self.selected
            rn = self.ctx.settings.ranges[idx]

            gray.set_value((rn.gray_min + rn.gray_max) // 2)
            thresh.set_value(rn.threshold)
            
            range_add.set_sensitive(not self.ctx.settings.has_full_coverage())
            range_up.set_sensitive(idx > 0)
            range_down.set_sensitive(idx < len(self.ctx.settings.ranges) - 1)

            for widget in [range_delete, slider_gray, slider_thresh]:
                widget.set_sensitive(True)

        else:
            range_add.set_sensitive(self.ctx.file_name is not None \
                and not self.ctx.settings.has_full_coverage())

            gray.set_value(0)
            thresh.set_value(0)

            for widget in [range_up, range_down, range_delete, slider_gray, slider_thresh]:
                widget.set_sensitive(False)

    def add_range(self, ranges):
        gray_min, gray_max, threshold = 0, 0, 0

        with self.ctx.change_settings() as settings:
            settings.ranges.append(OtsuRange(gray_min, gray_max, threshold))
            self.selected = len(settings.ranges) - 1

        self.refresh_ranges()
        self.update_selected()

    def delete_range(self, *args):
        with self.ctx.change_settings() as settings:
            settings.ranges.pop(self.selected)

            if len(settings.ranges) > 0:
                if self.selected == 0:
                    self.selected = 0
                else:
                    self.selected -= 1
            else:
                self.selected = None
            

        self.refresh_ranges()
        self.update_selected()

    def move_range_up(self, *args):
        with self.ctx.change_settings() as settings:
            otsu = settings.ranges.pop(self.selected)
            self.selected -= 1
            settings.ranges.insert(self.selected, otsu)

        self.refresh_ranges()
        self.update_selected()

    def move_range_down(self, *args):
        with self.ctx.change_settings() as settings:
            otsu = settings.ranges.pop(self.selected)
            self.selected += 1
            settings.ranges.insert(self.selected, otsu)
    
        self.refresh_ranges()
        self.update_selected()

    def update_blur(self, blur):
        blur = int(blur.get_value())
        blur -= 1 - blur % 2

        with self.ctx.change_settings() as settings:
            settings.blur = blur

    def update_thresh(self, threshold):
        idx = self.selected
        if idx is None:
            return

        threshold = threshold.get_value()
        with self.ctx.change_settings() as settings:
            settings.ranges[idx].user_set = True
            settings.ranges[idx].threshold = threshold

        self.refresh_ranges()
        self.update_selected()

    def update_gray(self, gray):
        idx = self.selected
        if idx is None:
            return

        gray = gray.get_value()

        with self.ctx.change_settings() as settings:
            d = gray - (settings.ranges[idx].gray_min + settings.ranges[idx].gray_max) // 2
            settings.ranges[idx].gray_min = int(min(max(settings.ranges[idx].gray_min + d, 0), 255))
            settings.ranges[idx].gray_max = int(min(max(settings.ranges[idx].gray_max + d, 0), 255))

        self.refresh_ranges()
        self.update_selected()

    def range_min_edited(self, model, idx, text):
        if idx is None:
            return

        try:
            idx, text = int(idx), int(text)
        except:
            return

        with self.ctx.change_settings() as settings:
            settings.ranges[idx].gray_min = text

        self.refresh_ranges()
        self.update_selected()

    def range_max_edited(self, model, idx, text):
        if idx is None:
            return

        try:
            idx, text = int(idx), int(text)
        except:
            return

        with self.ctx.change_settings() as settings:
            settings.ranges[idx].gray_max = text

        self.refresh_ranges()
        self.update_selected()

    def range_threshold_edited(self, model, idx, text):
        if idx is None:
            return

        try:
            idx, text = int(idx), int(text)
        except:
            return

        with self.ctx.change_settings() as settings:
            settings.ranges[idx].user_set = True
            settings.ranges[idx].threshold = text

        self.refresh_ranges()
        self.update_selected()
