# video_stream = openCV.video("Flask_UI/video/example.mp4")
# for once per second:
#     snap_shot = video_stream.captureImage()
#     os.run("FaceDetect/face-detect.py snap_shot > captured_face.jpg")

import cv2
import os
from face_detect_remee import face_detect

# vidcap = cv2.VideoCapture('/home/laspi/PycharmProjects/EigenFaceFilter/eigenface-filter/Flask_UI/video/LawyerCommercial.mp4')
# success, image = vidcap.read()
# count = 0
# while success:
#     cv2.imwrite('frames_vid/frame%d.jpg' % count, image)  # save frame as JPEG file
#     success, image = vidcap.read()
#     count += 1
#
# print(count)

dir = os.path.dirname(__file__)
img_dir = os.path.join(dir, 'frames_vid')

for root, dirs, files in os.walk(img_dir+"/"):
    for file in files:
        if file.endswith(".jpg"):
             print(os.path.join(root, file))
             face_detect(os.path.join(root, file))
#
