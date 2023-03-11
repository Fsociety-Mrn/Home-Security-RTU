import os
import cv2

from werkzeug.utils import secure_filename
from flask import Flask, request
from FaceDetection.JoloRecognition import JoloRecognition as JL

app = Flask(__name__) 

# 16 MB max file size
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  

# Upload folder status
app.config['UPLOAD_FOLDER'] = 'Static/uploads'

# upload images in known folder
app.config['REGISTER_FACIAL'] = 'FaceDetection/Known_Faces/Art Lisboa'

# accepted file type
app.config['MIMETYPES'] = {'image/png', 'image/jpeg', 'image/gif', 'image/svg+xml', 'image/webp.'}
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'webp'}

# validate the extentsion
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/face-recognition', methods=['POST'])
def upload_file():
    
    file = request.files['file']
    
    # check file if exist
    if file and allowed_file(file.filename):
        
        # check if file name is not malicious
        filename = secure_filename(file.filename)
        
        # save the file
        # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # read sending file via cv2
        file = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # facial reconition
        result = JL().Face_Compare(file,threshold=0.6)
        
        # return the result
        return result[0]
    else:
        
        # invalid file
        return 'Invalid file type'

@app.route("/facial-register", methods=['POST'])
def facialRegister():
    
    file = request.files['file']
    
    # check file if exist
    if file and allowed_file(file.filename):
        
        # check if file name is not malicious
        filename = secure_filename(file.filename)
        
        # save the file
        file.save(os.path.join(app.config['REGISTER_FACIAL'], filename))
        
        # return the result
        return "Save successfully"
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
    