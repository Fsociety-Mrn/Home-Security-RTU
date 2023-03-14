import os
import cv2

from werkzeug.utils import secure_filename
from flask import Flask, request,jsonify
from FaceDetection.JoloRecognition import JoloRecognition as JL

app = Flask(__name__) 

# 16 MB max file size
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  

# Upload folder status
app.config['UPLOAD_FOLDER'] = 'Static/uploads'

# upload images in known folder
app.config['REGISTER_FACIAL'] = 'FaceDetection/Known_Faces/'

# accepted file type
app.config['MIMETYPES'] = {'image/png', 'image/jpeg', 'image/gif', 'image/svg+xml', 'image/webp.'}
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'webp'}

# validate the extentsion
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ************************************* API ROUTES ************************************* #  #



# ================================ facial-recognition API ================================ #

# face recognition api
@app.route('/face-recognition', methods=['POST'])
def upload_file():
    
    file = request.files['file']
    
    # check file if exist
    if file and allowed_file(file.filename):
        
        # check if file name is not malicious
        filename = secure_filename(file.filename)
        
        # save the file
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # read sending file via cv2
        file = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # facial reconition
        result = JL().Face_Compare(file,threshold=0.6)
        
        # return the result
        return result[0]
    else:
        
        # invalid file
        return 'Invalid file type'



# ================================ name-register API ================================ #

# name register endpoint
@app.route('/name-register', methods=['POST']) 
def name_register():
    
    # Get the first and last name from the request body
    first_name = request.json.get('first_name', '')
    last_name = request.json.get('last_name', '')

    # Check that both first and last name are provided
    if not first_name or not last_name:
        return jsonify({'error': 'Both first and last name must be provided'}), 400

    # Define the name of the folder you want to create
    folder_name = f"{first_name} {last_name}"

    # Define the path to the folder you want to create
    path = f"FaceDetection/Known_Faces/{folder_name}"

    # Check if the folder already exists
    if os.path.exists(path):
        return jsonify({'error': f"Folder {path} already exists"}), 400

    # Create the folder using the os.makedirs() function
    try:
        os.makedirs(path)
        app.config['REGISTER_FACIAL'] = path
    except Exception as e:
        return jsonify({'error': f"Failed to create folder: {e}"}), 500

    # Return a success message
    return jsonify({'message': f"Folder {path} created successfully"}), 201



# ================================ facial-register API ================================ #

# check the file is valid
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# facial register endpoint
@app.route('/facial-register', methods=['POST'])
def facial_register():
    # Check if a file was uploaded
    file = request.files.get('file')
    if not file:
        return jsonify({'error': 'No file in request'}), 400

    # Check if the file is allowed
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Allowed file types are png, jpeg, jpg, gif.'}), 400

    # save the images if the folder of user is not 20
    if not len(os.listdir(app.config['REGISTER_FACIAL'])) == 20:
        
        # Save the file
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['REGISTER_FACIAL'], filename)
        file.save(file_path)

        return "File saved successfully"
    
    # train the known_images it return if successful train or not
    return JL().Face_Train(Dataset_Folder='FaceDetection/Known_Faces',location="FaceDetection/Model")

    
# ================================ check browser if server is running ================================ #
@app.route("/")
def hello_world():
    return "This is  basic  server made from flask!"


if __name__ == '__main__':

    app.run(
        host='0.0.0.0',
        debug=True,
        port=1030)
    