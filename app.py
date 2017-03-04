from flask import Flask, jsonify, request
from dotenv import load_dotenv, find_dotenv
from twilio import twiml
app = Flask(__name__)
load_dotenv(find_dotenv())

@app.route('/message', methods=['POST'])
def roomba_command():
	# twilio text message
	body = request.form['Body']

	resp = handle_twilio_message(body)

	twilio_resp = twiml.Response()
	twilio_resp.message(resp)
	return str(twilio_resp)

def handle_twilio_message(message):
	return 'Echo: ' + message

if __name__ == '__main__':
	app.run(debug=True)