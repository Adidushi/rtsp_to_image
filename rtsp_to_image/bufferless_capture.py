#!/usr/bin/env python

import cv2, threading, time
from Queue import Queue, Empty


class VideoCapture:

    def __init__(self, name):
        self.cap = cv2.VideoCapture(name)
        self.q = Queue()
        self.ret = False
        t = threading.Thread(target=self._reader)
        t.daemon = True
        t.start()

    # read frames as soon as they are available, keeping only most recent one
    def _reader(self):
        while True:
            self.ret, frame = self.cap.read()
            if not self.ret:
                break
            if not self.q.empty():
                try:
                    self.q.get_nowait()  # discard previous (unprocessed) frame
                except Queue.empty():
                    pass
            self.q.put(frame)

    def read(self, timeout):
        try:
            return self.ret, self.q.get(True, timeout)
        except Empty:
            return False, None
            

