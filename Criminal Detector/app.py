import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import cv2
import numpy as np
import matplotlib.pyplot as plt
from tensorflow import keras

app = Flask(__name__)
wsgi_app=app.wsgi_app

model=keras.models.load_model('faceDetector.h5')

@app.route('/', methods=['GET', 'POST'])
def hello():
    if request.method=='POST':
        file=request.files["file"]
        file.save(os.path.join('uploads', file.filename))
        path=os.path.join('uploads', file.filename)
        img=cv2.imread(path)
        img=cv2.resize(img,(128,128))
        img=img.reshape(-1,128,128,3)
        prediction=model.predict([img],verbose=1)
        val = np.argmax(prediction)
        
        return render_template("index.html",message=val)

    return render_template("index.html",message='success')

if __name__=='__main__':
    app.run(debug=True)