import os
import cv2

from werkzeug.utils import secure_filename
from flask import Flask, jsonify, request,render_template,Response
from JoloRecognition import JoloRecognition as JL

app = Flask(__name__)

# for face-recogition server
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 16 MB
app.config['UPLOAD_FOLDER'] = 'Static/uploads'
app.config['MIMETYPES'] = {'image/png', 'image/jpeg', 'image/gif', 'image/svg+xml', 'image/webp', 'image/mp4'}


ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'webp', 'mp4'}

# validate the extentsion
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/face-recognition', methods=['POST'])
def upload_file():
    
    file = request.files['file']
    
    if file and allowed_file(file.filename):
        
        # check if file name is not malicious
        filename = secure_filename(file.filename)
        
        file = cv2.imread(filename)
        
        cv2.imshow("hcehckc", file)
        # save the file
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return 'File uploaded successfully'
    else:
        
        # invalid file
        return 'Invalid file type'


# check browser if server is running
@app.route("/")
def hello_world():
    return "This is  basic  server made from flask!"

    


if __name__ == '__main__':

    app.run(
        host='0.0.0.0',
        debug=True,
        port=1030)
    