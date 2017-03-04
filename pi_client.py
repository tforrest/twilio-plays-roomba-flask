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
        print(str(res))
    else:
        print('NOTHING IN THE QUEUE.')
    time.sleep(5)
