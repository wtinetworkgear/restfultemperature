#!/usr/bin/env python

import json
import os
import requests

# supress Unverified HTTPS request, only do this in a verified environment
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Address of the WTI device
URI = "https://"
SITE_NAME = "rest.wti.com"
BASE_PATH = "/api/v2/status/temperature"

# put in the username and password to yuor WTI device here
USERNAME = "rest"
PASSWORD = "restfulpassword"

try:
	r = requests.get(URI+SITE_NAME+BASE_PATH, auth=(USERNAME, PASSWORD), verify=False)
	if (r.status_code == 200):
		os.system('clear')
		parsed_json = r.json()

#		Uncomment to see the JSON return by the unit
#		print parsed_json

		cszTemperature = parsed_json['temperature']
		cszTemperatureFormat = parsed_json['format']
		cszTimeStamp = parsed_json['timestamp']

		print("Current Temperature is")
		print("----------------------")
		print(cszTemperature+ " " +cszTemperatureFormat + " @ "+cszTimeStamp+"\r\n")
		print(URI+SITE_NAME+BASE_PATH)
	else:
		print(r.status_code)

except requests.exceptions.RequestException as e:  # This is the correct syntax
	print (e)
