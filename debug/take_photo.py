import picamera
import time
import argparse
import os
from Motor import Motor
import RPi.GPIO as GPIO

def main(args, lamp):
    lamp.forward(100)
    time_str = time.strftime('%Y-%m-%d-%H-%M')
    image_file = os.path.join(args.data_path, args.type, '{}.jpg'.format(time_str))

    # Opening camera and capturing the image
    with picamera.PiCamera() as camera:
        # Capture and resize the image
        time.sleep(.2)
        camera.resolution = (1280, 720)
        camera.capture(image_file)
        lamp.stop()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--type', 
        type=str,
        default='',
        help='type of bottle (large_plastic, small_plastic, large_carton, small_carton, metal)')
    parser.add_argument(
        '--data_path',
        type=str,
        default='',
        help='path of dataset')
    parser.add_argument(
        '--lamp_pins', 
        nargs='+',
        type=int,
        help='pins of the lamp')
    args = parser.parse_args()
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    
    lamp = Motor(args.lamp_pins)
    lamp.forward(100)
    lamp.stop()

    main(args, lamp)