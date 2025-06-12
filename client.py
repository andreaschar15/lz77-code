from flask import Flask, request, redirect, url_for, render_template
import tempfile
import shutil
import re
import json
import numpy as np
import cv2
import os
import sys
import subprocess
from lz77 import compress

app = Flask(__name__)


def image2bstream(image):
    _, enc_img = cv2.imencode('.png', image)
    return enc_img.tobytes()

@app.route("/")
def index():
    return render_template('upload.html')

@app.route("/compress", methods=['POST','GET'])
def compress_img():
    # gets the image filepath
    file = request.files['image']

    # converst it to numpy array
    filestr = file.read()
    npimg = np.frombuffer(filestr, np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    imginbytes = image2bstream(img)

    #sage_script = os.path.join(os.path.dirname(__file__), 'lz77.sage')

    byte_len = len(imginbytes)

    result = compress(imginbytes, byte_len)

    return result

if __name__ == '__main__':
    app.run(debug=True)

