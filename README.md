# Artifactory cleaner

============

Cleaner for generic repos for https://www.jfrog.com/artifactory/

Dependencies: python + pyhocon (`pip install pyhocon`)
Rename `cleaner.example.conf` to `cleaner.conf` and update config data

Config example:

```json
{
    "artifactory": {
        "url": "http://domain/artifactory",
        "auth": ""
    },
    "repos": [
        {
            "name": "libs-snapshot-local",
            "interval": 2592000
        }
    ],
    "exclude": ["maven-metadata.xml"]
}
```