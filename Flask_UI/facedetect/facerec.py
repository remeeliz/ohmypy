##################################################
## FileName: facerc.py
##################################################
## Author: RDinmore
## Date: 2020.06.22
## Purpose: Get face image from aws file directory
## Libs: cv2
## LocalLibs: filestore
## Path: Flask_UI/facedetect
##################################################

from filestore import *
import cv2
import os
import base64

def get_fileext(filename):
    return filename.rsplit('.', 1)[1].lower()

def facesquare(image):
    dir = os.path.dirname(__file__)
    cascPath = os.path.join(dir,"haarcascade_frontalface_default.xml")
    # Create the haar cascade
    faceCascade = cv2.CascadeClassifier(cascPath)

    # Read the image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    startx = 0
    endx = 0
    starty = 0
    endy = 0
    face = image
    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        startx = x
        starty = y
        endx = x + w
        endy = y + h
        face = image[starty:endy, startx:endx]
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    return_val = {
        "face":face,
        "image":image,
        "num_face":len(faces)
    }

    return return_val

def image_binary(cv_imagearray, image_path):
    output_arrray = facesquare(cv_imagearray["image"])

    output_img = output_arrray["image"]
    output_face = output_arrray["face"]
    output_count = output_arrray["num_face"]

    retval, buffer = cv2.imencode('.jpg', output_img)
    jpg_as_text = base64.b64encode(buffer)
    jpg_as_text = str(jpg_as_text)[2:]
    html = "<html><img id='return_image' src='data:image/"+get_fileext(image_path)+";base64," + str(jpg_as_text) + "/></html>"

    img = {"html":html,
        "face":output_face,
        "image":output_img,
        "num_face":output_count}

    return img