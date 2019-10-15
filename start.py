import numpy as np
import argparse
import cv2
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Flatten
from keras.layers.convolutional import Conv2D
from keras.optimizers import Adam
from keras.layers.pooling import MaxPooling2D
from keras.preprocessing.image import ImageDataGenerator
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Progressbar
 
from tkinter import ttk

 
import os
import time

import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt

# command line argument
ap = argparse.ArgumentParser()
ap.add_argument("--mode",help="train/display")
a = ap.parse_args()
mode = a.mode 

SMILE_TIME = 3
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Define data generators
# train_dir = 'data/train'
# val_dir = 'data/test'

# num_train = 28709
# num_val = 7178
# batch_size = 64
# num_epoch = 50

# train_datagen = ImageDataGenerator(rescale=1./255)
# val_datagen = ImageDataGenerator(rescale=1./255)

# train_generator = train_datagen.flow_from_directory(
#         train_dir,
#         target_size=(48,48),
#         batch_size=batch_size,
#         color_mode="grayscale",
#         class_mode='categorical')

# validation_generator = val_datagen.flow_from_directory(
#         val_dir,
#         target_size=(48,48),
#         batch_size=batch_size,
#         color_mode="grayscale",
#         class_mode='categorical')

# Create the model
model = Sequential()

model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(48,48,1)))
model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(1024, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(7, activation='softmax'))

# Creating UI Window
window = Tk()
window.title("Welcome to LikeGeeks app")
window.geometry('350x200')
style = ttk.Style()
 
style.theme_use('default')
 
style.configure("black.Horizontal.TProgressbar", background='black')
bar = Progressbar(window, length=200, style='black.Horizontal.TProgressbar')



def train():
    # Define data generators
    # train_dir = 'data/train'
    # val_dir = 'data/test'

    # num_train = 28709
    # num_val = 7178
    # batch_size = 64
    # num_epoch = 50

    # train_datagen = ImageDataGenerator(rescale=1./255)
    # val_datagen = ImageDataGenerator(rescale=1./255)

    # train_generator = train_datagen.flow_from_directory(
    #         train_dir,
    #         target_size=(48,48),
    #         batch_size=batch_size,
    #         color_mode="grayscale",
    #         class_mode='categorical')

    # validation_generator = val_datagen.flow_from_directory(
    #         val_dir,
    #         target_size=(48,48),
    #         batch_size=batch_size,
    #         color_mode="grayscale",
    #         class_mode='categorical')

    model.compile(loss='categorical_crossentropy',optimizer=Adam(lr=0.0001, decay=1e-6),metrics=['accuracy'])

    model_info = model.fit_generator(
            train_generator,
            steps_per_epoch=num_train // batch_size,
            epochs=num_epoch,
            validation_data=validation_generator,
            validation_steps=num_val // batch_size)

    plot_model_history(model_info)
    model.save_weights('model.h5')
    


# If you want to train the same model or try other models, go for this
if mode == "train":
    train()

# emotions will be displayed on your face from the webcam feed
elif mode == "display":
    model.load_weights('model.h5')

    # prevents openCL usage and unnecessary logging messages
    cv2.ocl.setUseOpenCL(False)

    # dictionary which assigns each label an emotion (alphabetical order)
    emotion_dict = {0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}

    # start the webcam feed
    cap = cv2.VideoCapture(0)
    curr_emoj = ''
    not_being_happy = True
    start_time = 0
    user_done = False
    while True:
        # Find haar cascade to draw bounding box around face
        if user_done:
            messagebox.showinfo('Congratulation', 'You did it')
            break
        if curr_emoj == 'Happy'  :
            start_time = time.time() # Start calculate happy time
            elapsed = 0
            while curr_emoj == 'Happy':
                bar['value'] = elapsed / SMILE_TIME * 100
                bar.grid(column=0, row=0)
                window.mainloop()

                """
                    Really need to refactor the code here
                """
                if elapsed >= SMILE_TIME:
                    user_done = True
                    break
                
                ret, frame = cap.read()
                facecasc = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = facecasc.detectMultiScale(gray,scaleFactor=1.3, minNeighbors=5)

                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y-50), (x+w, y+h+10), (255, 0, 0), 2)
                    roi_gray = gray[y:y + h, x:x + w]
                    cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray, (48, 48)), -1), 0)
                    prediction = model.predict(cropped_img)
                    maxindex = int(np.argmax(prediction))
                    curr_emoj = emotion_dict[maxindex]
                
                    cv2.putText(frame, emotion_dict[maxindex], (x+20, y-60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

                elapsed = time.time() - start_time
                print (elapsed)
                cv2.imshow('Video', cv2.resize(frame,(1000, 700),interpolation = cv2.INTER_CUBIC))
                
            
            
        else: 
            ret, frame = cap.read()
            if not ret:
                break
            facecasc = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = facecasc.detectMultiScale(gray,scaleFactor=1.3, minNeighbors=5)

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y-50), (x+w, y+h+10), (255, 0, 0), 2)
                roi_gray = gray[y:y + h, x:x + w]
                cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray, (48, 48)), -1), 0)
                prediction = model.predict(cropped_img)
                maxindex = int(np.argmax(prediction))
                curr_emoj = emotion_dict[maxindex]
            
                cv2.putText(frame, emotion_dict[maxindex], (x+20, y-60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        
            cv2.imshow('Video', cv2.resize(frame,(1000, 700),interpolation = cv2.INTER_CUBIC))
        
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()