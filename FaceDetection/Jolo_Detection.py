import cv2
import requests
import time

from io import BytesIO

#  setup camera
camera = cv2.VideoCapture(0)
camera.set(4,1080)

# Load face detector
face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def facialDetection(face_recognition_url ='http://192.168.100.36:1030/face-recognition'):
    R , G , B = 0,255,0
    Text = ""
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
            # Get the coordinates of the face
            (x, y, w, h) = faces[0]

            # Draw a rectangle around the face
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            cv2.putText(frame,Text,(x,y+h+30),cv2.FONT_HERSHEY_COMPLEX,1,(R,G,B),1)
                            
            # Check if 2 seconds have elapsed since the last send
            if timer >= 2:
                        
                # Encode the frame as a JPEG image
                img_encoded  = cv2.imencode('.jpg', frame)[1].tobytes()
                
                # Send the JPEG image to the face recognition API
                response = requests.post(
                    face_recognition_url, 
                    files={
                            'file': ('image.jpg', BytesIO(img_encoded), 'image/jpeg')
                        })
                print(response.text)
                if response.status_code == 200:
                    R , G , B = 0,255,0
                    Text = response.text
                else:
                    R , G , B = 255,0,0
                    Text = response.text
                    
                # Reset the timer and the start time
                timer = 0
                start_time = time.time()
            else:
                # Increment the timer by the elapsed time since the last send
                timer += time.time() - start_time
                start_time = time.time()
                    
        _, frame_encoded  = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame_encoded.tobytes() + b'\r\n')