#!/bin/bash
# To remove only the container that build on the image "chat-app"
docker rm $(docker ps -a -q --filter="ancestor=chat-app")
# To remove all the images "chat-app"
docker rmi $(docker images -q --filter="name=chat-app")
# To build the image "chat-app"
docker build -t chat-app . 
# To run the image
docker run -it -p 5000:5000 chat-app