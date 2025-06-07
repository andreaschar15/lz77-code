from flask import Flask, request, render_template, redirect, url_for, jsonify
import numpy as np
import cv2

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
    img_path = request.files['image']

    # converst it to numpy array
    filestr = img_path.read()
    npimg = np.frombuffer(filestr, np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    imginbytes = image2bstream(img)
    print(len(imginbytes))
    #print(str(imginbytes))
    return str(imginbytes)


if __name__ == '__main__':
    app.run(debug=True)

