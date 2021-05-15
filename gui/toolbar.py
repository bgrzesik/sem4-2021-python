
from gi.repository import Gtk
from processor import OtsuRange


class Toolbar(object):

    def __init__(self, window: "MainWindow", ctx: "Context"):
        self.ctx = ctx
        self.window = window
        self.builder = window.builder
        self.ranges = window.builder.get_object("ranges")

        self.selected_cell = None
        self.selected = None

        window.builder.connect_signals(self)

    def refresh_ranges(self):
        self.ranges.clear()

        for i, rn in enumerate(self.ctx.processor.settings.ranges):
            i = i == self.selected
            self.ranges.append([rn.gray_min, rn.gray_max, rn.threshold, i])

    def select_row(self, cell, idx):
        if self.selected_cell is not None:
            self.selected_cell.set_active(False)

        self.selected_cell = cell
        self.selected_cell.set_active(True)
        self.selected = int(idx)

        self.update_selected()
        self.refresh_ranges()

    def update_selected(self, *args):
        gray = self.builder.get_object("gray")
        thresh = self.builder.get_object("thresh")

        if self.selected_cell is not None:
            idx = self.selected
            rn = self.ctx.processor.settings.ranges[idx]

            gray.set_value((rn.gray_min + rn.gray_max) // 2)
            thresh.set_value(rn.threshold)
        else:
            gray.set_value(0)
            thresh.set_value(0)

    def add_range(self, ranges):
        gray_min, gray_max, threshold = 0, 0, 0
        ranges = self.ctx.processor.settings.ranges
        ranges.append(OtsuRange(gray_min, gray_max, threshold))

        if self.selected_cell:
            self.selected_cell.set_active(False)
            self.selected_cell = None
            self.selected = None

        self.refresh_ranges()
        self.window.update()
        self.update_selected()

    def delete_range(self, selection):
        _, tree_iter = selection.get_selected_rows()

        ranges = self.ctx.processor.settings.ranges
        for row in reversed(tree_iter):
            row = row.get_indices()[0]
            ranges.pop(row)

        if self.selected_cell:
            self.selected_cell.set_active(False)
            self.selected_cell = None
            self.selected = None

        self.refresh_ranges()
        self.window.update()
        self.update_selected()

    def update_thresh(self, threshold):
        idx = self.selected
        if idx is None:
            return

        ranges = self.ctx.processor.settings.ranges
        threshold = threshold.get_value()
        ranges[idx].threshold = threshold

        self.refresh_ranges()
        self.window.update()
        self.update_selected()

    def update_gray(self, gray):
        idx = self.selected
        if idx is None:
            return

        ranges = self.ctx.processor.settings.ranges
        gray = gray.get_value()

        d = gray - (ranges[idx].gray_min + ranges[idx].gray_max) // 2
        ranges[idx].gray_min += d
        ranges[idx].gray_max += d

        self.refresh_ranges()
        self.window.update()
        self.update_selected()

    def range_min_edited(self, model, idx, text):
        if idx is None:
            return

        try:
            idx, text = int(idx), int(text)
        except:
            return

        ranges = self.ctx.processor.settings.ranges
        ranges[idx].gray_min = text

        self.refresh_ranges()
        self.window.update()
        self.update_selected()

    def range_max_edited(self, model, idx, text):
        if idx is None:
            return

        try:
            idx, text = int(idx), int(text)
        except:
            return

        ranges = self.ctx.processor.settings.ranges
        ranges[idx].gray_max = text

        self.refresh_ranges()
        self.window.update()
        self.update_selected()

    def range_threshold_edited(self, model, idx, text):
        if idx is None:
            return

        try:
            idx, text = int(idx), int(text)
        except:
            return

        ranges = self.ctx.processor.settings.ranges
        ranges[idx].threshold = text

        self.refresh_ranges()
        self.window.update()
        self.update_selected()
