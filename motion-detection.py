from time import sleep
import cv2
from cv2 import VideoCapture
import numpy as np



def has_motion(device):
    if isinstance(device, VideoCapture): #If we're working with a webcam
        ret,img_one = device.read()
        prepared_frame_one = cv2.cvtColor(img_one, cv2.COLOR_BGR2GRAY) #make gratscale
        prepared_frame_one = cv2.GaussianBlur(src=prepared_frame_one, ksize=(5,5), sigmaX=0) #Smooth a bit
        sleep(1)

        ret, img_two = device.read()
        prepared_frame_two = cv2.cvtColor(img_two, cv2.COLOR_BGR2GRAY) #make gratscale
        prepared_frame_two = cv2.GaussianBlur(src=prepared_frame_two, ksize=(5,5), sigmaX=0) #Smooth a bit
        
        diff_frame = cv2.absdiff(src1=prepared_frame_one, src2=prepared_frame_two)

        #Image processing magic I stole from https://towardsdatascience.com/image-analysis-for-beginners-creating-a-motion-detector-with-opencv-4ca6faba4b42
        kernel = np.ones((5, 5))
        diff_frame = cv2.dilate(diff_frame, kernel, 1)

        # play with the thresh kwarg to set threshold for motion detection
        thresh_frame = cv2.threshold(src=diff_frame, thresh=50, maxval=255, type=cv2.THRESH_BINARY)[1]
        moved_pixels = np.count_nonzero(thresh_frame)
        print(thresh_frame)

        #If > 10% of the pixels have motion... there is motion (0.1). We may want to play with this threshold as well
        ratio_moved = moved_pixels/thresh_frame.size
        print(ratio_moved)
        if ratio_moved < 0.1:
            return False
        else:
            return True
        

try:
    from picamerax import PiCamera
    camera = PiCamera()
    camera.resolution = (1024, 768)
    camera.start_preview()
    # Camera warm-up time
    sleep(2)
    camera.capture('images/test.png')
except OSError as e: # Not using a RPi
    cap = cv2.VideoCapture(0) # Set the first cam as your video source
    # ret,frame = cap.read() # read() combines grab() and retrive() in a helper function 
    # cv2.imwrite('images/test.png',frame)
    if has_motion(cap):
        print("I SEE SOMETHING! Taking a vdeo. SMILE!")
        #from https://www.learningaboutelectronics.com/Articles/How-to-record-video-Python-OpenCV.php
        width= int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height= int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        writer= cv2.VideoWriter('images/test.mp4', cv2.VideoWriter_fourcc(*'DIVX'), 20, (width,height))
        i=0
        while i<60: #We can swap this to while has_motion() maybe?
            i+=1
            ret,frame= cap.read()

            writer.write(frame)

            cv2.imshow('frame', frame)

            if cv2.waitKey(1) & 0xFF == 27: #if IO jam I think
                break

        writer.release()
        cv2.destroyAllWindows()
    else:
        print("I didn't see anything!")

    cap.release()
