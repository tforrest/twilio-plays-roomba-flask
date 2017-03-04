import requests
import time
from roomba.create2 import Create2

roomba = Create2()
roomba.start()
roomba.safe()

URL = 'https://twilio-plays-roomba.herokuapp.com/next';

def run_command(message):
	try:
		command, degree = message.split()
		command = command.lower()
		degree = float(degree)
		print("Running command: {}".format(message))
		if command == 'forward':
			roomba.straight(degree)
		elif command == 'backward':
			roomba.straight(-1 * degree)
		elif command == 'turn':
			roomba.clockwise(degree)
		elif command == 'turn-':
			roomba.counterclockwise(degree)
		else:
			print("Not a valid command: {}".format(message))
	except Exception as e:
		print e
		print("Error when sending message: {}".format(message))
	finally:
		time.sleep(0.5)
		roomba.drive(0, 0)

def validate(message):
	try:
		command, degree = message.split()
		if command not in ['forward', 'backward', 'turn-', 'turn'] and float(degree) < 0:
			return False
	except Exception as e:
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
