# NOTE: Code directory
# Login 
#   |-- Mainpage
#   |-- Facial Login
#           | -- Load Facial Recognition
#           | -- Facial Recognition Function
#           | -- API route Facial Recognition Result
#   | -- Finger Login
#           | -- API for Fingerprint Result
#           | -- Verify Finger Login Function

# Registration
#     | -- Register name
#               | -- API for submit 
#     | -- Fingerprint Register
#               | -- API for Fingerprint Register
#               | -- Enroll Finger Function
#     | -- Facial Registration
#               | -- Load Facial Detection
#               | -- Facial Register Function
#               | -- API route Facial Register status
# Surveilance
#     | -- Surveilance
#               | -- Load Surveilance Camera
#               | -- Surveilance Camera Function


from flask import Flask, render_template,Response,request,redirect, url_for, jsonify
# from Face_Recognition.Face_Recognition import JoloRecognition as Jolo
from Facerecognition.Face_Recognition import Face_Recognition as Jolo

import cv2
import os
import time
# import adafruit_fingerprint
# import serial
# import RPi.GPIO as GPIO
import threading

# Set up GPIO
# GPIO.setmode(GPIO.BCM)
# GPIO.setwarnings(False)

# # seplenoid lock
# GPIO.setup(24, GPIO.OUT, initial=GPIO.LOW)

# # Ultrasonic Sensor

# # TRIGGER
# GPIO.setup(21, GPIO.OUT)

# # ECHO
# GPIO.setup(20, GPIO.IN)

# # buzzer
# GPIO.setup(6, GPIO.OUT, initial=GPIO.LOW)

# # Buton
# GPIO.setup(5, GPIO.IN,pull_up_down=GPIO.PUD_UP)

app = Flask(__name__)

# NOTE:
# uncomment this code if camera wont open in windows

# this is for facial recognition
# camera = cv2.VideoCapture(0)
# camera.set(4,1080)
    
# this is for surveillance cam
# camerSurveillance = cv2.VideoCapture(1)

# result of facial training
result = "capturing..."

# result of face recognition
Text = ""

# route for registered faces
path = f"FaceDetection/Known_Faces/"

# fingeprint
location = 1
finger_status = ""






# uart = serial.Serial('/dev/ttyS0', baudrate=57600, timeout=1)

# finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)

@app.route('/successLogin')
def successLogin():
    
    return render_template('success.html')
# ========================== Login ========================== #


@app.route("/alarming", methods=['GET'])
def alarming():
    # buzzer()
    # GPIO.output(6,GPIO.HIGH)

    return jsonify(
            {
                'message': "Emergency!",
                'warning': True
            },200)
    
@app.route("/emergencyButton", methods=['GET'])
def emergency():
    # if GPIO.input(5):
    #     GPIO.output(6,GPIO.HIGH)

    #     return jsonify(
    #         {
    #             'message': "Emergency!",
    #             'warning': True
    #         },200)
    # else:
     
    #     return jsonify(
    #         {
    #             'message': "Not Emegergency!",
    #             'warning': False
    #         },200)
        
    return jsonify(
        {
            'message': "Not Emegergency!",
            'warning': False
        },200)        

@app.route("/alert", methods=['GET'])
def alarm():
    
        return jsonify(
            {
                'message': "Force Entry!",
                'warning': True
            },200)
    
    # GPIO.output(21,False)
    # time.sleep(0.5)
    # GPIO.output(21,True)
    # time.sleep(0.00001)
    # GPIO.output(21,False)
    
    # pulse_start,pulse_end = 0,0
    # while GPIO.input(20) == 0:
    #     pulse_start = time.time()
        
    # while GPIO.input(20) == 1:
    #     pulse_end = time.time()
        
    # distance = (pulse_end-pulse_start) * 17150
    # inches = round(distance / 2.54, 1)
    
    
    # print(inches)
    
    # if inches < 10.0:
    #     GPIO.output(6,GPIO.HIGH)

        
    #     return jsonify(
    #         {
    #             'message': "Force Entry!",
    #             'warning': True
    #         },200)
    # return jsonify(
    #         {
    #             'message': "No worry ",
    #             'warning': False
    #         },200)

def buzzer():
    # GPIO.output(6,True)
    print("Buzzer On")
    time.sleep(0.5)
    # GPIO.output(6,False)
    print("Buzzer On")
    time.sleep(0.5)

