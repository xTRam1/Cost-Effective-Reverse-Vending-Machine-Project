import tkinter as tk
import time
import pdb
import random
import argparse
from motor import Motor
from functions import classify, val_weight, transaction

# GUI Constants
HEIGHT = 500
WIDTH = 900
LARGEFONT =("Verdana", 35)

def build_page(first_time=True, trans=True, dial_components=None, dial_number=''):
	if first_time == False:
		label_dial, upper_frame, lower_frame, dial_frame, label_please = dial_components
		if trans == True:
			if dial_number == '':
				label_please['text'] = 'Please Dial a Number Before Transaction'
				print('Please Dial Number before transaction.')
				return
			transaction(dial_number)
			print('Transaction Complete')
		label_dial['text'] = ''
		upper_frame.pack_forget()
		lower_frame.pack_forget()
		dial_frame.pack_forget()

	global count
	count = 0
	page_frame = tk.Frame(root, bg='#def7f6')
	page_frame.pack(side='top', fill='both')
	
	bottle_count = tk.Label(page_frame, text='Bottle Count: ' + str(count), font=LARGEFONT)
	bottle_count.pack(side='top')

	label_place = tk.Label(page_frame, text='Place your bottles', font=LARGEFONT)
	label_place.pack(side='top')

	recycle_button = tk.Button(page_frame, text='Recycle', font=LARGEFONT, command=lambda: recycle(label_place, bottle_count))
	recycle_button.pack(side='left')
	
	mul_button = tk.Button(page_frame, text='Done', font=LARGEFONT, command=lambda: finish(page_frame, label_place))
	mul_button.pack(side='right')

def move_motors(bottle=''):
	return
	# Süreleri hesaplanır, Motor.stop(time=0) methodunu da kullanabiliriz

	if bottle == 'carton':
		motor_1.forward(speed=args.motor_speeds[0], time=args.motor_times[0])
		motor_2.forward(speed=args.motor_speeds[1],time=args.motor_times[0])
		motor_1.backward(speed=args.motor_speeds[0],time=args.motor_times[0])
		motor_2.backward(speed=args.motor_speeds[1],time=args.motor_times[0])
	elif bottle == 'plastic':
		motor_1.forward(speed=args.motor_speeds[0],time=args.motor_times[0])
		motor_3.forward(speed=args.motor_speeds[2],time=args.motor_times[0])
		motor_1.backward(speed=args.motor_speeds[0],time=args.motor_times[0])
		motor_3.backward(speed=args.motor_speeds[2],time=args.motor_times[0])
	elif bottle == 'metal':
		motor_1.forward(speed=args.motor_speeds[0],time=args.motor_times[0])
		motor_1.backward(speed=args.motor_speeds[0],time=args.motor_times[0])

def recycle(label, bottle_count):
	print('Object Detection Working...')
	bottle = classify()
	weight = val_weight(bottle)
	weight = random.randint(0, 1)

	global count
	if weight:
		move_motors(bottle)
		print('Accepted... Recycling...')
		label['text'] = 'Accepted'
		count += 1
		bottle_count['text'] = 'Bottle Count: ' + str(count)
	else:
		print('Rejected... Error...')
		label['text'] = 'Remove the Container and Repeat'

def finish(page_frame, label):
	print('Type your number.')
	global count
	if count == 0:
		print('You must first insert some bottles')
		label['text'] = 'You must first insert some bottles'
		return

	page_frame.pack_forget()

	# Frames
	upper_frame = tk.Frame(root, bg='#def7f6')
	upper_frame.pack(side='top')

	lower_frame = tk.Frame(root, bg='#def7f6')
	lower_frame.pack(side='top')

	dial_frame = tk.Frame(root, bg='#def7f6')
	dial_frame.pack(side='top')

	label_please = tk.Label(upper_frame, text='Dial Your Number Please', font=LARGEFONT, bg='#def7f6')
	label_please.pack(side='top', fill='both')

	label_dial = tk.Label(lower_frame, text='', font=LARGEFONT, bg='#def7f6')
	label_dial.pack(side='top', fill='both')

	build_dial(dial_frame, label_dial)
	dial_components = (label_dial, upper_frame, lower_frame, dial_frame, label_please)

	button_ok = tk.Button(lower_frame, text='OK', font=LARGEFONT, bg='#def7f6', command=lambda: build_page(
		first_time=False, trans=True, dial_components=dial_components, dial_number=label_dial['text']))
	button_ok.pack(side='top')

	label_quit = tk.Button(lower_frame, text='Donate', font=LARGEFONT, bg='#def7f6', command=lambda: build_page(
		first_time=False, trans=False, dial_components=dial_components, dial_number=label_dial['text']))
	label_quit.pack(side='top')	


