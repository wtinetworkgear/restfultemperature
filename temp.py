#!/usr/bin/env python
import json
import requests

# supress Unverified HTTPS request, only do this in a verified environment
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Address of the WTI device
URI             = "https://"
SITE_NAME       = "rest.wti.com"

# put in the username and password to your WTI device here
BASE_PATH = "/api/v2/status/temperature"
USERNAME  = "rest"
PASSWORD  = "restfulpassword"
AUTH = (USERNAME, PASSWORD)
HEADER = ""

# or if using user tokens put in the User's Token to your WTI device here
#BASE_PATH = "/api/v2/token/status/temperature"
#HEADER = {"X-WTI-API-KEY":"!m+-w-~qo0aq78n=wgyz2c54c365rknj3rnguew8!4mztzx-6j2wlwoonbh4s1cj"}
#AUTH = ""

try:
	r = requests.get(URI+SITE_NAME+BASE_PATH, verify=False, auth=AUTH, headers=HEADER)

	if (r.status_code == 200):
		parsed_json = r.json()

#		Uncomment to see the JSON return by the unit
#		print (parsed_json)

		cszTemperature = parsed_json['temperature']
		cszTemperatureFormat = parsed_json['format']
		cszTimeStamp = parsed_json['timestamp']

		print("Current Temperature is")
		print("----------------------")
		print(cszTemperature+ " " +cszTemperatureFormat + " @ "+cszTimeStamp+"\r\n")
		print(URI+SITE_NAME+BASE_PATH)
	else:
		print(r.status_code)

except requests.exceptions.RequestException as e:
	print ("Exception:")
	print (e)
