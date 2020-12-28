from motor import Motor
import time
import argparse
import RPi.GPIO as GPIO

def main(args, motorT, motor1, motor2):
    if args.object_name == 'large_carton' or args.object_name == 'small_carton':
        motor1.forward(int(args.motor1_speed['forward']), args.motor1_time_forward)
        motor1.stop()
        motorT.forward(int(args.motorT_speed['forward']), args.motorT_time)
        motorT.stop()
        motorT.backward(int(args.motorT_speed['backward']), args.motorT_time)
        motorT.stop()
        motor1.backward(int(args.motor1_speed['backward']), args.motor1_time_backward)
        motor1.stop()
    elif args.object_name == 'metal':
        motor2.forward(int(args.motor2_speed['forward']), args.motor2_time_forward)
        motor2.stop()
        motorT.forward(int(args.motorT_speed['forward']), args.motorT_time)
        motorT.stop()
        motorT.backward(int(args.motorT_speed['backward']), args.motorT_time)
        motorT.stop()
        motor2.backward(int(args.motor2_speed['backward']), args.motor2_time_backward)
        motor2.stop()
    elif args.object_name =='large_plastic' or args.object_name == 'small_plastic':
        motorT.forward(int(args.motorT_speed['forward']), args.motorT_time)
        motorT.stop()
        motorT.backward(int(args.motorT_speed['backward']), args.motorT_time)
        motorT.stop()

class ParseKwargs(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, dict())
        for value in values:
            key, value = value.split('=')
            getattr(namespace, self.dest)[key] = value
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--object_name', 
        type=str,
        default='',
        help='type of bottle (large_plastic, small_plastic, large_carton, small_carton, metal)')
    
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
    args = parser.parse_args()
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    motorT = Motor(args.motorT_pins)
    motorT.stop()
    motor1 = Motor(args.motor1_pins)
    motor1.stop()
    motor2 = Motor(args.motor2_pins)
    motor2.stop()
    
    main(args, motorT, motor1, motor2)

