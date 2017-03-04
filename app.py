from flask import Flask, jsonify, request
#from dotenv import load_dotenv, find_dotenv
from twilio import twiml


from Queue import Queue
from threading import Thread
from time import sleep
import os


app = Flask(__name__)

#load_dotenv(find_dotenv())

directions = ['forward', 'backward']

task_q = []
"""def send_rasp(task_q):
	while True:
		sleep(2)
		if task_q.empty():
			continue
		message = task_q.get()
		print(message)
		handle_twilio_message(message)

rasp_signal = Thread(target=send_rasp, args=(task_q, ))
rasp_signal.setDaemon(True)
rasp_signal.start()"""

@app.route('/', methods=['POST'])
def roomba_command():
	twilio_resp = twiml.Response()
	body = request.form['Body']
	task_q.append(body)

	message = 'Command valid and queued to roomba'
	twilio_resp.message(message)

	return str(twilio_resp)

@app.route('/next', methods=['GET'])
def next():
	if len(task_q) == 0:
		return jsonify({'command': None})
	else:
		task = task_q[0]
		task_q.pop(0)
		return jsonify({'command': task})

@app.route('/queue', methods=['GET'])
def queue():
	return jsonify(task_q)

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


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.debug = True
    app.run(host='0.0.0.0', port=port)
