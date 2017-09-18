import time
import io
import threading
import numpy as np
#import picamera
import cv2
from pylepton import Lepton
from DataManger import DataManger
class Camera(object):
    thread = None  # background thread that reads frames from camera
    frame = None  # current frame is stored here by background thread
    tempture= None
    last_access = 0  # time of last client access to the camera
    #cap =None
    def initialize(self):
        if Camera.thread is None:
            # start background frame thread
            Camera.thread = threading.Thread(target=self._thread)
            Camera.thread.start()
            

            # wait until frames start to be available
            while self.frame is None:
                time.sleep(0)

    def get_frame(self):
        Camera.last_access = time.time()
        self.initialize()
        return self.frame

    def capture(self,device = "/dev/spidev0.0"):
        with Lepton(device) as l:
            a,_ = l.capture()
        print("capture")
        #cv2.normalize(a, a, 0, 65535, cv2.NORM_MINMAX)
        #np.right_shift(a, 8, a)
        return a #np.uint8(a)
    @classmethod
    def _thread(cls):
        device = "/dev/spidev0.0"
        with Lepton(device) as l:
            a,_ = l.capture()
        Tempture={}
        Tempture["max"]=(np.amax(a)   - 7400) / 29
        Tempture["min"]=(np.amin(a)   - 7400) / 29
        Tempture["ave"]=(np.mean(a)   - 7400) / 29
        cls.tempture=Tempture
        DataManger.save(Tempture)
        cv2.normalize(a, a, 0, 65535, cv2.NORM_MINMAX)
        np.right_shift(a, 8,a)
        Frame = np.uint8(a)
        cls.frame=Frame
        cls.thread = None
    
    def get_tempture(self):
        
        return self.tempture