@app.route("/offBuzzer", methods=['GET'])
def offBuzzer():
    
    threading.Thread(target=turnOffBuzzer,args=()).start()
    return jsonify(
            {
                'message': "No worry ",
                'warning': False
            },200)
    
def turnOffBuzzer():
    print("Buzzer Off")
    # GPIO.output(6, GPIO.LOW)

# Main page
@app.route('/')
def index():
    global result,Text
    result = "capturing..."
    Text = "Loading face recognition"
    return render_template('index.html')

@app.route("/high", methods=['GET'])
def high():
    # GPIO.output(6,GPIO.LOW)

    # GPIO.output(24, GPIO.HIGH)
    # time.sleep(3)
    # GPIO.output(24, GPIO.LOW)
    return jsonify(
            {
                'message': "LED on"
            },200)
    

@app.route("/low", methods=['GET'])
def low():
    # GPIO.output(24, GPIO.LOW)
    return jsonify(
            {
                'message': "LED OFF"
            },200)
    



#  load facial recognition
@app.route('/video_feed')
def video_feed():
# comment this code if camera wont open on windows
    
    # load camera
    camera = cv2.VideoCapture(0)
 
    
    # Load face detector
    faceetector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    return Response(facialDetection(camera=camera, face_detector=faceetector), mimetype='multipart/x-mixed-replace; boundary=frame')


# Finger Login 
@app.route('/seventh_page')
def seventh_page():
    return render_template('finger-login.html')

# API for Fingerprint Result
@app.route('/fingerlogin', methods=['GET'])       
def verify_finger():
    if get_fingerprint():
        # print("Detected #", finger.finger_id, "with confidence", finger.confidence)
        
        # GPIO.output(6,GPIO.LOW)

        # GPIO.output(24, GPIO.HIGH)
        # time.sleep(3)
        # GPIO.output(24, GPIO.LOW)
        
        return jsonify(
            {
                'error': False,
                'message': "Success"
            },200) 
    else:
        print("Finger not found")
        
   
            
        return jsonify({
                'error': True,
                'message': "Failed please try again"
            },400)
        
# Verify Finger Login Function
def get_fingerprint():
    return True
    # """Get a finger print image, template it, and see if it matches!"""
    # print("Waiting for image...")
    # while finger.get_image() != adafruit_fingerprint.OK:
    #     pass
    # print("Templating...")
    # if finger.image_2_tz(1) != adafruit_fingerprint.OK:
    #     return False
    # print("Searching...")
    # if finger.finger_search() != adafruit_fingerprint.OK:
    #     return False
    
    
    
    return True


# ------------------- facial recognition Function
def facialDetection(camera=None, face_detector=None):
    global Text
    B , G , R = (0,255,255)
    Text = ""
    
    textResult = ""
    # Login Attempt
    success = 0
    fail = 0                                    
    
    # Initialize the timer and the start time
    timer = 0
    start_time = time.time()
    
    while True:
        
        # Capture a frame from the camera
        ret, frame = camera.read()
        
        if not ret:
            break

        frame = cv2.flip(frame,1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces in the frame
        faces = face_detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=20, minSize=(100, 100), flags=cv2.CASCADE_SCALE_IMAGE)
   
        # checking detecting face should be 1
        if len(faces) == 1:
                            
            # Check if 2 seconds have elapsed since the last send
            if timer >= 2:
                       
                # facial comparison 
                response = Jolo().Face_Compare(face=frame)

                try:
    
                    # check if face is recognize
                    if "No match detected" != response[0] and success < 2:
                        success += 1
                    else: 
                        # check if not 
                        fail += 1
                        B, G, R = (0, 0, 255)

                        # check if fail
                        if fail == 3:
                            Text = "Access Denied"
                            fail = 1
                            B, G, R = (0, 0, 255)
                            # route to failure pages
                    
                        # check if success      
                        if success == 2:
                            Text = "Access Granted"
                            
                            # GPIO.output(6,GPIO.LOW)

                            # GPIO.output(24, GPIO.HIGH)
                            # time.sleep(3)
                            # GPIO.output(24, GPIO.LOW)
                            
                            textResult = response[0]
                            B, G, R = (0, 255, 0)
                            success = 1
                            fail=1     

                        # textResult = response[0]              
                        
                except:
                    pass
                # Reset the timer and the start time
                timer = 0
                start_time = time.time()
            else:
                # Increment the timer by the elapsed time since the last send
                timer += time.time() - start_time
                start_time = time.time()
                
            # Get the coordinates of the face
            (x, y, w, h) = faces[0]
            
            # Draw a rectangle around the face and pt text
            #cv2.rectangle(frame, (x, y), (x+w, y+h), (R,G,B), 2)
            cv2.putText(frame,textResult,(x,y+h+30),cv2.FONT_HERSHEY_COMPLEX,1,(R,G,B),1)

            # Center coordinates
            center_coordinates = x + w // 2, y + h // 2
  
            # Radius of circle
            radius = w // 2
   
            # Blue color in BGR
            color = (B, G, R)
   
