# Github2Glass

A small example project that listens for Github commits via the MQTT Publish service hook and sends them to Google Glass.

## What's in the box

* /backend - contains the command line python script that listens for messages published to the broker
* /web - simple authentication frontend based on Google Glass PHP starter project
* /db - where the sqlite database is created
* /modules - stuff we need for installing VM packages with Puppet
* /manifests - Puppet configuration and classes
* /Vagrantfile - base configuration for our Vagrant virtual machine

## Vagrant and Puppet

This example uses Vagrant (http://www.vagrantup.com/) and Puppet (https://puppetlabs.com/) to setup a virtual machine that runs the both the web frontend for authentication and backend service script. This makes this project pretty easy to get up and running!

## Configuration

1. Edit the configuration in /web/config.php:
```
$api_client_id = "YOUR_CLIENT_ID";
$api_client_secret = "YOUR_CLIENT_SECRET";
$api_simple_key = "YOUR_SIMPLE_KEY";
```

2. Edit the configuration in /backend/broker_listener.py:
```
_BROKER_URL = "YOUR_PUBLIC_MQTT_INSTANCE"
_BROKER_PORT = 1883
_TOPIC_BASE = "SOME_TOPIC_BASE"
_CLIENT_API = "YOUR_CLIENT_ID"
_CLIENT_SECRET = "YOUR_CLIENT_SECRET"
```

3. Get the Precise64 Vagrant box:
```
$ vagrant box add precise64 http://files.vagrantup.com/precise64.box
```

4. Fire up the virtual machine:
```
$ vagrant up
```

5. Navigate to the authentication page at http://localhost:4040 and log in.

6. Log into the virtual machine:
```
$ vagrant ssh
```

7. Start the listener:
```
vagrant@precise64:~$ python /vagrant/backend/broker_listener.py
```

8. Enable the MQTT Publish service hook for one of your repos, reusing the existing broker information you already used in step two.

9. Commit something to that repo and see it pop!

## Argh, it's totally not working

So, the MQTT Publish service hook only uses QoS 0, which means it's sending out there and hoping. This is not the most robust situation, but usually works. 

If you're still getting nothing and no error messages, there is a set of Github payload JSON you can uncomment and the manually just ping your broker using a mosquitto_pub or some such tool.

## Not for production, ala, watch the dust and the quota!

I wrote this demo pretty quick. It has bugs. It has gaps in features. And if I rolled it out, I'd burn my quota pretty quick (I see all you Glass Explorers making the codes and commits).

