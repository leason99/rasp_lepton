import threading
import  camera

class AlertThread(threading.Thread):
    
    def __init__(self,camera,alertTempture):
        threading.Thread.__init__(self)
        self.stopped = threading.Event()
        self.alertTemp=alertTempture
        self.camera=camera
        self.alert=False


    def run(self):
        #while not self.stopped.wait(0.3):        
        while True:
        
            maxTemp=self.camera.get_tempture()["max"]
        
           
            if int(self.alertTemp) < int(maxTemp) :
                self.alert=True
            
    def stop(self):
        self.stopped.set()
        self.alert=False
    
    def isstop(self):
        return self.stopped.is_set()
    
    def setAlertTemp(self,alertTemp):
        self.alertTemp=alertTemp
    
    def isAlert(self):
        return self.alert 
           