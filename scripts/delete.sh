#!/bin/bash
docker stop chat-app-run
docker stop chat-App-run
if [ $# -eq 0 ]; then
    docker rmi -f chat-app
else
    docker rmi -f chat-app:$1
fi
docker rm -f chat-app-run
docker rm -f chat-App-run


