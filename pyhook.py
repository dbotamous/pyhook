#!/usr/bin/env python3

from flask import Flask, request
import json
import pprint
import requests
import os.path
import time
import logging
# import ephem

# Create a place for logs to go. Will need to make sure that the user running this has access to the logfile.
logging.basicConfig(filename='/var/log/pyhook.log',
                    level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')

# set the path to config file
config_file = '.pyhook_config.json'
if not os.path.isfile(config_file):
    raise Exception(
        "No config file found in Environment Variables or at {}".format(config_file))
config = json.load(open(config_file))
clientid = config['clientid']
iftttkey = config['iftttkey']

app = Flask(__name__)
pp = pprint.PrettyPrinter(indent=2)

# create for route for POST requests.
@app.route('/', methods=['POST'])
def dewstuff():
    data = json.loads(request.form['payload'])
    pp.pprint(data)
    # send to hue for light control
    light_control(data)
    # add future stuff below
    # logging.info(data)

    return "OK"


def light_control(event):
    playurl = 'https://maker.ifttt.com/trigger/play/with/key/' + iftttkey
    pauseurl = 'https://maker.ifttt.com/trigger/pause/with/key/' + iftttkey
    stopurl = 'https://maker.ifttt.com/trigger/stop/with/key/' + iftttkey

    testurl = 'https://maker.ifttt.com/trigger/stop/with/key/' + iftttkey
    print(testurl)

    # check for client
    if event['Player']['uuid'] == clientid:
        logging.info("Correct client detected, dewing stuff.")

        # lights off if media is playing
        if event['event'] == 'media.play' or event['event'] == 'media.resume':
            logging.info("Media playing, turning lights off")
            r = requests.put(playurl)

        # dim lights if media is paused
        if event['event'] == 'media.pause':
            logging.info("Media paused, dimming lights")
            r = requests.put(pauseurl)

        # lights on if media is stopped
        if event['event'] == 'media.stop':
            logging.info("Media stopped, turning lights on")
            r = requests.put(stopurl)

    logging.info("Wrong player detected, dewing nothing.")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='9090')