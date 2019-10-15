#!/usr/bin/env python3

from flask import Flask, request
import json
import pprint
import requests
import os.path
import time
import logging

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
bridgeip = config['bridgeip']
huekey = config['huekey']
huegroup = config['huegroup']

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

    return "OK"


def light_control(event):
    # build PUT url to hue bridge
    puturl = 'http://' + bridgeip + '/api/' + huekey + '/groups/' + huegroup + '/action'
    # build GET url to hue bridge
    geturl = 'http://' + bridgeip + '/api/' + huekey + '/groups/' + huegroup

    # check for client
    if event['Player']['uuid'] == clientid:
        logging.info("Client detected")

        # TODO get light group settings first, then return lights to how they were once the media is stopped.
        # get current light group settings
        lights_info = requests.get(geturl)
        lights_dict = json.loads(lights_info.text)
        lights_status = lights_dict['state']
        logging.debug(lights_status)

        # turn off lights if media starts playing
        # TODO check hue response for errors.
        if event['event'] == 'media.play' or event['event'] == 'media.resume':
            logging.info("Media playing, turning lights off")
            r = requests.put(puturl, data="{\"on\":false}")

        # dim lights if media is paused
        if event['event'] == 'media.pause':
            logging.info("Media paused, dimming lights")
            r = requests.put(puturl, data="{\"on\": true,\"bri\": 120,\"hue\": 8402,\"sat\": 140,\"effect\": \"none\",\"xy\": [0.4575,0.4099]}")

        # lights on if media is stopped
        if event['event'] == 'media.stop':
            logging.info("Media stopped, turning lights on")
            time.sleep(.5)
            r = requests.put(puturl, data="{\"on\": true,\"bri\": 200,\"hue\": 8402,\"sat\": 140,\"effect\": \"none\",\"xy\": [0.4575,0.4099]}")
    print(r.status_code)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='9090')