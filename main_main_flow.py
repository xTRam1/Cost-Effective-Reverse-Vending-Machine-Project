"""
This document specificies the main flow 
"""

import tensorflow as tf

from motor import Motor
from hx711 import HX711
from rasp_classify import classify, load_labels

import picamera
import time
import PIL.Image
import numpy as np
import argparse
from tkinter import *
import RPi.GPIO as GPIO

total_price = 0.00

def main_flow(args, hx, motorT, motor1, motor2, labels, interpreter, lamp):
    LARGEFONT =("Verdana", 20)

    root = Tk()
    root.attributes('-fullscreen', True)

    # Recycle_Frame
    recycle_frame = Frame(root, padx=10, pady=50)
    recycle_frame.grid(row=0, column=0)
    recycle_header = Label(recycle_frame, font=LARGEFONT, text="Tap the Recycle button \n when you have placed your \n container into the machine", padx=25, pady=25, fg="#6CBA6D")      
    recycle_header.grid(row=0, column=0, columnspan=3)
    recycle_button = Button(recycle_frame, font=LARGEFONT, text="Recycle", command=lambda: recycle_flow(args, hx, motorT, motor1, motor2, total_price, result_label, recycle_label, interpreter, labels, lamp, transaction_label), padx=25, pady=25, bg="#6CBA6D", fg="#FFFFFF") 
    recycle_button.grid(row=1, column=1)
    result_label = Label(recycle_frame, font=('Verdana', 20), text="", padx=5, pady=5, fg="#6CBA6D")
    result_label.grid(row=2, column=1)
    recycle_label = Label(recycle_frame, font=LARGEFONT, text="Recycle Count: " + "{:.2f}".format(total_price) + " TL", padx=25, pady=25, fg="#6CBA6D")
    recycle_label.grid(row=3, column=1)

    # Dial_frame
    dial_frame = Frame(root, padx=10, pady=50)
    dial_frame.grid(row=0, column=1)

    dial_header = Label(dial_frame, font=LARGEFONT, text="Type your student number belove \n when you have finished recycling \n and tap the OK button", padx=25, pady=10, fg="#CF9A3F")
    dial_header.grid(row=0, column=0, columnspan=3)

    dial_screen = Label(dial_frame, font=LARGEFONT, text='', padx=25, pady=10, fg="#CF9A3F")
    dial_screen.grid(row=1, column=0, columnspan=3)

    button_1 = Button(dial_frame, text="1", height=2, width=5, command=lambda: dial('1', transaction_label, dial_screen), bg="#CF9A3F", fg="#000000") 
    button_2 = Button(dial_frame, text="2", height=2, width=5, command=lambda: dial('2', transaction_label, dial_screen), bg="#CF9A3F", fg="#000000")
    button_3 = Button(dial_frame, text="3", height=2, width=5, command=lambda: dial('3', transaction_label, dial_screen), bg="#CF9A3F", fg="#000000")
    button_4 = Button(dial_frame, text="4", height=2, width=5, command=lambda: dial('4', transaction_label, dial_screen), bg="#CF9A3F", fg="#000000")
    button_5 = Button(dial_frame, text="5", height=2, width=5, command=lambda: dial('5', transaction_label, dial_screen), bg="#CF9A3F", fg="#000000")
    button_6 = Button(dial_frame, text="6", height=2, width=5, command=lambda: dial('6', transaction_label, dial_screen), bg="#CF9A3F", fg="#000000")
    button_7 = Button(dial_frame, text="7", height=2, width=5, command=lambda: dial('7', transaction_label, dial_screen), bg="#CF9A3F", fg="#000000")
    button_8 = Button(dial_frame, text="8", height=2, width=5, command=lambda: dial('8', transaction_label, dial_screen), bg="#CF9A3F", fg="#000000")
    button_9 = Button(dial_frame, text="9", height=2, width=5, command=lambda: dial('9', transaction_label, dial_screen), bg="#CF9A3F", fg="#000000")
    button_0 = Button(dial_frame, text="0", height=2, width=5, command=lambda: dial('0', transaction_label, dial_screen), bg="#CF9A3F", fg="#000000")

    button_1.grid(row=2, column=0)
    button_2.grid(row=2, column=1)
    button_3.grid(row=2, column=2)

    button_4.grid(row=3, column=0)
    button_5.grid(row=3, column=1)
    button_6.grid(row=3, column=2)

    button_7.grid(row=4, column=0)
    button_8.grid(row=4, column=1)
    button_9.grid(row=4, column=2)

    button_0.grid(row=5, column=1)

    ok_button = Button(dial_frame, text='OK', command=lambda: ok(total_price, transaction_label, dial_screen, result_label, recycle_label), height=1, width=3, bg="#CF9A3F", fg="#000000")
    ok_button.grid(row=5, column=2)

    remove_button = Button(dial_frame, text='<--', command=lambda: remove(dial_screen), height=1, width=3, bg="#CF9A3F", fg="#000000")
    remove_button.grid(row=5, column=0)

    transaction_label = Label(dial_frame, font=("Verdana", 15), text="", fg="#7B8D93")
    transaction_label.grid(row=6, column=0, columnspan=3)

    root.mainloop()

