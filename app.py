import cv2

from flask import Flask, jsonify, request,render_template,Response

import requests
from io import BytesIO

app = Flask(__name__)

#  setup camera
camera = cv2.VideoCapture(0)
camera.set(4,1080)

# face detection
face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')



def generate_frames(url=''):
    
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            frame = cv2.flip(frame,1)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Detect faces in the frame
            faces = face_detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=20, minSize=(100, 100), flags=cv2.CASCADE_SCALE_IMAGE)

            if len(faces) == 1:
                for (x, y, w, h) in faces:
                    face = frame[y:y+h, x:x+w]
                    # draw reactnagle on face detected
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2) 
                    
                    img_bytes = cv2.imencode('.jpg', frame)[1].tobytes()
                    response = requests.post(url, files={'file': ('image.jpg', BytesIO(img_bytes), 'image/jpeg')})
                    print(response.text)
                    
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':

    app.run(
        host='0.0.0.0',
        debug=True,
        port=3030)
    