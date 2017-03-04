from flask import Flask, jsonify, request
from dotenv import load_dotenv, find_dotenv
from twilio import twiml

app = Flask(__name__)
load_dotenv(find_dotenv())

directions = ['forward', 'backward']

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
		return message.lower()
	try:
		degree = float(message)
	except ValueError as e:
		return 'Invalid command'
	return str(degree)

if __name__ == '__main__':
	app.run(debug=True)