def build_dial(dial_frame, label_dial):
	one = tk.Button(dial_frame, text='1', font=LARGEFONT, command=lambda: dial(label_dial, '1'))
	one.grid(row=0, column=0)
	two = tk.Button(dial_frame, text='2', font=LARGEFONT, command=lambda: dial(label_dial, '2'))
	two.grid(row=0, column=1)
	three = tk.Button(dial_frame, text='3', font=LARGEFONT, command=lambda: dial(label_dial, '3'))
	three.grid(row=0, column=2)
	four = tk.Button(dial_frame, text='4', font=LARGEFONT, command=lambda: dial(label_dial, '4'))
	four.grid(row=1, column=0)
	five = tk.Button(dial_frame, text='5', font=LARGEFONT, command=lambda: dial(label_dial, '5'))
	five.grid(row=1, column=1)
	six = tk.Button(dial_frame, text='6', font=LARGEFONT, command=lambda: dial(label_dial, '6'))
	six.grid(row=1, column=2)
	seven = tk.Button(dial_frame, text='7', font=LARGEFONT, command=lambda: dial(label_dial, '7'))
	seven.grid(row=2, column=0)
	eight = tk.Button(dial_frame, text='8', font=LARGEFONT, command=lambda: dial(label_dial, '8'))
	eight.grid(row=2, column=1)
	nine = tk.Button(dial_frame, text='9', font=LARGEFONT, command=lambda: dial(label_dial, '9'))
	nine.grid(row=2, column=2)
	zero = tk.Button(dial_frame, text='0', font=LARGEFONT, command=lambda: dial(label_dial, '0'))
	zero.grid(row=3, column=1)

def dial(label_dial, number):
	label_dial['text'] = label_dial['text'] + number


if __name__ == "__main__":
	
	# Arguments
	parser = argparse.ArgumentParser()
	parser.add_argument(
        '--motor_1_pins', 
        type=tuple,
        default=(2, 3, 4),
        help='pins to which motor 1 is binded to')
	parser.add_argument(
        '--motor_2_pins', 
        type=tuple,
        default=(5, 6, 7),
        help='pins to which motor 2 is binded to')
	parser.add_argument(
        '--motor_3_pins', 
        type=tuple,
        default=(8, 9, 10),
        help='pins to which motor 3 is binded to')
	parser.add_argument(
        '--motor_speeds', 
        type=tuple,
        default=(1,1,1),
        help='speeds with which motors operate')
	parser.add_argument(
        '--motor_times', 
        type=tuple,
        default=(1,1,1),
        help='duration each motor operates with')
	args = parser.parse_args()	
	
	# Motors (Pins can be determined )
	motor_1 = Motor(args.motor_1_pins)
	motor_2 = Motor(args.motor_2_pins)
	motor_3 = Motor(args.motor_3_pins)

	# GUI Preparation
	root = tk.Tk()
	canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH, bg='#def7f6')
	canvas.pack()
	count = 0

	# Background image
	back_image = tk.PhotoImage(file='/Users/erenerdogan/Downloads/bottles.png')
	back_label = tk.Label(root, image=back_image)
	back_label.place(relwidth=1, relheight=1)

	# Builds GUI and mainloop
	build_page(True)
	root.mainloop()
