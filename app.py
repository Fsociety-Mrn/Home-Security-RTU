from flask import Flask, render_template,Response,request,redirect, url_for
from FaceDetection.Jolo_Detection import facialDetection,facialRegister

import cv2
import requests


url='http://192.168.100.36:1030'

app = Flask(__name__)


# camera = cv2.VideoCapture(0)
# camera.set(4,1080)
    

# this block of code is for entry code
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    
    # load camera
    camera = cv2.VideoCapture(0)
    camera.set(4,1080)
    
    # Load face detector
    faceetector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    
    return Response(facialDetection(url=url,camera=camera, face_detector=faceetector), mimetype='multipart/x-mixed-replace; boundary=frame')


# this block of code is for registration
@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/registerFacial')
def registerFacial():
# Load face detector
    camera = cv2.VideoCapture(0)
    camera.set(4,1080)

    faceetector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    return Response(facialRegister(url=url,camera=camera, face_detector=faceetector), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/facial')
def facial():
    return render_template('face.html')

@app.route('/submit', methods=['POST'])
def submit_form():
    
    first_name = request.form.get('firstname')
    last_name = request.form.get('lastname')

    api_url = "http://192.168.100.36:1030/name-register"
    data = {
        "first_name": str(first_name), 
        "last_name": str(last_name)
        }
    headers = {
        "Content-Type": "application/json"
        }
    
    response = requests.post(api_url, json=data, headers=headers)
    print(response.status_code)
    if response.status_code == 200 or response.status_code == 201:
        
        return redirect(url_for('/facial'))
    else:
        print("Error: Name registration failed with status code", response.status_code)
        print(response.content)
        return response.content


if __name__ == '__main__':

    app.run(
        host='0.0.0.0',
        debug=True,
        port=3030)
    