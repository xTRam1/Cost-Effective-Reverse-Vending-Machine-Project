# Reverse-Vending-Machine
Reproducible Software Artifact for Reverse Vending Project

Our reverse vending machine uses AI-powered computer vision and a load cell to sort the containers. The computer vision algorithm classifies the containers into three categories (metal, plastic and carton) and the load cell checks whether they contain liquid or not. After accepting the containers, the machine transfers money to the user’s card.

Files contained:

1) ```gui.py``` includes the Graphical User Interface (GUI) of the machine. [Work in Progress]
2) ```ai.py``` includes the code for training image classification network and downloading TFLite file for Raspberry Pi 4 Module. [Completed]
3) ```functions.py``` includes the code for essential functions: ```classify```, ```transaction```, ```val_weight```. [Work in Progress]
4) ```motor.py``` includes the motor class for Rasberry Pi 4 functionality. [Completed]

