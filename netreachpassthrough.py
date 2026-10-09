#!/usr/bin/env python
import json
import requests
from urllib.parse import quote

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# NetReach API Documentation
# HTML: https://upgrade.wti.com/pub/TechSupport/Restful_WTI/NetReach/current/api/Netreach_api_html.html
# PostMan Friendly: https://upgrade.wti.com/pub/TechSupport/Restful_WTI/NetReach/current/api/NetReach_postman_friendly.postman_collection.json
# OpenAPI (Swagger): https://upgrade.wti.com/pub/TechSupport/Restful_WTI/NetReach/current/api/Netreach_openapi.yaml

# This API Key is generated in the NetReach Application Under Users
NETREACH_API_KEY="<NETREACH_API_KEY>"

# NetReach user that sets up API Passthrough, needs Administrator rights in NetReach
USERNAME  = "<NETREACH_USERNAME>"
PASSWORD  = "<NETREACH_PASSWORD>"

BASE_URL = "https://<NETREACH_HOSTNAME>"

def netreach_login(session):
	r = session.post(BASE_URL+"/login", data={"username": USERNAME, "password": PASSWORD}, allow_redirects=False)

	if (r.status_code != 302 or r.headers.get("Location", "").endswith("/login")):
		raise RuntimeError(f"NetReach login failed for user {USERNAME}")


def query_passthrough(api_key):
	# The "*" signifies get the temperature all groups
	url = BASE_URL+"/api/*/temperature"
	r = requests.get(url, verify=False, headers={"nr-wti-api-key": api_key}, timeout=120)

	if (r.status_code != 200):
		print(f"{r.status_code}: {r.text}\r\n")
		return

	for line in r.text.splitlines():
		if (not line.startswith("data:")):
			continue

		unit = json.loads(line[len("data:"):])
		data = unit["data"]

#		print (data)

		print(f"{unit['unit_siteid']} ({unit['unit_ipaddress']})")
		if ("temperature" in data):
			print(f"  {data['temperature']} {data['format']} @ {data['timestamp']}")
		elif ("message" in data):
			detail = data.get("data", {}).get("status", {}).get("text", "")
			print(f"  {data['message']} {detail}")
		else:
			print(f"  {json.dumps(data)}")

	print(url)


session = requests.Session()
session.verify = False

try:
	netreach_login(session)
	print("\r\nCurrent Temperature is")
	print("----------------------")
	query_passthrough(NETREACH_API_KEY)
	print()

except (requests.exceptions.RequestException, RuntimeError, ValueError, KeyError) as e:
	print ("Exception:")
	print (e)
