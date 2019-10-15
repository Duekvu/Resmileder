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


### Todo:

* Make the app run transparently, and "wake up" every couple of hours to remind user to smile
* Add database and flask server to potentially make it to be a web application. 



