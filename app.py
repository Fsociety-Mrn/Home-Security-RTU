from flask import Flask, render_template,Response,request
from FaceDetection.Jolo_Detection import facialDetection,facialRegister

import cv2
app = Flask(__name__)

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
    
    
    return Response(facialDetection(camera=camera, face_detector=faceetector), mimetype='multipart/x-mixed-replace; boundary=frame')


# this block of code is for registration
@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/registerFacial')
def registerFacial():

    camera = cv2.VideoCapture(0)
    camera.set(4,1080)
    
# Load face detector
    faceetector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    return Response(facialRegister(camera=camera, face_detector=faceetector), mimetype='multipart/x-mixed-replace; boundary=frame')

# subumit form

@app.route('/submit', methods=['POST'])
def submit_form():
    first_name = request.form.get('firstname')
    last_name = request.form.get('lastname')
    print(first_name + last_name)
    # do something with the form data
    return render_template('face.html')


if __name__ == '__main__':

    app.run(
        host='0.0.0.0',
        debug=True,
        port=3030)
    