def dial(number, transaction_label, dial_screen):
	transaction_label['text'] = ''
	dial_screen['text'] = dial_screen['text'] + number

def recycle_flow(args, hx, motorT, motor1, motor2, total_price, result_label, recycle_label, interpreter, labels, lamp, transaction_label):    
    """
    Main recycle function. Does the classification, weight check, and seperator movement.
    """
    transaction_label['text'] = ''
    object_name = classify(args, labels, interpreter, lamp)
    if object_name == None:
        result_label['text'] = "Rejected"
        return 

    weight = hx.get_weight(args.num_weight)
    if not check_weight(args, weight, object_name):
        result_label['text'] = "Rejected"
        return 

    move_motors(args, object_name, motorT, motor1, motor2)
    
    global total_price
    total_price = total_price + float(args.price_map[object_name])
    result_label['text'] = 'Accepted'
    recycle_label['text'] = "Recycle Count: " + "{:.2f}".format(total_price) + " TL"
    return 

def move_motors(args, object_name, motorT, motor1, motor2):
    if object_name == 'large_carton' or object_name == 'small_carton':
        motor1.forward(int(args.motor1_speed['forward']), args.motor1_time_forward)
        motor1.stop()
        motorT.forward(int(args.motorT_speed['forward']), args.motorT_time)
        motorT.stop()
        motorT.backward(int(args.motorT_speed['backward']), args.motorT_time)
        motorT.stop()
        motor1.backward(int(args.motor1_speed['backward']), args.motor1_time_backward)
        motor1.stop()
    elif object_name == 'metal':
        motor2.forward(int(args.motor2_speed['forward']), args.motor2_time_forward)
        motor2.stop()
        motorT.forward(int(args.motorT_speed['forward']), args.motorT_time)
        motorT.stop()
        motorT.backward(int(args.motorT_speed['backward']), args.motorT_time)
        motorT.stop()
        motor2.backward(int(args.motor2_speed['backward']), args.motor2_time_backward)
        motor2.stop()
    elif object_name =='large_plastic' or object_name == 'small_plastic':
        motorT.forward(int(args.motorT_speed['forward']), args.motorT_time)
        motorT.stop()
        motorT.backward(int(args.motorT_speed['backward']), args.motorT_time)
        motorT.stop()
  
def check_weight(args, weight, object_name):
    if weight < float(args.weight_map[object_name]) - float(args.weight_uncertainty_map[object_name]): 
        print(float(args.weight_map[object_name]) - float(args.weight_uncertainty_map[object_name]))
        return False
    elif weight > float(args.weight_map[object_name]) + float(args.weight_uncertainty_map[object_name]):
        print(float(args.weight_map[object_name]) + float(args.weight_uncertainty_map[object_name]))
        return False
    else:
        return True

def ok(total_price, transaction_label, dial_screen, result_label, recycle_label):
	if total_price == 0:
		transaction_label['text'] = "You haven't recycled. Try again."
		return
	if dial_screen['text'] == '':
		transaction_label['text'] = "Plase enter your student number first."
		return	
	result_label['text'] = ''
	dial_screen['text'] = ''
	transaction_label['text'] = "Transaction Completed. Thank you."
	total_price = 0.0
	recycle_label['text'] = "Rcycle Count: " + "{:.2f}".format(total_price) + " TL"