#            Line thickness of 2 px
            thickness = 3
            cv2.circle(frame, center_coordinates, radius, color, thickness)
            
            
        elif len(faces) > 1:
            
            # If more than 1 faces 
            # B, G, R = (0, 0, 255)
            Text = "More than 1 face is detected"
        else:
            # B, G, R = (0, 0, 0)
            Text = "No face is detected"    
            
        _, frame_encoded  = cv2.imencode('.png', frame)
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame_encoded.tobytes() + b'\r\n')
        
# API route Facial Recognition Result
@app.route("/GET_FacialResult", methods=["GET"])
def GET_FacialResult():
    return jsonify(Text) 

# ========================== Registration ========================== #

# Register Name
@app.route('/third_page')
def thirdpage():
    return render_template('name-register.html')

# API for submit 
@app.route('/submit', methods=['POST'])
def submit_form():
    global path

    # Define the path to the folder you want to create
    path = f"Facerecognition/Registered-Faces/{str(request.form.get('fullname'))}"
    
    # Check if the folder already exists
    if os.path.exists(path):
        return jsonify({'error': f"Folder {path} already exists"}), 400
    else:
        os.makedirs(path)
        # route to facial registration
        return redirect(url_for('fourt_page'))

# Fingerprint Register **************************** #
@app.route('/fourt_page')
def fourt_page():
    
    # please check if finger print is registered
    return render_template('finger-register.html')

# API for Fingerprint Register
@app.route('/fingerprint', methods=['GET'])
def fingerprint_registration():
    
    return jsonify({
            'error': False,
            'message': "Fingerprint enrolled successfully"
        },200)
    
    # if enroll_finger():
    #     return jsonify({
    #         'error': False,
    #         'message': "Fingerprint enrolled successfully"
    #     },200)
    # else:
    #     return jsonify({
    #         'error': True,
    #         'message': "Fingerprint enrolled failed"
    #     },400)

# Enroll Finger Function
# def enroll_finger():
#     """Take a 2 finger images and template it, then store in the next empty location"""
#     global location,finger_status

#     # Search for the next empty finger location
#     while finger.load_model(location) == adafruit_fingerprint.OK:
#         location += 1

#     for fingerimg in range(1, 3):
#         if fingerimg == 1:
#             print("Place finger on sensor...", end="")
#             finger_status = "Place finger on sensor..."
#         else:
#             print("Place same finger again...", end="")
#             finger_status = "Place finger on sensor..."
            
#         while True:
#             i = finger.get_image()
#             if i == adafruit_fingerprint.OK:
#                 print("Image taken")
#                 finger_status = "Image taken"
#                 break
            
#             if i == adafruit_fingerprint.NOFINGER:
#                 print(".", end="")
#                 finger_status = "waiting finger"
                
#             elif i == adafruit_fingerprint.IMAGEFAIL:
#                 print("Imaging error")
#                 finger_status = "Imaging error"
#                 return False
#             else:
#                 print("Other error")
#                 finger_status = "Other error"
#                 return False

#         print("Templating...", end="")
#         i = finger.image_2_tz(fingerimg)
#         if i == adafruit_fingerprint.OK:
#             print("Templated")
#             finger_status = "Templated"
#         else:
#             if i == adafruit_fingerprint.IMAGEMESS:
#                 print("Image too messy")
#                 finger_status = "Image too messy"
#             elif i == adafruit_fingerprint.FEATUREFAIL:
#                 print("Could not identify features")
#                 finger_status = "Could not identify features"
#             elif i == adafruit_fingerprint.INVALIDIMAGE:
#                 print("Image invalid")
#                 finger_status = "Image invalid"
#             else:
#                 print("Other error")
#                 finger_status = "Other error"
#             return False

