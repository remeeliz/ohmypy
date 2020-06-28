##################################################
## FileName: camera.py
##################################################
## Author: RDinmore, XWu
## Date: 2020.06.27
## Purpose: capture screen
## Libs: cv2, math
## Path: Flask_UI/camera.py
##################################################

import cv2
from math import fmod
from facedetect import *
from db_functions import *

class VideoCamera(object):
    def __init__(self, filename):
        self.video = cv2.VideoCapture(filename)
        self.i = 0

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        #self.i = self.i + 1

        #if fmod(self.i,50):
        #    insert_face(image_array["face"], "Unknown")

        image_array = facesquare(image)
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()