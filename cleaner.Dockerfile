FROM alpine:3.5

RUN apk update && \
    apk add git python2 py2-pip bash && \
    git clone https://github.com/codio/artifactory-cleaner.git && \
    pip2 install pyhocon

RUN (echo '{' \
&& echo '    "artifactory": {' \
&& echo '        "url": "http://artifactory.int.codio.com:8081/artifactory",' \
&& echo '        "auth": "maven:qOwTInzY_4ocuwy0ph_GBhKO0"' \
&& echo '    },' \
&& echo '    "repos": [' \
&& echo '        {' \
&& echo '            "name": "component-builds",' \
&& echo '            "interval": 2160000' \
&& echo '        },' \
&& echo '        {' \
&& echo '            "name": "node-prometheus",' \
&& echo '            "interval": 2160000' \
&& echo '        },' \
&& echo '        {' \
&& echo '            "name": "node-plutus",' \
&& echo '            "interval": 2160000' \
&& echo '        },' \
&& echo '        {' \
&& echo '            "name": "node-socrates",' \
&& echo '            "interval": 2160000' \
&& echo '        },' \
&& echo '        {' \
&& echo '            "name": "grpc-node-zeus",' \
&& echo '            "interval": 2160000' \
&& echo '        },' \
&& echo '        {' \
&& echo '            "name": "grpc-web-zeus",' \
&& echo '            "interval": 2160000' \
&& echo '        }' \
&& echo '    ],' \
&& echo '    "exclude": ["maven-metadata.xml"]' \
&& echo '}' \
) >> artifactory-cleaner/cleaner.conf

RUN (echo '#!/usr/bin/env bash' \
&& echo '' \
&& echo '/usr/bin/python /artifactory-cleaner/cleaner.py' \
) >> artifactory-cleaner/cleaner.sh && chmod +x artifactory-cleaner/cleaner.sh

WORKDIR /artifactory-cleaner/

ENTRYPOINT /artifactory-cleaner/cleaner.sh