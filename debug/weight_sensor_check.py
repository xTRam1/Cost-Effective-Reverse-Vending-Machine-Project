from hx711 import HX711
import time
import argparse
import sys
import RPi.GPIO as GPIO
    
def main(args):
    hx1 = HX711(args.sensor_pins[0], args.sensor_pins[1])
    hx1.set_reading_format("MSB", "MSB")
    hx1.set_reference_unit(args.reference_unit)

    hx1.reset()
    hx1.tare()
    print('Tare done for first weight sensor')
    while True:
        try:
            val1 = hx1.get_weight(args.num_weight)
            print('Value of the First Sensor: {}'.format(val1))
            # Uncomment to see the difference
            #hx1.power_down()
            #hx1.power_up()
            time.sleep(0.1)
        except (KeyboardInterrupt, SystemExit):
            cleanAndExit()


def cleanAndExit():
    print("Cleaning...")
    GPIO.cleanup()
    print("Bye!")
    sys.exit()

if __name__ == "__main__":
    # Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--sensor_pins', 
        nargs='+',
        type=int,
        help='GPIO pins for the first weight sensor.')
    parser.add_argument(
        '--reference_unit', 
        type=int,
        default=1,
        help='reference unit for first sensor')
    parser.add_argument(
        '--num_weight', 
        type=int,
        default=3,
        help='number of times load cell takes measures and takes the median.')
    
    args = parser.parse_args()
    main(args)
