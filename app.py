#!/usr/bin/env python
from flask import Flask, render_template, Response ,jsonify 

# emulated camera
from camera_pi import Camera
import cv2
import numpy as np

# Raspberry Pi camera module (requires picamera package)
# from camera_pi import Camera

app = Flask(__name__)

frame=None

#temp=999
@app.route('/')
def index():
    """Video streaming home page."""

    return render_template('index.html')


def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
       

        
        frame_jpg = cv2.imencode('.jpg', frame)[1].tostring()
        

        
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame_jpg + b'\r\n')

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')



@app.route('/tempture', methods= ['GET'])
def tempture():
    print("run ajax")


    tempture=jsonify(tempture=Camera().get_tempture())
    return tempture


if __name__ == '__main__':
    app.run(host='192.168.1.94', debug=True, threaded=True)
