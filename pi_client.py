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
            print(str(res))
        else:
            printf("Invalid command.")
    else:
        print('No commands in the queue.')
    time.sleep(5)

def validate_message(message):
	try:
		command, degree = message.split()
		if command not in ['forward', 'backward', 'turn-', 'turn'] and float(degree) < 0:
			return False
	except Exception as e:
		return False
	return True
