# Main script
import cv2

from JoloRecognition import JoloRecognition as Jolo


# face detection
face_detector=cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Set up the camera
cap = cv2.VideoCapture(0)
cap.set(4,1080)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 400)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 400)
cap.set(cv2.CAP_PROP_FPS, 36)

# Start streaming the camera
while True:   
    
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # rgb = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
    
    # Detect faces in the frame
    faces = face_detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=20, minSize=(100, 100), flags=cv2.CASCADE_SCALE_IMAGE)
    
    for (x, y, w, h) in faces:
        face = frame[y:y+h, x:x+w]
        
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2) 
        
        # get the result of Face_Compare script
        result = Jolo().Face_Compare(frame,threshold=0.6)

        
        cv2.putText(frame,str(result[0]),(x,y+h+30),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,255),1)


    cv2.imshow('Frame', frame)

    # Break the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close the window
cap.release()
cv2.destroyAllWindows()
