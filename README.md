# Pyhook python web server for plex webhooks

I'm bad at READMEs more readme coming.....

This will run a web server for plex webhooks, and currently control hue lights when media from a certain client is played/paused/stopped.

### Prerequisites:

```
python
install requirements
```


### How to use:

```
bridgeip: - The internal IP to talk to the bridge
```
Use https://account.meethue.com/bridge to get the internal IP of the bridge, or go to https://discovery.meethue.com/, or find the internal IP of the bridge from your router.

From a computer on the same network as your bridge go to: https://<bridge.ip.address>/debug/clip.html

We will use the API Debugger to get the variables.

```
huekey: - This is the API key that we need to talk to the bridge. "pyhook#plex" can be called whatever you want.
    URL: /api
    Body: {"devicetype":"pyhook#plex"}
    POST
```
The response description will say "Link button not pressed". Press the button on your bridge,
and click the POST button again. The new response will say username: <token>. This is the
value you want to use as the HUE_TOKEN. We will also use this value to get the next few
variables.



```
huegroup: - This is the group ID of the lights you want to interact with.
    URL: /api/<token>/groups
    BODY:
    GET
```
In the list of groups, find the name of the group you want to use, right above that is the
group ID.
```
Group ID ----> "1": {
	              "name": "Theater", <-----Group Name
	              "lights": [
		                 "1"
	              ],
```

```
clientid: - the UUID of the plex client that you want to look for
```
Run the web server by running `python pyhook.py` then tail the log and play something on plex using the client you want to look for.
    You will see something like this:

    
    'Player': { 'local': True,
              'publicAddress': '1.2.3.4',
              'title': 'Name of client',
              'uuid': '123abcd4567-com-plexapp'}, <---- this the ID to use.
     

Rename .pyhook_config_empty.json to .pyhook_config.json
Put in the values n stuff.
