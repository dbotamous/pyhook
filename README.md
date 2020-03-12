# Pyhook python web server for plex webhooks

I'm bad at READMEs more readme coming.....

This will run a web server for plex webhooks. It will look for media.play, media.resume, media.pause, and media.stop events. It will then send that to IFTTT, and you can tie it into whatever home automation you chose. I use this with Abode to control my theater lighting, works great. 

### Prerequisites:

```
python
install requirements
```


### How to use:

I'll add to this later.

Setup a webhook in plex, pointed to where you are installing pyhook. Google how to setup a webhook in plex. 


You need to have an IFTTT account, and create and a webhook service. Once that is created, you can go to the webhook service and click on documentation, that will give you a url like this:
"https://maker.ifttt.com/trigger/{event}/with/key/supersecretkey"

You will add the "supersecretkey" to the .pyhook_config.json file

You then create three Applets.

``` 
If Webhook play, then automation of your choosing. 
```

For me using Abode, I have webhooks, and Abode as services, so mine look like this:

```
If Webhook play, then Abode dim the theater lights to 0
If Webhook pause, then Abode dim the theater lights to 20
If Webhook stop, then Abode dim the theater lights to 50
```

Once those are created, you can start the service (python pyhook.py) and tail the log file (/var/log/pyhook.log).
Play something on the plex client that you want to use, you will see something like this

```
'Player': { 'local': True,
          'publicAddress': '1.2.3.4',
          'title': 'Name of client',
          'uuid': '123abcd4567-com-plexapp'}, <---- this the ID to use.

```

Put that plex client ID in the .pyhook_config.json file, and restart the service. 

That should be it. 