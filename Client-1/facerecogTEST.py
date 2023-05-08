
import cv2
import numpy as np
import urllib.request




url='http://192.168.100.61/640x480.jpg' # esp url



def main() :
    


    
    while True:
        img_resp=urllib.request.urlopen(url)
        
        
        imgnp=np.array(bytearray(img_resp.read()),dtype=np.uint8)
        img=cv2.imdecode(imgnp,-1)
        
        # success, img = cap.read()
        frame = cv2.flip(img, 1) # Flip camera vertically

        
        cv2.imshow('Attendance check',frame)
        
        k = cv2.waitKey(30) & 0xff
        if k == 27: # press 'ESC' to quit
            break
        cv2.waitKey(1)
        

    cv2.destroyAllWindows
    
main()