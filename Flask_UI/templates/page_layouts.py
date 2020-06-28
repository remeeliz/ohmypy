##################################################
## FileName: page_layouts.py
##################################################
## Author: RDinmore
## Date: 2020.06.22
## Purpose: return html to be displayed
## Libs: yattag, flask, urllib
## Path: Flask_UI/templates
##################################################

from yattag import Doc
from flask import url_for
import urllib.parse
import os
import sys
import pandas as pd

def get_page(page_name):
    doc, tag, text, line = Doc().ttl()
    doc.asis(header())

    if page_name == "data_page":
        doc.asis(view_data_page())
    elif page_name == "more_info":
        doc.asis(buttons())
        doc.asis(info_page())
    elif page_name == "learn_face":
        doc.asis(learn_face())
    else:
        doc.asis(buttons())        

    doc.asis(footer())
    return doc.getvalue()

def data_page(datatable):
    doc, tag, text, line = Doc().ttl()
    doc.asis(header())
    html = datatable.to_html()
    doc.asis(html)
    doc.asis(footer())
    return doc.getvalue()

def eval_face(response, image_name, output_count):
    doc, tag, text, line = Doc().ttl()
    doc.asis(header())
    doc.asis(footer())

    with tag('div', id='display_face'):
        with tag('div', id='photo-container'):
            doc.asis(response)
            doc.asis('</br>')
            doc.asis('</br>')
            text("Name: " +  urllib.parse.unquote_plus(image_name))
            doc.asis('</br>')
            text("Face count: " + str(output_count))
            doc.asis('</br>')
            doc.asis('</br>')
    doc.asis(footer())
    return doc.getvalue()

def info_page():
    doc, tag, text, line = Doc().ttl()
    with tag('div'):
        with tag('div', id='container'):
            with tag('div', id='display_info'):
                doc.asis('<div class="alert"><span class="closebtn" onclick="this.parentElement.style.display='+"'none'"+';">x</span>')
                text("This is a facial recognition media player. After selecting a media file the software will parse facial images and insert them into the database. ")
                text("These images will then be compared to current images and highlighted if recognized. The images will also be used to continue to grow the facial ")
                text("recognition data set.")
                text("")
                doc.asis('</div>')

    return doc.getvalue()

def footer():
    doc, tag, text, line = Doc().ttl()

    with tag('div', id='container'):
        with tag('div', id='photo-container'):
            with tag('form', id='menu'):
                with tag('footer'):
                    with tag('p'):
                        text("Developed for CIS4390")
                        doc.asis("<br>")
                        text("Developers: Remee A., Martin L., Luke O., Zihan S., Xinxin W.")

    return doc.getvalue()

def header():
    doc, tag, text, line = Doc().ttl()
    stylesheet = open(os.path.join(sys.path[0],"templates/stylesheet.txt"))

    with tag('html'):
        with tag('head'):
            doc.asis('<meta charset="utf-8"/>')
            with tag('title'):
                text('Oh My Py')
            with tag('style'):
                doc.asis(stylesheet.read())

    with tag('div', id='container'):
        doc.asis('<a href="'+url_for('home')+'"')
        with tag('div', id='photo-container'):
            doc.stag('img', src='https://raw.githubusercontent.com/remeeliz/ohmypy/master/header.JPG', id="header")
        doc.asis('</a>')

    return doc.getvalue()

def buttons():
    doc, tag, text, line = Doc().ttl()

    with tag('div', id='container'):
        with tag('div', id='photo-container'):
            with tag('form', id='menu'):
                doc.asis('<label id="button1" for="test" > SELECT MEDIA FILE </label><br>')
                doc.asis('<input type="file" id="test" accept="image/png, image/jpeg, video/mp4">')
            with tag('form', id='menu'):
                doc.asis('<button type="submit" id="button2" value="view_data"> MEDIA PLAYER SAMPLE </button>')
                doc.asis('<textarea name="content" id="hide" method="post">data_page</textarea>')
            with tag('form', id='menu'):
                doc.asis('<button type="submit" id="button4" value="learn_data"> LEARN FACE </button>')
                doc.asis('<textarea name="content" id="hide" method="post">learn_face</textarea>')
            with tag('form', id='menu'):
                doc.asis('<button type="submit" id="button5" value="database"> VIEW DATA </button>')
                doc.asis('<textarea name="content" id="hide" method="post">database</textarea>')
            with tag('form', id='menu'):
                doc.asis('<button type="submit" id="button3" value="more_info"> MORE INFO </button>')
                doc.asis('<textarea name="content" id="hide" method="post">more_info</textarea>')

    return doc.getvalue()

def view_data_page():    
    doc, tag, text, line = Doc().ttl()

    with tag('div', id='photo-container'):
        doc.asis('<iframe width="1000" height="500" src="'+url_for('video_feed')+'" frameborder="0" allowfullscreen></iframe>')
    return doc.getvalue()

def learn_face():
    doc, tag, text, line = Doc().ttl()
    with tag('div', id='container'):
        with tag('div', id='photo-container'):
            with tag('div'):
                text("Choose an image with a single face to train facial recognition")
                with tag('div', id='learn_face'):
                    doc.asis('<form method=post enctype=multipart/form-data>')
                    doc.asis('<label for="file-upload" class="custom-file-upload"><i class="fa fa-cloud-upload"></i>Choose File</label></br>')
                    doc.asis('<input type="file" name="file" id="file-upload" accept="image/png,image/jpeg" required></br></br>')
                    doc.asis('<input type="text" name="name_in" placeholder="Eigen Face" required>')
                    doc.asis('</br></br>')
                    doc.asis('<button type="submit" id="eval_button" value="Upload"> Evaluate </button>')
                    doc.asis('</form>')

    return doc.getvalue()