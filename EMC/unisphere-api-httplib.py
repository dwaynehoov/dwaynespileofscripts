#!/usr/bin/python

import httplib
import base64
import string
import json
import time
 
host = "hostnameorIP"
port = 0443 #default unisphere API port
url = "/univmax/restapi/performance/Array/metrics" #this can change to match the data you are interested in, refer to EMC schemas
username = 'username'
password = 'password'
symIDs = ['000123456789','000123456789','000123456789'] #enter full 12 digit symmetrix IDs here
for sid in symIDs:
	message = {'arrayParam':
	            {'endDate': int(time.time()*1000), #End time to specify is now.
	             'startDate': int(time.time()*1000)-(3600*1000), # one hour back
	             'metrics': ['IO_RATE','PERCENT_HIT','HIT_PER_SEC','MB_READ_PER_SEC','MB_WRITE_PER_SEC','READ_HIT_PER_SEC','READ_MISS_PER_SEC','REQUEST_PER_SEC','RESPONSE_TIME_READ','RESPONSE_TIME_WRITE'], #array of what metrics we want
	             'symmetrixId': sid #symmetrix ID (full 12 digits)
	            }
	          }
	requestJSON = json.dumps(message, sort_keys=True, indent=4)
	clen = len(requestJSON)
	# base64 encode the username and password
	auth = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
	headers = {	'Host': host,'User-Agent': 'Python http auth','content-type': 'application/json','accept':'application/json','Content-length': clen,'Authorization': "Basic %s" % auth }
	conn = httplib.HTTPSConnection(host, port)
	conn.request("POST",url,body=requestJSON,headers=headers)
	response = conn.getresponse()
	apiOut = response.read()
	print 'symmetrixId=' + sid + ' apiOut='+ apiOut # this was the format I used for easier parsing, printing apiOut will give you JSON
conn.close()