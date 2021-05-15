from processor import ImageProcessor
import cv2


class Context(object):

    def __init__(self):
        self.img = None
        self.processor = None
        self.dest = None

    def select_img(self, img):
        self.img = cv2.imread(img)
        self.processor = ImageProcessor(img)

    def process(self):
        if self.img is None:
            return

        self.dest = self.processor.process()