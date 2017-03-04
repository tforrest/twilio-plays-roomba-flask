import requests
import time
from roomba.create2 import Create2

roomba = Create2()
roomba.start()
roomba.safe()

URL = 'https://twilio-plays-roomba.herokuapp.com/next';

while True:
    res = requests.get(URL).json()

    if 'command' in res:
        if validate_message(res['command']):
            command = res['command']
            
            print(command)
            run_command(command)
        else:
            printf("Invalid command.")
    else:
        print('No commands in the queue.')

    time.sleep(5)

def run_command(message):
	try:
		command, degree = message.split()
		command = command.lower()
		if command == 'forward':
			roomba.straight(degree)
		elif command == 'backward':
			roomba.clockwise(180)
			roomba.straight(degree)
		elif command == 'turn':
			roomba.clockwise(degree)
		elif command == 'turn-':
			roomba.counterclockwise(degree)
	except Exception as e:
		print("Error when sending message: {}".format(message))
	finally:
		time.sleep(0.5)
		roomba.drive(0, 0)

def validate_message(message):
	try:
		command, degree = message.split()
		if command not in ['forward', 'backward', 'turn-', 'turn'] and float(degree) < 0:
			return False
	except Exception as e:
		return False
	return True
