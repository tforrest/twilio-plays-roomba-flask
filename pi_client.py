import requests
import time

URL = 'https://twilio-plays-pokemon.herokuapp.com/next';

while True:
    command = requests.get(URL).text
    print("COMMAND: " + command)
    time.sleep(5)
