# Reverse-Vending-Machine
Reproducible Software Artifact for Cost Effective Reverse Vending Project

Our aim is to build a compact, cost-effective, and fraud-resistant reverse vending machine using minimalistic design. After 2021, our government will enact a container deposit legislation that will put monetary deposits on plastic, metal, glass, and carton containers. With this legislation, reverse vending machines will be ever more important and prevalent. Therefore, we wanted to be a part of the movement incentivizing a more sustainable life.

Our reverse vending machine uses AI-powered computer vision and a load cell to sort the containers. The computer vision algorithm classifies the containers into three categories (metal, plastic and carton) and the load cell checks whether they contain liquid or not. After accepting the containers, the machine transfers money to the user’s card.

## Files contained
1) ```main_main_flow.py``` includes the main functionality of the machine (classification, weight_check, storage, GUI).
2) ```main_main_flow.sh``` inclues the shell script for custom machine functionality.
3) ```ai.py``` includes the code for training image classification network and downloading TFLite file for Raspberry Pi 4 Module.
4) ```ai_train.sh``` includes a modifiable shell script for custom training.
5) ```ai_train_notebook.ipynb``` includes a google colab notebook for interactive ai training.
6) ```rasp_classify.py``` includes the functions to classify containers using PiCamera and AI.
6) ```dataset``` includes the dataset images for all classes.
7) ```motor.py``` includes the motor class for Rasberry Pi 4 functionality.
8) ```hx711.py``` includes the weight sensor class for Raspberry Pi 4 functionality. 
9) ```model.tflite``` includes the TFLite deep learning model. 
10) ```labels.txt``` includes the labels of the types of containers our machine classifies (large_plastic, large_carton, small_plastic, small_carton, metal).
11) ```test``` is a folder containing useful scripts for debugging and checking individual parts of the machine (```motor_check.py: ```, ```weight_sensor_check.py ```, ``` take_photo.py: ```, ```check_ai.py```).

## How to reproduce it
### Dataset
You can either use our dataset provided here or construct your own one. In order to construct one, you just need to take images of the classes of containers you would like your machine to classify and place each image into their respective class folders: (an example is shown below)
```
--> Dataset
    --> class_1
        --> image1.jpg (this is just an example, you can name your images whatever you wish)
        --> image2.jpg
        ...
    --> class_2
    --> class_3
    ...
```

### AI training
You can  either modify the paraneters in ```ai_train.sh``` for your own project or use ```ai_train_notebook.ipynb``` in order to interactively modify the training code: (specific instructions on how the code works are present in ```ai.py```)
```sh
$ bash ai_train.sh
```
After training you will have ```model.tflite``` and ```labels.txt``` files which are customized for your own training. Again, if you don't want custom training, you can just use the files we have provided here. 

### Raspberry Pi 4
Transfer all of your files into your Raspberry Pi 4. You must modify the parameters in ```main_main_flow.sh``` for the motors' and the weight sensor's GPIO pins and also the path to your project folder. After that, you can simply run  this command line and there you have yourself your own machine!! 
```sh
$ bash main_main_flow.sh
```
What's left to do is to assemble the mechanical pieces and you're done:) Save your environment! Promote recycling... for a better future!!
