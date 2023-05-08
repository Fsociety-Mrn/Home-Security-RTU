import cv2

camera = cv2.VideoCapture(0)
camera.set(4,1080)


while True:
    
    ret, frame = camera.read()
        
    if not ret:
        break
    
    cv2.imshow('asdasd',frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
