import cv2
import numpy as np
from dataclasses import dataclass, field
from typing import *


@dataclass
class OtsuRange(object):
    gray_min: int
    gray_max: int

    threshold: int


@dataclass
class ImageProcessorSettings(object):
    ranges: List[OtsuRange] = field(default_factory=list)
    blur: int = 21

    def add_range(self, gray_min: int, gray_max: int, threshold: int):
        self.ranges.append(OtsuRange(gray_min=gray_min,
                                     gray_max=gray_max,
                                     threshold=threshold))


def get_otsu_threshhold(img, mask):
    threshold, _ = cv2.threshold(img[mask != 0], 0, 255,
                                 cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    return threshold


class ImageProcessor(object):

    def __init__(self, img,context):
        if isinstance(img, str):
            self.orig = cv2.imread(img)
        else:
            self.orig = img

        self.ranges = []
        self.gray = None
        self.gauss = None
        self.context=context
        self.settings = ImageProcessorSettings()
        self.colours=[[106,161,19],[28,89,237],[148,237,5],[237,66,28],[161,38,11],[161,130,19],[0,240,204],[237,187,5],[237,28,237],[163,0,163]]
    def process(self):
        if self.gray is None:
            self.gray = cv2.cvtColor(self.orig, cv2.COLOR_RGB2GRAY)

        if self.gauss is None:
            self.gauss = cv2.GaussianBlur(
                self.gray, (self.settings.blur, self.settings.blur), 0)

        if self.context.regions is None:
            self.context.regions= cv2.cvtColor(self.gray, cv2.COLOR_GRAY2RGB)

        out = np.zeros_like(self.gray)
        total_mask = np.zeros_like(self.gray)

        colour_it=0
        for otsu in self.settings.ranges:
            col_min = np.array([otsu.gray_min])
            col_max = np.array([otsu.gray_max])
            mask = cv2.inRange(self.gauss, col_min, col_max)

            tmp = cv2.bitwise_and(total_mask, mask)
            cv2.bitwise_xor(tmp, mask, dst=mask)

            self.context.regions[mask==255] =self.colours[colour_it]

            print(get_otsu_threshhold(self.gray, mask))

            _, th = cv2.threshold(self.gray, otsu.threshold, otsu.gray_max,
                                  cv2.THRESH_BINARY)

            th[th != 0] = 255

            cv2.copyTo(th, mask, dst=out)
            cv2.copyTo(mask, mask, dst=total_mask)

            th = cv2.bitwise_and(th, mask)
            colour_it=(colour_it+1)%len(self.colours)
        return out
