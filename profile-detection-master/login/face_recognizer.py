#!/usr/bin/python

# Import the required modules
import cv2, os
import cStringIO
import numpy as np
import sys
from PIL import Image
from binascii import a2b_base64
import base64 
import re
import urllib


# For face detection we will use the Haar Cascade provided by OpenCV.
cascadePath = "login/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)

# For face recognition we will the the LBPH Face Recognizer 
recognizer = cv2.face.createLBPHFaceRecognizer(threshold=60.0)
# recognizer = cv2.face.createLBPHFaceRecognizer(threshold=50.0)

def get_images_and_labels(path):
    # Append all the absolute image paths in a list image_paths
    # We will not read the image with the .sad extension in the training set
    # Rather, we will use them to test our accuracy of the training
    image_paths = [os.path.join(path, f) for f in os.listdir(path) if not f.endswith('.DS_Store')]
    # print image_paths
    # images will contains face images
    images = []
    # labels will contains the label that is assigned to the image
    labels = []
    # print image_paths
    for image_path in image_paths:
        # Read the image and convert to grayscale
        image_pil = Image.open(image_path).convert('L')
        # Convert the image format into numpy array
        image = np.array(image_pil, 'uint8')
        # Get the label of the image
        nbr = int(os.path.split(image_path)[1].split(".")[0].replace("subject", ""))
        # Detect the face in the image
        faces = faceCascade.detectMultiScale(image)
        # If face is detected, append the face to images and the label to labels
        # i=1
        print image_path 
        images.append(image)
        labels.append(nbr)

        # for (x, y, w, h) in faces:
        #     images.append(image)
        #     # images.append(image[y: y + h, x: x + w])
        #     labels.append(nbr)
            
        #     # cv2.imshow("Adding faces to traning set...", image[y: y + h, x: x + w])
        #     # START: crop image to there faces
        #     # i= i+1
        #     # temp_image_path = "yalefaces/subject03-" + str(i) +".gif"
        #     # cv2.imshow("Adding faces to traning set...", image)
        #     image_pil =image_pil.crop((x, y, x+w, y + h))
        #     image_pil.save(image_path)
        #     # image_pil.save(temp_image_path)
        #     # END: 
        #     # cv2.waitKey(50)
    # return the images list and labels list
    print labels
    return images, labels


def init():
    # Path to the Yale Dataset
    path = 'login/yalefaces'
    # Call the get_images_and_labels function and get the face images and the 
    # corresponding labels
    images, labels = get_images_and_labels(path)
    cv2.destroyAllWindows()

    # Perform the tranining
    recognizer.train(images, np.array(labels))

# init()

def checkImg(imgurl):
    # print imgurl
    image_pil = cv2.imread(imgurl)

    image = np.array(image_pil, 'uint8')

    faces = faceCascade.detectMultiScale(
        image,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags = cv2.CASCADE_SCALE_IMAGE
    )

    # print "Found {0} faces!".format(len(faces))
    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        crop = image_pil[y:y+h, x:x+w]
        crop = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
        img = np.array(crop, 'uint8')
        file = imgurl
        # cv2.imwrite(file, crop)
        flag = recognizerImg(img)
        print flag
    return flag

def recognizerImg(img):
    # recognizer.h
    # START: code for recoganize the image 
    # predict_image_pil = Image.open('test.png').convert('L')
    # predict_image = np.array(predict_image_pil, 'uint8')
    predict_image = img
    nbr_predicted=  recognizer.predict(predict_image)
    # nbr_predicted, conf = recognizer.predict(predict_image)
    print "{} is Correctly Recognized with confidence {}", nbr_predicted
    # END: 
    return nbr_predicted

# START: conver the img from client and feed to recognizerImg()
def startAppWithImg(imgUri):
    # data = imgUri
    # png_recovered = base64.decodestring(data)

    # # binary_data = a2b_base64(data)
    # fd = open('image1.png', 'wb')
    # fd.write(png_recovered)
    # fd.close()
    # img = a2b_base64(data)
    url = urllib.unquote(imgUri).decode('utf8')
    print "START : url submitted "
    # print url
    image_data = re.sub('^data:image/.+;base64,', '', url).decode('base64')
    # print image_data
    image_pil = Image.open(cStringIO.StringIO(image_data)).convert('L')
    image_pil.save('test.png')
    image_pil = cv2.imread("test.png")

    print " END : url submitted "
    image = np.array(image_pil, 'uint8')

    # pic = cStringIO.StringIO()
    # image_string = cStringIO.StringIO(base64.b64decode(imgUri)
    # image = Image.open(image_string)
    # image.save(pic, image.format, quality = 100)
    # pic.seek(0)


    # Read the image
    # image = cv2.imread(image_string)
    # image = cv2.imread('image.png')
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = faceCascade.detectMultiScale(
        image,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags = cv2.CASCADE_SCALE_IMAGE
    )

    # print "Found {0} faces!".format(len(faces))
    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        # pt1 = (int(x), int(y))
        # pt2 = (int(x + w), int(y + h))
        crop = image_pil[y:y+h, x:x+w]
        crop = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
        img = np.array(crop, 'uint8')
        file = "test.png"
        cv2.imwrite(file, crop)
        # frame = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        # cv2.waitKey(50)
        flag = recognizerImg(img)
        print flag
        # if flag>0:
            # break
    return flag
# END: conver the img from client and feed to recognizerImg()



# START: get the image from the web cam
def startApp():
    # recognizerImg()
    print "app started"
    video_capture = cv2.VideoCapture(0)
    print "viedo started"
    # crop = vis[0:1, 0:1]
    flag =0
                
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
            img = np.array(crop, 'uint8')
            file = "test_image.png"
            cv2.imwrite(file, crop)
            frame = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.waitKey(50)
            flag = recognizerImg(img)


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


        if flag > 0:
            break

    # When everything is done, release the capture
    cv2.waitKey(500)

    video_capture.release()
    cv2.destroyAllWindows()
    return flag


# END: get the image form the web cam


# Append the images with the extension .sad into image_paths
# image_paths = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.sad')]
# for image_path in image_paths:
# predict_image_pil = Image.open('yalefaces/subject01.sad.gif').convert('L')
# predict_image = np.array(predict_image_pil, 'uint8')
# faces = faceCascade.detectMultiScale(predict_image)
# print faces
# for (x, y, w, h) in faces:
#     nbr_predicted, conf = recognizer.predict(predict_image[y: y + h, x: x + w])
#     nbr_actual = int(os.path.split(image_path)[1].split(".")[0].replace("subject", ""))
#     if nbr_actual == nbr_predicted:
#         print "{} is Correctly Recognized with confidence {}".format(nbr_actual, conf)
#     else:
#         print "{} is Incorrect Recognized as {}".format(nbr_actual, nbr_predicted)
#     cv2.imshow("Recognizing Face", predict_image[y: y + h, x: x + w])
#     cv2.waitKey(1000)
