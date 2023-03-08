from flask import Flask, render_template,Response
from FaceDetection.Jolo_Detection import facialDetection


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(facialDetection(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':

    app.run(
        host='0.0.0.0',
        debug=True,
        port=3030)
    