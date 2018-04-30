import urllib2, base64, json
import os, time

# Address of the WTI device
BASE_PATH = "https://192.168.0.158/api/v2/status/temperature"
# put in the username and password to yuor WTI device here
USERNAME = "super"
PASSWORD = "super"

iCount = 0
while (iCount < 100):
	request = urllib2.Request(BASE_PATH)

	base64string = base64.encodestring('%s:%s' % (USERNAME, PASSWORD)).replace('\n', '') 
	request.add_header("Authorization", "Basic %s" % base64string)  
	result = urllib2.urlopen(request)

	cszTemp = result.read().strip()
#	Uncomment to see the raw JSON return by the unit
#	print cszTemp

	parsed_json = json.loads(cszTemp)

	cszTemperature = parsed_json['temperature']
	cszTemperatureFormat = parsed_json['format']
	cszTimeStamp = parsed_json['timestamp']

	os.system('clear')
	print("Current Temperature is")
	print("----------------------")
	print(cszTemperature+ " " +cszTemperatureFormat + " @ "+cszTimeStamp)
	
	time.sleep(1)
	iCount + iCount + 1

