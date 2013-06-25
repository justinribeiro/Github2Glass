#!/usr/bin/python

import sys
import httplib2
import mosquitto
import sqlite3
import json
import random
import string
import time
import logging

from oauth2client.client import OAuth2Credentials
from apiclient.discovery import build
from string import Template

creds = None

# broker information for mqtt
_BROKER_URL = "YOUR_PUBLIC_MQTT_INSTANCE"
_BROKER_PORT = 1883
_TOPIC_BASE = "SOME_TOPIC_BASE"

_CLIENT_API = "YOUR_CLIENT_ID"
_CLIENT_SECRET = "YOUR_CLIENT_SECRET"
_TOKEN_URI = "https://accounts.google.com/o/oauth2/auth"

# sqlite3 database info for creds
_DB_PATH = "/vagrant/db/github2glass.sqlite"

def on_connect(mosq, obj, rc):
	print("Connected to broker")

def on_message(mosq, obj, msg):
	print("Incoming message from broker!")
	sendTimelineCard(msg.topic, msg.payload)

def on_publish(mosq, obj, mid):
    print("mid: "+str(mid))

def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))

def on_log(mosq, obj, level, string):
    print(string)

def sendTimelineCard(topic, payload):

	print("Sending timeline card!")
	
	# not getting MQTT messages because QoS 0 is not awesome sometimes? uncomment to send some test data
	#payload = '{"after": "9849af5dc2126e2ff1c6213b092ad8b3a7385d56", "before": "ca86dcb1d94e56a1b14acf9ab1bf0a93452d9b98", "commits": [ { "added": [], "author": { "email": "justin@justinribeiro.com", "name": "Justin Ribeiro", "username": "justinribeiro" }, "committer": { "email": "justin@justinribeiro.com", "name": "Justin Ribeiro", "username": "justinribeiro" }, "distinct": true, "id": "9849af5dc2126e2ff1c6213b092ad8b3a7385d56", "message": "Remove comment, test hook", "modified": [ "src/com/example/android/apps/fan/ui/HomeActivity.java" ], "removed": [], "timestamp": "2013-06-25T09:05:34-07:00", "url": "https://github.com/justinribeiro/pubsub-android-gcp/commit/9849af5dc2126e2ff1c6213b092ad8b3a7385d56" } ], "compare": "https://github.com/justinribeiro/pubsub-android-gcp/compare/ca86dcb1d94e...9849af5dc212", "created": false, "deleted": false, "forced": false, "head_commit": { "added": [], "author": { "email": "justin@justinribeiro.com", "name": "Justin Ribeiro", "username": "justinribeiro" }, "committer": { "email": "justin@justinribeiro.com", "name": "Justin Ribeiro", "username": "justinribeiro" }, "distinct": true, "id": "9849af5dc2126e2ff1c6213b092ad8b3a7385d56", "message": "Remove comment, test hook", "modified": [ "src/com/example/android/apps/fan/ui/HomeActivity.java" ], "removed": [], "timestamp": "2013-06-25T09:05:34-07:00", "url": "https://github.com/justinribeiro/pubsub-android-gcp/commit/9849af5dc2126e2ff1c6213b092ad8b3a7385d56" }, "pusher": { "email": "justin@justinribeiro.com", "name": "justinribeiro" }, "ref": "refs/heads/master", "repository": { "created_at": 1371487406, "description": "Example Android application backed with Google Cloud Platform and Paho.", "fork": false, "forks": 0, "has_downloads": true, "has_issues": true, "has_wiki": true, "id": 10742035, "language": "Java", "master_branch": "master", "name": "pubsub-android-gcp", "open_issues": 0, "organization": "justinribeiro", "owner": { "email": "team@justinribeiro.com", "name": "justinribeiro" }, "private": true, "pushed_at": 1372176334, "size": 3976, "stargazers": 0, "url": "https://github.com/justinribeiro/pubsub-android-gcp", "watchers": 0 } }'
	
	cardTemplate = Template('<article><section><div class=\"text-large\"><p class=\"yellow\">$repobranch <sub>$commit</sub></p><p>$message</p></div></section><footer><div>$committer</div></footer></article>')
	
	db = sqlite3.connect(_DB_PATH)
	cursor = db.cursor()
	cursor.execute('SELECT userid, credentials FROM credentials')
	
	# multi-user? Maybe later when the API qouta is higher. Wink. Bwwahahhaha ;-)
	result = cursor.fetchone()
	
	if result != None:
		getUserKeys = json.loads(result[1])
		credentials = OAuth2Credentials(getUserKeys['access_token'], _CLIENT_API, _CLIENT_SECRET, getUserKeys['refresh_token'], None, _TOKEN_URI, None)
		test = credentials.access_token_expired
		mirror_service = create_service('mirror', 'v1', credentials)
		
		# get some data
		payloadToJson = json.loads(payload)
		
		#break the data out so we can see it, make it short + pretty for resolution
		repoBranch =  payloadToJson['repository']['name'] + '/' + payloadToJson['ref'].rsplit('/',1)[1]
		commitShort = payloadToJson['commits'][0]['id'][:8]
		commitMessage = payloadToJson['commits'][0]['message']
		committerName = payloadToJson['commits'][0]['committer']['name']
		
		# build the card
		htmlCard = cardTemplate.substitute(repobranch=repoBranch, commit=commitShort, message=commitMessage, committer=committerName)

		#we add a delete menu item, just in case you want to remove it from your timeline
		body = {
			'creator': {
				'displayName': 'Github 2 Glass',
				'id': 'GITHUB_2_GLASS_JDR'
			},
			'html': htmlCard,
			'notification': {'level': 'DEFAULT'},
			'menuItems': [{'action': 'DELETE'}]
		}
		
		# why aren't you having more fun...you're freakin' sending data to a device on your face!
		mirror_service.timeline().insert(body=body).execute()

def create_service(service, version, creds=None):
	"""Create a Google API service.

	Load an API service from a discovery document and authorize it with the
	provided credentials.

	Args:
	service: Service name (e.g 'mirror', 'oauth2').
	version: Service version (e.g 'v1').
	
	creds: Credentials used to authorize service.
	Returns:
	Authorized Google API service.
	"""
	# Instantiate an Http instance
	http = httplib2.Http()
	
	if creds:
		# Authorize the Http instance with the passed credentials
		creds.authorize(http)

	return build(service, version, http=http)	
    
print "Github 2 Glass listener"

broker = mosquitto.Mosquitto()

broker.on_message = on_message
broker.on_connect = on_connect
broker.on_publish = on_publish
broker.on_subscribe = on_subscribe
broker.connect(_BROKER_URL, _BROKER_PORT, 60)
broker.subscribe(_TOPIC_BASE + "/#", 2)

rc = 0
while rc == 0:
	rc = broker.loop()