def remove(dial_screen):
    dial_screen['text'] = dial_screen['text'][:-1]

class ParseKwargs(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, dict())
        for value in values:
            key, value = value.split('=')
            getattr(namespace, self.dest)[key] = value

if __name__ == "__main__":
    
    # Arguments
    parser = argparse.ArgumentParser()
    
    # AI
    parser.add_argument(
        '--labels_file', 
        type=str,
        default='',
        help='file path for the file containing the labels for AI')
    parser.add_argument(
        '--model_file', 
        type=str,
        default='',
        help='file path for the TensorFlowLite model')
    parser.add_argument(
        '--min_prob', 
        type=float,
        default=0.8,
        help='minimum probability for acceptance')
    
    # Weight Sensor
    parser.add_argument(
        '--weight_sensor_pins', 
        nargs='+',
        type=int,
        help='GPIO pins for the weight sensor')
    parser.add_argument(
        '--weight_sensor_reference_unit', 
        type=int,
        default=1,
        help='Reference unit for the weight sensor')
    parser.add_argument(
        '--num_weight', 
        type=int,
        default=3,
        help='number of times load cell takes measures and takes the median.')
    parser.add_argument(
        '--weight_map', 
        nargs='*', 
        action=ParseKwargs,
        help='dictionary for the weights of the objects')
    parser.add_argument(
        '--weight_uncertainty_map', 
        nargs='*', 
        action=ParseKwargs,
        help='uncertainty for weight measurements.')
    
    # Motors
    # Pins
    parser.add_argument(
        '--motorT_pins', 
        nargs='+',
        type=int,
        help='pins of T-seperator motor')
    parser.add_argument(
        '--motor1_pins', 
        nargs='+',
        type=int,
        help='pins of first motor')
    parser.add_argument(
        '--motor2_pins', 
        nargs='+',
        type=int,
        help='pins of second motor')
    parser.add_argument(
        '--lamp_pins', 
        nargs='+',
        type=int,
        help='pins of the lamp')
    
    # Times
    parser.add_argument(
        '--motor1_time_forward', 
        type=float,
        default=1,
        help='How long first motor will work')
    parser.add_argument(
        '--motor2_time_forward', 
        type=float,
        default=1,
        help='How long second motor will work')
    parser.add_argument(
        '--motor1_time_backward', 
        type=float,
        help='How long first motor will work')
    parser.add_argument(
        '--motor2_time_backward', 
        type=float,
        help='How long second motor will work')
    parser.add_argument(
        '--motorT_time', 
        type=float,
        default=1,
        help='How long T-seperator motor will work')
    
    # Speeds
    parser.add_argument(
        '--motorT_speed', 
        nargs='*', 
        action=ParseKwargs,
        help='Speed of the T-seperator motor')
    parser.add_argument(
        '--motor1_speed', 
        nargs='*', 
        action=ParseKwargs, 
        help='Speed of the first motor.')
    parser.add_argument(
        '--motor2_speed', 
        nargs='*', 
        action=ParseKwargs,
        help='Speed of the second motor.')
    
    # Transaction
    # dictionary
    parser.add_argument(
        '--price_map', 
        nargs='*', 
        action=ParseKwargs,
        help='Price for each class.')
    args = parser.parse_args()

    # Initiations (HX711, motorT, motor1, motor2)
    hx = HX711(args.weight_sensor_pins[0], args.weight_sensor_pins[1])
    hx.set_reading_format("MSB", "MSB")
    hx.set_reference_unit(args.weight_sensor_reference_unit)
    hx.reset()
    hx.tare()
    print("Tare done!")

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)    
    
    lamp = Motor(args.lamp_pins)
    lamp.forward(100)
    lamp.stop()
    
    motorT = Motor(args.motorT_pins)
    motorT.stop()
    motor1 = Motor(args.motor1_pins)
    motor1.stop()
    motor2 = Motor(args.motor2_pins)
    motor2.stop()
    
    # Setting up the model and the labels
    labels = load_labels(args.labels_file)
    interpreter = tf.lite.Interpreter(args.model_file)

    main_flow(args, hx, motorT, motor1, motor2, labels, interpreter, lamp)
