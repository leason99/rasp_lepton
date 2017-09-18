#!/usr/bin/env python
from flask import Flask, render_template, Response ,jsonify,request,redirect,url_for
from camera_pi import Camera
from AlertThread import AlertThread 
# emulated camera
import threading

import cv2
import numpy as np
from DataManger import  DataManger
# Raspberry Pi camera module (requires picamera package)
# from camera_pi import Camera

app = Flask(__name__)
frame=None
alert_tempture=None
alertThread=None
camera=Camera()
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
    global camera
    return Response(gen(camera),mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/set_alert' ,methods=[ 'POST'])
def set_alert():
    alertTemp=request.form["alert_tempture"]
    global alertThread
    global camera
    if not alertThread:
        alertThread=AlertThread(camera,alertTemp)
        alertThread.start()
    else:
        if alertThread.isstop:
            alertThread=AlertThread(camera,alertTemp)
            alertThread.start()
        else :
            alertThread.setAlertTemp(alertTemp)
    
    
    return redirect(url_for('index'))

@app.route('/alert', methods= ['GET'])
def alert():
    global alertThread
    data={}
    if alertThread != None : 
        data["alert"]=alertThread.isAlert()
    else :
        data["alert"]=False

    data["text"]="The tempture is too hight"
    #print(data)
    return jsonify(data=data)
   

@app.route('/tempture', methods= ['GET'])
def tempture():
    #print("run ajax",Camera().get_tempture())

    tempture=jsonify(tempture=Camera().get_tempture())
    return tempture

@app.route('/searchDetails', methods= ['GET'])
def searchDetails():
    limit={
            "class":1,
            "temperature":{ "$ne": None }
    }
    details=DataManger.find(limit)
   
    maxTemp=[]

    for data in details:
    
        maxTemp.append(data["temperature"]["max"])

    return jsonify(maxTemp=maxTemp[-30:])




if __name__ == '__main__':
    app.run(host='192.168.1.94', debug=True, threaded=True)
