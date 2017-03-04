from flask import Flask, jsonify
from dotenv import load_dotenv, find_dotenv
app = Flask(__name__)
load_dotenv(find_dotenv())

@app.route('/')
def hello_world():
    return jsonify({
		'hello': 'world'
	})

if __name__ == '__main__':
	app.run(debug=True)