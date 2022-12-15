from time import sleep
from picamerax import PiCamera
import cv2


try:
    camera = PiCamera()
    camera.resolution = (1024, 768)
    camera.start_preview()
    # Camera warm-up time
    sleep(2)
    camera.capture('foo.jpg')
except OSError as e: # Not using a RPi
    cap = cv2.VideoCapture(0) # Set the first cam as your video source
    ret,frame = cap.read() # read() combines grab() and retrive() in a helper function 
    cv2.imwrite('images/c1.png',frame)
    # while(True):
    #     cv2.imshow('img1',frame) #display the captured image
    #     if cv2.waitKey(1) & 0xFF == ord('y'): #save on pressing 'y' 
    #         cv2.imwrite('images/c1.png',frame)
    #         cv2.destroyAllWindows()
    #         break

    cap.release()