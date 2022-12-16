from time import sleep
import cv2
from cv2 import VideoCapture
import numpy as np


def _prep_image(frame):
    prepared_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #make gratscale
    return cv2.GaussianBlur(src=prepared_frame, ksize=(5,5), sigmaX=0) #Smooth a bit

def has_motion(prepared_frame_one, prepared_frame_two):
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


def device_has_motion(device):
    if isinstance(device, VideoCapture): #If we're working with a webcam
        ret,img_one = device.read()
        prepared_frame_one = _prep_image(img_one)
        sleep(1)

        ret, img_two = device.read()
        prepared_frame_two = _prep_image(img_two)
        return has_motion(prepared_frame_one, prepared_frame_two)
        
def frame_blurred(image):
    # Determine the variance of laplacian
    # image = cv2.imread("images/test.png")
    try:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        lap_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        print(lap_var)
        if lap_var > 30:
            return False
        else:
            return True
    except:
        return True


def sample_video(video_path):
    video = cv2.VideoCapture(video_path)
    fps = video.get(cv2.CAP_PROP_FPS)
    frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)
    
    samples = []
    i = 1
    while i < frame_count:
        i+=1
        video.set(cv2.CAP_PROP_POS_FRAMES, i)
        ret, frame = video.read()
        frame_blurred(frame)
        if not frame_blurred(frame):
            samples.append(frame)
    return samples

def save_to_disk(samples):
    # We may want to downsample even more if we get a lot of "good" samples
    for i, frame in enumerate(samples):
        cv2.imwrite(f"images/frame{i}.jpg", frame)

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

    if device_has_motion(cap):
        print("I SEE SOMETHING! Taking a vdeo. SMILE!")
        #from https://www.learningaboutelectronics.com/Articles/How-to-record-video-Python-OpenCV.php
        width= int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height= int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        writer = cv2.VideoWriter('images/test.mp4', cv2.VideoWriter_fourcc(*'DIVX'), 20, (width,height))
        motion = True
        i = 1
        ret, past_frame=  cap.read()

        while motion:
            ret,frame= cap.read()
            if i%30 == 0: #every 30 frames, check if there's still motion
                past_prepped = _prep_image(past_frame)
                current_prepped = _prep_image(frame)
                motion = has_motion(past_prepped, current_prepped)
                past_frame = frame

            writer.write(frame)
            # cv2.imshow('frame', frame)

            if cv2.waitKey(1) & 0xFF == 27: #if IO jam I think
                break
            i+=1

        writer.release()
        cv2.destroyAllWindows()
        samples = sample_video('images/test.mp4')
        save_to_disk(samples)
    else:
        print("I didn't see anything!")
    cap.release()
