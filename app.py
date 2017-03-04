from flask import Flask, jsonify, request
from dotenv import load_dotenv, find_dotenv
from twilio import twiml


from Queue import Queue
from threading import Thread
from time import sleep


load_dotenv(find_dotenv())

directions = ['forward', 'backward']

task_q = Queue()
def send_rasp(task_q):
	while True:
		sleep(2)
		if not task_q.empty():
			message = task_q.get()
			print(message)

rasp_signal = Thread(target=send_rasp, args=(task_q, ))
rasp_signal.setDaemon(True)
rasp_signal.start()

app = Flask(__name__)

@app.route('/message', methods=['POST'])
def roomba_command():
	# twilio text message
	body = request.form['Body']

	resp = handle_twilio_message(body)

	twilio_resp = twiml.Response()
	twilio_resp.message(resp)
	return str(twilio_resp)

def handle_twilio_message(message):
	if message.lower() in directions:
		task_q.put(message.lower())
		return 'Message sent'
	try:
		degree = float(message)
	except ValueError as e:
		return 'Invalid command'
	task_q.put(str(degree))
	return 'Message sent'

if __name__ == '__main__':
	app.run(debug=True)