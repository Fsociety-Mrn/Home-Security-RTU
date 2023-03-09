from flask import Flask, render_template,Response
from FaceDetection.Jolo_Detection import facialDetection

import cv2
app = Flask(__name__)

camera = cv2.VideoCapture(0)
camera.set(4,1080)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(facialDetection(camera=camera), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':

    app.run(
        host='0.0.0.0',
        debug=True,
        port=3030)
    