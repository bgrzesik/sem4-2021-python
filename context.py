from processor import ImageProcessor
import cv2


class Context(object):

    def __init__(self):
        self.img = None
        self.processor = None
        self.dest = None
        self.regions = None
        self.file_name = None

    def select_img(self, img):
        self.file_name = img
        self.img = cv2.imread(img)
        self.processor = ImageProcessor(img)


    def save_img(self,path):
        cv2.imwrite(path, self.dest)

    def process(self):
        if self.img is None:
            return

        self.dest, self.regions = self.processor.process()
