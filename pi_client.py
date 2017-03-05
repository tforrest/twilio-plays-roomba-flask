import requests
import time
from roomba.create2 import Create2

roomba = Create2()
roomba.start()
roomba.safe()

URL = 'https://twilio-plays-roomba.herokuapp.com/next';

def run_command(message):
	command = message.lower()
	print("Running command: {}".format(message))
	if command == 'forward':
		roomba.straight(50)
	elif command == 'backward':
		roomba.straight(-1 * 50)
	elif command == 'turn clockwise':
		roomba.clockwise(50)
	elif command == 'turn counterclockwise':
		roomba.counterclockwise(50)
	else:
		print("Not a valid command: {}".format(message))
	time.sleep(0.5)
	roomba.drive(0, 0)

def validate(message):
	command = command.lower()
	if command not in ['forward', 'backward', 'turn counterclockwise', 'turn clockwise']:
		return False
	return True

def start_client():
	while True:
		try:
			res = requests.get(URL).json()
		except Exception as e:
			print e
			print 'Invalid request to Twilio'
			continue
		if 'command' in res:
			command = res['command']
			if validate(command):
				print(command)
				run_command(command)
			else:
				print("Invalid command.")
		else:
			print('No commands in the queue.')
		time.sleep(1)

if __name__ == '__main__':
	start_client()
