# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 23:40:56 2020

@author: Asus
"""

import cv2
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import os
import keras
from tqdm import tqdm
IMG_HEIGHT=IMG_WIDTH=128
IMG_CHANNELS=3
    
inputs = tf.keras.layers.Input((IMG_HEIGHT, IMG_WIDTH, IMG_CHANNELS))
s = tf.keras.layers.Lambda(lambda x: x / 255)(inputs)


c1 = tf.keras.layers.Conv2D(16, (3, 3), kernel_initializer='he_normal', padding='same')(s)
c1 = tf.keras.layers.BatchNormalization()(c1)
c1 = tf.keras.layers.ReLU()(c1)
c1 = tf.keras.layers.Conv2D(32, (3, 3), kernel_initializer='he_normal', padding='same')(c1)
c1 = tf.keras.layers.BatchNormalization()(c1)
c1 = tf.keras.layers.ReLU()(c1)
c1 = tf.keras.layers.Dropout(0.1)(c1)
c1 = tf.keras.layers.Conv2D(16, (3, 3), kernel_initializer='he_normal', padding='same')(c1)
c1 = tf.keras.layers.BatchNormalization()(c1)
c1 = tf.keras.layers.ReLU()(c1)
p1 = tf.keras.layers.MaxPooling2D((2, 2))(c1)

c2 = tf.keras.layers.Conv2D(32, (3, 3), kernel_initializer='he_normal', padding='same')(p1)
c2 = tf.keras.layers.BatchNormalization()(c2)
c2 = tf.keras.layers.ReLU()(c2)
c2 = tf.keras.layers.Conv2D(64, (3, 3), kernel_initializer='he_normal', padding='same')(c2)
c2 = tf.keras.layers.BatchNormalization()(c2)
c2 = tf.keras.layers.ReLU()(c2)
c2 = tf.keras.layers.Dropout(0.1)(c2)
c2 = tf.keras.layers.Conv2D(32, (3, 3), kernel_initializer='he_normal', padding='same')(c2)
c2 = tf.keras.layers.BatchNormalization()(c2)
c2 = tf.keras.layers.ReLU()(c2)
p2 = tf.keras.layers.MaxPooling2D((2, 2))(c2)

c3 = tf.keras.layers.Conv2D(64, (3, 3), kernel_initializer='he_normal', padding='same')(p2)
c3 = tf.keras.layers.BatchNormalization()(c3)
c3 = tf.keras.layers.ReLU()(c3)
c3 = tf.keras.layers.Conv2D(128, (3, 3), kernel_initializer='he_normal', padding='same')(c3)
c3 = tf.keras.layers.BatchNormalization()(c3)
c3 = tf.keras.layers.ReLU()(c3)
c3 = tf.keras.layers.Dropout(0.2)(c3)
c3 = tf.keras.layers.Conv2D(64, (3, 3), kernel_initializer='he_normal', padding='same')(c3)
c3 = tf.keras.layers.BatchNormalization()(c3)
c3 = tf.keras.layers.ReLU()(c3)

L1 = tf.keras.layers.Flatten()(c3)
L1 = tf.keras.layers.Dense(32,kernel_initializer='he_normal',)(L1)
outputs= tf.keras.layers.Dense(1, activation='sigmoid')(L1)
model = tf.keras.Model(inputs=[inputs], outputs=[outputs])



model.load_weights('D:/project/sih/dd/accidentDetector.h5')



 
img=cv2.imread('imagee.jpg')
cv2.imshow("image",img)
img=cv2.resize(img,(128,128))
img=img.reshape(-1,128,128,3)
prediction = model.predict([img])
prediction = (prediction>0.5).astype(np.uint8)
if(prediction[0][0]==1):
    print("ACCIDENT the location of the CAM1 sent to the authorities")
elif(prediction[0][0]!=1):
    print("normal")
cv2.waitKey(0)
cv2.destroyAllWindows()











