##################################################
## FileName: main.py
##################################################
## Author: RDinmore, XWu
## Date: 2020.06.22
## Purpose: server main page
## Libs: flask, datetime
## LocalLibs: templates, database, camera, filestore
## Path: Flask_UI/filestore
##################################################

from flask import Flask, render_template, request, Response, make_response, flash, request, redirect, url_for, send_from_directory
import cv2
import os
import appconfig as cfg
from templates import *
from database import *
from datetime import timedelta
from camera import VideoCamera
from filestore import *
from facedetect import *
from db_functions import *
from werkzeug.utils import secure_filename
import base64

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = cfg.UPLOAD_FOLDER
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=3)
app.config['SECRET_KEY'] = cfg.SECRET_KEY

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def home():
    url_get = request.args.get('content')
    if url_get == 'database':
        return data_page(get_data())
    else:
        return get_page(url_get)

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera('https://ohmypy-summer2020.s3.amazonaws.com/videos/LibertyMutualInsuranceCommercial.mp4')),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# this is a test for facial recognition
@app.route('/test')
def process():
    #this will search in the s3 for any files with the name steve and return top path
    image_path = get_s3object("Steve")
    #this transforms the image into a cv image for facedetect
    image = get_cvimage(image_path)
    output_array = image_binary(image, image_path)

    image_name = 'Steve Carell'
    insert_face(output_array["image"], image_name)
    return eval_face(output_array["html"], image_name, output_array["num_face"])


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    name_in = '/' + request.form['name_in']
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            file_type = '/' + get_fileext(file.filename)
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',filename=filename,name=name_in,filetype=file_type))

@app.route('/uploads/<filename>/<name>/<filetype>')
def uploaded_file(filename,name,filetype):
    filename = app.config['UPLOAD_FOLDER'] + "/" + filename

    image_file = gettemp_cvimage(filename)
    image = facesquare(image_file)
    output_array = image_binary(image, filename)

    insert_face(output_array["image"], name)
    return eval_face(output_array["html"], name, output_array["num_face"])

if __name__ == "__main__":
    app.run(debug=True)

