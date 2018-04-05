import requests
import json
import hashlib
import base64
import time
import hmac
import json

# Credentials
AccessId = "dSpe6j9eTQXs3Iph7jCU"
AccessKey = "dcm!p2d2w79V=5f}+[354xL=g{k442Y6h5qV}C_6"
account = "ianbloom"

# Request Info
httpVerb ='GET'
resourcePath = '/device/devices'

# size: number of devices returned in query
size = 1000
# offset: number of devices to offset query by (this will be incremented with subsequent queries)
offset = 0
# fields: the comma seperated fields we would like returned from our query (in this case only the device NAME)
fields = 'name'

# Initialize array to hold device names
catchArray = []

# DO: GET a list of 1000 device names, WHILE we have not hit the last page of devices
while True:
	# Construct query parameters
	queryParams = '?size=' + str(size) + '&fields=' + fields + '&offset=' + str(offset)
	# Data payload is EMPTY for GET requests
	data = ''

	# Construct URL 
	url = 'https://'+ account +'.logicmonitor.com/santaba/rest' + resourcePath + queryParams

	# Get current time in milliseconds
	epoch = str(int(time.time() * 1000))

	# Concatenate Request details
	requestVars = httpVerb + epoch + data + resourcePath

	# Construct signature
	authCode = hmac.new(AccessKey.encode(),msg=requestVars.encode(),digestmod=hashlib.sha256).hexdigest()
	signature = base64.b64encode(authCode.encode())

	# Construct headers
	auth = 'LMv1 ' + AccessId + ':' + signature.decode() + ':' + epoch
	headers = {'Content-Type':'application/json','Authorization':auth}

	# Make request
	response = requests.get(url, data=data, headers=headers)

	# Capture response body as data
	data = json.loads(response.content)
	# Refer to list of devices
	devices = data['data']['items']
	for item in devices:
		deviceName = item['name']
		catchArray.append(deviceName)
	offset += size

	# If we have reached final 'page' of data, then the number of returned devices is smaller than 'size'
	# |
	# V
	# Break loop
	if len(devices) < size:
		break

# After all device names have been captured in catchArray, print each
for item in catchArray:
	print(item)