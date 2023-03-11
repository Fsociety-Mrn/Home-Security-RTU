import cv2
import requests
import time

from io import BytesIO

url='http://192.168.100.36:1030'

# facial register
def facialRegister(face_recognition_url = url + '/facial-register',camera=None, face_detector=None):

    timer = 0
    start_time = time.time()

    capture = 1
    while capture <= 20:
        
        # Capture a frame from the camera
        ret, frame = camera.read()
        
        if not ret:
            break
    
        frame = cv2.flip(frame,1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
        # Detect faces in the frame
        faces = face_detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=20, minSize=(100, 100), flags=cv2.CASCADE_SCALE_IMAGE) 
                    
        if len(faces) == 1:
            
            if timer >= 0.5:
                
                # Encode the frame as a JPEG image
                img_encoded  = cv2.imencode('.png', frame)[1].tobytes()
                
                # Send the JPEG image to the face recognition API
                response = requests.post(
                    face_recognition_url, 
                    files={
                            'file': (str(capture)+".png", BytesIO(img_encoded), 'image/png')
                        })
                
                print(response.text)
                
                timer = 0
                start_time = time.time()
                capture +=1
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
        





# facial recognition
def facialDetection(face_recognition_url = url + '/face-recognition', camera=None, face_detector=None):
    
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
                            
            # Check if 2 seconds have elapsed since the last send
            if timer >= 0.8:
                        
                # Encode the frame as a JPEG image
                img_encoded  = cv2.imencode('.png', frame)[1].tobytes()
                
                # Send the JPEG image to the face recognition API
                response = requests.post(
                    face_recognition_url, 
                    files={
                            'file': ('image.png', BytesIO(img_encoded), 'image/png')
                        })
                
                # check if there is matches and if status code is 200 
                B, G, R = (255, 0, 0) if response.text == 'No match detected' else (0, 255, 0) if response.status_code == 200 else (0, 0, 255)
                Text = response.text

                    
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
            cv2.rectangle(frame, (x, y), (x+w, y+h), (R,G,B), 2)
            cv2.putText(frame,Text,(x,y+h+30),cv2.FONT_HERSHEY_COMPLEX,1,(R,G,B),1)
                    
        _, frame_encoded  = cv2.imencode('.png', frame)
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame_encoded.tobytes() + b'\r\n')