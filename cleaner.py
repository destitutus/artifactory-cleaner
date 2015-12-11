__author__ = 'dima'

import httplib
from base64 import b64encode
import time

timestamp = int(time.time())
#2592000
print timestamp*1000

userAndPass = b64encode(b"maven:qOwTInzY_4ocuwy0ph_GBhKO0").decode("ascii")
headers = { 'Authorization' : 'Basic %s' %  userAndPass }

url = "artifactory.int.codio.com"

conn = httplib.HTTPConnection(url, 8081)

conn.request("GET", "/artifactory/api/search/usage?notUsedSince=1449670852990&repos=component-builds", headers=headers)

res = conn.getresponse()

print res.status, res.reason

data = res.read()

print data