#         if fingerimg == 1:
#             print("Remove finger")
#             finger_status = "Remove finger"
#             time.sleep(1)
#             while i != adafruit_fingerprint.NOFINGER:
#                 i = finger.get_image()

#     print("Creating model...", end="")
#     i = finger.create_model()
#     if i == adafruit_fingerprint.OK:
#         print("Created")
#     else:
#         if i == adafruit_fingerprint.ENROLLMISMATCH:
#             print("Prints did not match")
#         else:
#             print("Other error")
#         return False

#     print("Storing model #%d..." % location, end="")
#     i = finger.store_model(location)
#     if i == adafruit_fingerprint.OK:
#         print("Stored")
#     else:
#         if i == adafruit_fingerprint.BADLOCATION:
#             print("Bad storage location")
#         elif i == adafruit_fingerprint.FLASHERR:
#             print("Flash storage error")
#         else:
#             print("Other error")
#         return False

#     print("Fingerprint enrolled successfully")
#     finger_status = "Fingerprint enrolled successfully"
#     location += 1  # Increment finger location
#     return True


# Facial Registration
@app.route('/fifth_page')
def fifth_page():
    
    # Training: we pass the training parameter to html file
    
    return render_template('facial-register.html')

    

# load facial detection
@app.route('/facial_register')
def facial_register():
# comment this code if camera wont open on windows
    
    # load camera
    camera = cv2.VideoCapture(0)
    # camera.set(4,1080)
    
    # Load face detector
    faceetector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    return Response(
        facialRegister(
        camera=camera, 
        face_detector=faceetector,
        path=path
        ),mimetype='multipart/x-mixed-replace; boundary=frame')

#  Facial Register Function
def facialRegister(camera=None, face_detector=None, path=None):
    global result
    capture=1
    result = "Capture " + str(capture)
    
    # Initialize the timer and the start time
    timer = 0
    start_time = time.time()
   
    while True:
        
        # Capture a frame from the camera
        ret, frame = camera.read()
        
        # check if camera is working
        if not ret:
            break
     
        frame = cv2.flip(frame,1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
        # Detect faces in the frame
        faces = face_detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=20, minSize=(100, 100), flags=cv2.CASCADE_SCALE_IMAGE) 
        
        # check if there is 1 face detected
        # NOTE: if more than 1 it wont detected and the timer will restart
        if len(faces) == 1:
        
    
            if timer >= 0.5:
                
                if not len(os.listdir(path))==10:
                    cv2.imwrite(path + "/" +str(capture)+".png", frame)
                    capture+=1
                    result = "Capture " + str(capture)
                else:
                    
                    result = "Training"
                    # facial training
                    result=Jolo().Face_Train()

                    
                    
                timer = 0
                start_time = time.time()
            else:
                timer += time.time() - start_time
                start_time = time.time()
                
            # Get the coordinates of the face
            (x, y, w, h) = faces[0]
            
            # Draw a rectangle around the face and pt text
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)    
        
        
        _, frame_encoded  = cv2.imencode('.png', frame)
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame_encoded.tobytes() + b'\r\n')

# API for Facial Register status
@app.route("/update_variable", methods=["GET"])
def update_variable():
    # Replace this with the code that generates the new value of the variable
    new_value = result
    return jsonify(new_value)     
        
# ========================== Surveilance ========================== #

# Surveilance
@app.route('/sixth_page')
def sixth_page():
    return render_template('surveilance.html')



# Load Surveilance Camera
@app.route('/surveilance_camera')
def surveilance_camera():  
# comment this code if camera wont open on windows

    camera = cv2.VideoCapture(0)
    
    return Response(surveilanceCamera(camera=camera),mimetype='multipart/x-mixed-replace; boundary=frame')

# Surveilance Camera Function
def surveilanceCamera(camera=None):
    while True:
        _, frame = camera.read()
        frame = cv2.flip(frame,1)
        
            
        _, frame_encoded  = cv2.imencode('.png', frame)
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame_encoded.tobytes() + b'\r\n')
        
# Facial login
@app.route('/facial_logins')
def facial_logins():
    return render_template('facial-login.html')


if __name__ == '__main__':
    
    # TYPE on raspberry Terminal: hostname -I
    # copy and replace the host
    app.run(
        # host='192.168.254.116',
        host='0.0.0.0',        
        debug=True,
        port=4000)
    
    