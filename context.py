from gi.repository import GLib

import cv2
import threading
import dataclasses
from processor import ImageProcessor, ImageProcessorSettings, get_otsu_threshhold
from contextlib import contextmanager
from copy import deepcopy


class WorkerThread(threading.Thread):

    def __init__(self, ctx: "Context"):
        super().__init__()

        self.ctx = ctx
        self.condvar = threading.Condition()
        self.daemon = True

    def run(self):
        while True:
            with self.condvar:
                while self.ctx.file_name == self.ctx.current_file_name and \
                        self.ctx.settings == self.ctx.current_settings:
                    self.condvar.wait()

            with self.ctx.lock:
                settings = deepcopy(self.ctx.settings)
                file_name = self.ctx.file_name
                img = self.ctx.img


            processor = ImageProcessor(img)
            processor.settings = settings
            
            if img is not None:
                dest, regions = processor.process()
            else:
                dest, regions = None, None
            
            with self.ctx.lock:
                self.ctx.current_settings = settings

                # write Otsu threshold to those ranges which didn't change
                if len(settings.ranges) == len(self.ctx.current_settings.ranges):
                    for new, cur in zip(settings.ranges, self.ctx.settings.ranges):
                        if new.user_set or cur.user_set:
                            continue

                        if (new.gray_min, new.gray_max) != (cur.gray_min, cur.gray_max):
                            continue

                        cur.threshold = new.threshold


                self.ctx.current_file_name = file_name
                self.ctx.gray = processor.gray
                self.ctx.dest = dest
                self.ctx.regions = regions
            
            GLib.idle_add(self.ctx.post_process)

class Context(object):

    def __init__(self, post_process):
        self.img = None
        self.dest = None
        self.gray = None
        self.regions = None
        self.post_process = post_process

        self.lock = threading.Lock()
        self.settings = ImageProcessorSettings()
        self.current_settings = deepcopy(self.settings)
        self.file_name = None
        self.current_file_name = None

        self.worker = WorkerThread(self)
        self.worker.start()


    def select_img(self, img):
        self.file_name = img
        self.img = cv2.imread(img)

        with self.lock:
            self.settings = ImageProcessorSettings()
            self.current_settings = deepcopy(self.settings)

            with self.worker.condvar:
                self.worker.condvar.notify()

    @contextmanager
    def change_settings(self) -> ImageProcessorSettings:
        with self.lock:
            settings = deepcopy(self.settings)
            print(settings, self.current_settings)
            
            yield settings

            print(settings, self.current_settings)
            self.settings = settings

            with self.worker.condvar:
                self.worker.condvar.notify()
    
    
