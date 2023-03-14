from flask import Flask, render_template,Response,request,redirect, url_for
from FaceDetection.Jolo_Detection import facialDetection,facialRegister

import cv2
import requests

# NOTE:
# this is URL for API server
# please change this if you connected to the other network

url='http://192.168.100.36:1030'

app = Flask(__name__)

# NOTE:
# uncomment this code if camera wont open in windows
# camera = cv2.VideoCapture(0)
# camera.set(4,1080)
    

# ========================== Login ========================== #

# load facial recognition html
@app.route('/')
def index():
    return render_template('index.html')

#  load facial  recognition
@app.route('/video_feed')
def video_feed():
# comment this code if camera wont open on windows
    
    # load camera
    camera = cv2.VideoCapture(0)
    camera.set(4,1080)
    
    # Load face detector
    faceetector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    return Response(facialDetection(url=url,camera=camera, face_detector=faceetector), mimetype='multipart/x-mixed-replace; boundary=frame')

# ========================== registration ========================== #

# register name
@app.route('/register')
def register():
    return render_template('name-register.html')

# submit form
@app.route('/submit', methods=['POST'])
def submit_form():
    
    # send data to API endpoints
    response = requests.post(
        url + "/name-register", 
        json={ 
            "first_name": str(request.form.get('firstname')), 
            "last_name": str(request.form.get('lastname'))
        }, 
        headers={"Content-Type": "application/json"}
    )
    
    # check if status is created
    if response.status_code == 201:
        
        # route to facial registration
        return redirect(url_for('facial'))
         
    return response.content

# facial Registration
@app.route('/facial')
def facial():
    return render_template('facial-register.html')

# load facial detection
@app.route('/facial_register')
def facial_register():
# comment this code if camera wont open on windows
    
    # load camera
    camera = cv2.VideoCapture(0)
    camera.set(4,1080)
    
    # Load face detector
    faceetector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # local = load localhost  IP address
    # url = server localhost IP address
    # camera = load camera
    # face_detecter = facial detection
    return Response(
        facialRegister(

            local=str(request.remote_addr) + ":" + str(request.environ.get('SERVER_PORT')),
            url=url,
            camera=camera, 
            face_detector=faceetector), 
        mimetype='multipart/x-mixed-replace; boundary=frame')
  

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        debug=True,
        port=3030)
    