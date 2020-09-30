# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 00:57:28 2020

@author: user
"""

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import re
import tensorflow as tf
import keras

#Data cleaning and preparing
stop_words= set(stopwords.words("english"))
lemma = WordNetLemmatizer()
news = pd.read_csv(r" news.csv")
data=news.drop(['Unnamed: 0'],axis=1)
TEXTdata=[]
TITLEdata=[]
for i in range(len(news)):
 data['text'].iloc[i] = re.sub('[^a-zAZ]',' ',data['text'].iloc[i]).lower()
 data['title'].iloc[i] = re.sub('[^a-zAZ]',' ',data['title'].iloc[i]).lower()

 textword = word_tokenize(data['text'].iloc[i])
 titleword = word_tokenize(data['title'].iloc[i])
 text=""
 title=""
 for w in textword:
 if w not in stop_words:
 wr = lemma.lemmatize(w)
 text=text+" "+wr
 for k in titleword:
 if k not in stop_words:
 kr = lemma.lemmatize(k)
 title=title+" "+kr
 TEXTdata.append(text)
 TITLEdata.append(title)
 
#Vectorisation of data to produce training data and labels
Y=[]
for i in range(len(data)):
 if data['label'].iloc[i] == 'FAKE':
 Y.append(1)
 elif data['label'].iloc[i] == 'REAL':
 Y.append(0)
 
#text to vector

cv=TfidfVectorizer()
X=cv.fit_transform(TEXTdata).toarray()

#Splitting data into train and test data in 80:20 ratio
Xtrain, Xtest, Ytrain, Ytest = train_test_split(X,Y,test_size=0.2)
#The deep learning classification model
from keras.callbacks import CSVLogger
csv_logger = CSVLogger('log.csv', append=True, separator=';')
##model
model=tf.keras.Sequential()
model.add(tf.keras.layers.Dense(1024,input_shape=(X.shape[1],),activati
on='relu'))
model.add(tf.keras.layers.BatchNormalization())
model.add(tf.keras.layers.Dropout(0.1))
model.add(tf.keras.layers.Dense(512,input_shape=(1024,),activation='rel
u'))
model.add(tf.keras.layers.BatchNormalization())
model.add(tf.keras.layers.Dropout(0.4))
model.add(tf.keras.layers.Dense(1024,input_shape=(512,),activation='rel
u'))
model.add(tf.keras.layers.BatchNormalization())
model.add(tf.keras.layers.Dropout(0.3))
model.add(tf.keras.layers.Dense(1,input_shape=(1024,),activation='sigmo
id'))
model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['acc
uracy'])
history=model.fit(Xtrain,np.array(Ytrain),batch_size=64 ,epochs=100)

# Plotting of training accuracy and cost curve
import matplotlib.pyplot as plt
plt.plot(history.history['accuracy'])
plt.title('Model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.show()
plt.plot(history.history['loss'])
plt.title('Model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.show()

# Evaluation of model on testing data
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
Ypred = model.predict(Xtest)
Ypred = (Ypred>0.5).astype(np.uint8)
CF = confusion_matrix(Ytest,Ypred)
print("Confusion matrix: \n",CF)
CLFR = classification_report(Ytest,Ypred)
print("Classification report: \n",CLFR)