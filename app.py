from flask import Flask, jsonify, request
#from dotenv import load_dotenv, find_dotenv
from twilio import twiml


from Queue import Queue
from threading import Thread
from time import sleep


app = Flask(__name__)

#load_dotenv(find_dotenv())

directions = ['forward', 'backward']

task_q = Queue()
def send_rasp(task_q):
	while True:
		sleep(2)
		if task_q.empty():
			continue
		message = task_q.get()
		print(message)
		handle_twilio_message(message)

rasp_signal = Thread(target=send_rasp, args=(task_q, ))
rasp_signal.setDaemon(True)
rasp_signal.start()

@app.route('/', methods=['POST'])
def roomba_command():
	twilio_resp = twiml.Response()
	body = request.form['Body']
	message = 'Command valid and queued to roomba'
	if not validate_message:
		message = 'Invalid command'
	else:
		task_q.put(body)
	twilio_resp.message(message)
	return str(twilio_resp)

@app.route('/', methods=['GET'])
def index():
	return 'Hello!'

def validate_message(message):
	try:
		command, degree = message.split()
		if command not in ['forward', 'backward', 'turn-', 'turn'] and float(degree) < 0:
			return False
	except Exception as e:
		return False
	return True

def handle_twilio_message(message):
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


if __name__ == '__main__':
	app.run(debug=True)
