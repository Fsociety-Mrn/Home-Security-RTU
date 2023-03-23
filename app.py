from flask import Flask, render_template,Response,request,redirect, url_for
from FaceDetection.Jolo_Detection import facialDetection,facialRegister

import cv2
import requests

# NOTE:
# this is URL for API server
# please change this if you connected to the other network


app = Flask(__name__)

# NOTE:
# uncomment this code if camera wont open in windows
camera = cv2.VideoCapture(0)
camera.set(4,1080)
    

# ========================== Login ========================== #

# load main page
@app.route('/')
def index():
    return render_template('index.html')

# define route for facial login
@app.route('/second_page')
def second_page():
    return render_template('facial-login.html')

#  load facial recognition
@app.route('/video_feed')
def video_feed():
# comment this code if camera wont open on windows
    
    # load camera
    # camera = cv2.VideoCapture(0)
    # camera.set(4,1080)
    
    # Load face detector
    faceetector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    return Response(facialDetection(camera=camera, face_detector=faceetector), mimetype='multipart/x-mixed-replace; boundary=frame')

# ========================== registration ========================== #

# register name
@app.route('/third_page')
def thirdpage():
    return render_template('name-register.html')

# fingerprint register
@app.route('/fourt_page')
def fourtpage():
    return render_template('finger-register.html')

@app.route('/fifth_page')
def fifthpage():
    return render_template('surveilance.html')

# submit form for name register
@app.route('/submit', methods=['POST'])
def submit_form():
    
    # get Full name
    print(str(request.form.get('fullname')))
    
    # route to facial registration
    return redirect(url_for('facial'))
         
# facial Registration
@app.route('/facial')
def facial():
    return render_template('facial-register.html')

# load facial detection
@app.route('/facial_register')
def facial_register():
# comment this code if camera wont open on windows
    
    # load camera
    # camera = cv2.VideoCapture(0)
    # camera.set(4,1080)
    
    # Load face detector
    faceetector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # camera = load camera
    # face_detecter = facial detection
    return Response(facialRegister(camera=camera, face_detector=faceetector),mimetype='multipart/x-mixed-replace; boundary=frame')
  

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        debug=True,
        port=5000)
    
    