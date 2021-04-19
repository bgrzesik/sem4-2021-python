# %%

import math
import cv2
import numpy as np
import matplotlib
from dataclasses import dataclass, field
from matplotlib import pyplot as plt
from PIL import Image
from IPython import get_ipython
import ipywidgets as widgets
from typing import *

get_ipython().run_line_magic("matplotlib", "widget")

# %%


@dataclass
class OtsuRange(object):
    gray_min: int
    gray_max: int

    threshold: int


@dataclass
class ImageProcessorSettings(object):
    ranges: List[OtsuRange] = field(default_factory=list)
    blur: int = 15

    def add_range(self, gray_min: int, gray_max: int, threshold: int):
        self.ranges.append(OtsuRange(gray_min=gray_min,
                                     gray_max=gray_max,
                                     threshold=threshold))


class ImageProcessor(object):

    def __init__(self, img):
        if isinstance(img, str):
            self.orig = cv2.imread(img)
        else:
            self.orig = img

        self.ranges = []
        self.gray = None

        self.settings = ImageProcessorSettings()

    def process(self):
        if not self.gray:
            self.gray = cv2.cvtColor(self.orig, cv2.COLOR_RGB2GRAY)

        out = self.gray.copy()

        gauss = cv2.GaussianBlur(
            self.gray, (self.settings.blur, self.settings.blur), 0)

        col_min = np.array([0])
        col_max = np.array([0])
        total_mask = cv2.inRange(gauss, col_min, col_max)

        fig, ax = plt.subplots()
        ax.imshow(out, cmap="gray")
        fig.show()

        fig, ax = plt.subplots()
        ax.imshow(gauss, cmap="gray", vmin=0, vmax=255)
        fig.show()

        for otsu in self.settings.ranges:
            col_min = np.array([otsu.gray_min])
            col_max = np.array([otsu.gray_max])
            mask = cv2.inRange(gauss, col_min, col_max)

            tmp = cv2.bitwise_and(total_mask, mask)
            cv2.bitwise_xor(tmp, mask, mask=mask)

            fig, ax = plt.subplots()
            ax.imshow(mask, cmap="gray", vmin=0, vmax=255)
            fig.show()

            _, th = cv2.threshold(out, otsu.threshold, otsu.gray_max,
                                  cv2.THRESH_BINARY)

            print(th)

            cv2.copyTo(th, mask, out)
            cv2.copyTo(mask, mask, total_mask)

            th = cv2.bitwise_and(th, mask)

            fig, ax = plt.subplots()
            ax.imshow(th, cmap="gray", vmin=0, vmax=255)
            fig.show()

            fig, ax = plt.subplots()
            ax.imshow(out, cmap="gray", vmin=0, vmax=255)
            fig.show()


proc = ImageProcessor("./eg/1.jpg")
proc.settings.add_range(190, 250, 195)
proc.settings.add_range(150, 190, 160)
proc.process()
