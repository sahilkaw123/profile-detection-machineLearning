import cv2
import sys
import numpy as np
from PIL import Image


 
# Captures a single image from the camera and returns it in PIL format
def get_image():
 # read is the easiest way to get a full image out of a VideoCapture object.
 retval, im = camera.read()
 return im
 

cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)

video_capture = cv2.VideoCapture(0)
# crop = vis[0:1, 0:1]
            
while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        pt1 = (int(x), int(y))
        pt2 = (int(x + w), int(y + h))
        crop = frame[y:y+h, x:x+w]
        crop = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
        file = "test_image.png"
        cv2.imwrite(file, crop)
        frame = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # if faces:
    # retval, im = camera.read()
    # camera_capture = frame

    # file = "test_image.png"
    # A nice feature of the imwrite method is that it will automatically choose the
    # correct format based on the file extension you provide. Convenient!
    # cv2.imwrite(file, camera_capture)
    

    # print crop
    # cv2.imshow("crop",crop)
    # Display the resulting frame
    cv2.imshow('Video', frame)
    # cv2.imshow('frame', gray)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()

image_pil = Image.open("test_image.png").convert('L')
image = np.array(image_pil, 'uint8')
faces = faceCascade.detectMultiScale(image)
for (x, y, w, h) in faces:
    image_pil =image_pil.crop((x, y, x+w, y + h))
    image_pil.save("yalefaces/subject03.gif")
    cv2.waitKey(50)







