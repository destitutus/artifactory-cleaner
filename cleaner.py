__author__ = 'dima'

import httplib
from base64 import b64encode
import time
from pyhocon import ConfigFactory
from urlparse import urlparse
import json

def not_exclude(value, excludes):
    for val in excludes:
        if val in value:
            return False
    return True

def clean_path(conn, path, header):
    conn.request("DELETE", path, headers=headers)
    res = conn.getresponse()
    data = res.read()
    print data

def outdated(conn, url, headers, repo, interval, exclude):      
    timestamp = int(time.time())
    date = (timestamp - interval)  * 1000

    conn.request("GET", url + "/api/search/usage?notUsedSince=" + str(date) + "&repos=" + repo, headers=headers)

    res = conn.getresponse()

    data = res.read()

    json_object = json.loads(data)
    
    if 'results' in json_object:    
        for value in json_object["results"]:
            if not_exclude(value["uri"], exclude):
                updated = value["uri"].replace("api/storage/", "")
                substr = "/artifactory/"
                pos = updated.index(substr)
                path = updated[pos:len(updated)]
                print path
                clean_path(conn, path, headers)


config = ConfigFactory.parse_file("cleaner.conf")

artifactory_url = urlparse(config.get("artifactory.url"))
port = artifactory_url.port if artifactory_url.port else 80 if artifactory_url.scheme == 'http' else 443

conn = httplib.HTTPConnection(artifactory_url.hostname, port) if artifactory_url.scheme == 'http' else httplib.HTTPSConnection(artifactory_url.hostname, port)

user_pass = b64encode(config.get("artifactory.auth")).decode("ascii")
headers = { 'Authorization' : 'Basic %s' %  user_pass }

for value in config.get("repos"):
    outdated(conn, artifactory_url.path, headers, value.get('name'), value.get_int('interval'), config.get("exclude"))