import cv2
import time
import webbrowser

from FaceDetection.Jolo_Recognition import JoloRecognition as Jolo

form_path = 'http://127.0.0.1:3030/'
# ============================== facial register ============================== #
def facialRegister(camera=None, face_detector=None):
    
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
            
            # Get the coordinates of the face
            (x, y, w, h) = faces[0]
            
            # Draw a rectangle around the face and pt text
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)    
        
        
        _, frame_encoded  = cv2.imencode('.png', frame)
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame_encoded.tobytes() + b'\r\n')
        


# ============================== facial recognition ============================== #
def facialDetection(camera=None, face_detector=None):
    
    R , G , B = 0,255,0
    Text = ""
    
    # Login Attempt
    success = 1
    fail = 1                                    
    
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
            if timer >= 1:
                
                # facial comparison 
                response = Jolo().Face_Compare(face=frame)
                
                try:
                
                # check if there is matches and if status code is 200 
                    B, G, R = (255, 0, 0) if response[0] == 'No match detected' else (0, 255, 0)
                    Text = response[0]
                    
         
                    # check if face is recognize
                    if "No match detected" != response[0] and success < 3:
                        success += 1
                    else: 
                        # check if not 
                        fail += 1
                    
                        # check if fail
                        if fail == 5:
                            Text = "Access Denied"
                            fail = 1
                             

                            # route to failure pages
                    
                        # check if success      
                        if success == 3:
                            Text = "Access granted"
                            success = 1
                            fail=1
                            webbrowser.open(form_path)
                            # route to succes pages
                    
                        
                        
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
            cv2.putText(frame,Text,(x,y+h+30),cv2.FONT_HERSHEY_COMPLEX,1,(R,G,B),1)
            
            


            # Center coordinates
            center_coordinates = x + w // 2, y + h // 2
  
            # Radius of circle
            radius = w // 2
   
            # Blue color in BGR
            color = (R, G, B)
   
#            Line thickness of 2 px
            thickness = 3
            cv2.circle(frame, center_coordinates, radius, color, thickness)
            
            
        else:
            
            # If more than 1 faces 
            B, G, R = (255, 0, 0)
            Text = "More than 1 face is detected"
                  
        _, frame_encoded  = cv2.imencode('.png', frame)
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame_encoded.tobytes() + b'\r\n')