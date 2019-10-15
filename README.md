# Resmileder 

* Under development

A Python application that challenge you to be happy for 3 seconds every couple of hours. This is an application that I developed during 24 hours hackathon at University of Washington - Dubhack 2019. The idea is very simple, we had fitbit which remind us to stand up and walk around after a couple of hours, so Resmileder reminds you to smile. Smiling can trick your brain into believing you’re happy which can then spur actual feelings of happiness. 

### Dependencies

* Python 3.6, OpenCV 3 or 4, Tensorflow, TFlearn, Keras, tkinter

### Usage

* If you would like to use my pre-trained model, run ```python start.py --mode run```.

* Want to train your own model:

1. Download dataset from here: https://anonfile.com/bdj3tfoeba/data_zip
2. run ```python start.py --mode train```

### Algorithm

* Use haar cascade to detect faces in each frame of the webcam feed

* resized the region containing the face then passing it to the Convnet

* network outputs a list of softmax scores for the seven classes {Angry", "Disgusted","Fearful", "Happy", "Neutral", "Sad", "Surprised"}

* If the model predict face to be happy, then start count down the time

* Program stop when either user hit q or they "smile/or be happy" for 3 second ( This value can be changed)



### Todo:

* Fix bugs user face hang when they are happy lol . 
* Make the app run transparently, and "wake up" every couple of hours to remind user to smile
* Add database and flask server to potentially make it to be a web application. 


### Demo

* I was sucessfully happy for 3 seconds, the challenge is over
![Alt Text](ezgif.com-crop.gif)







