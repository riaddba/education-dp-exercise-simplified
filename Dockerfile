# Dockerizing Python 3.9.7 and MongoDB 5.0
# Based on ubuntu:latest, installs MongoDB following the instructions from:
# https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/
# INSTRUCTIONS:
# - Create the contianer:
#   > docker build -t ubuntu_pymongo .
# - Create a folder to share your project in your host with the container. Ex: ~/shared
# - Run the next command (need the route of the created shared folder), this command access to the bash of container:
#   > docker run -v /c/Users/Jhonny/Documents/vm_share/mongoDB/shared:/data/code -t -i -p 27019:27017 ubuntu_pymongo
# - To open another bash console run the command: 
#   > docker exec -it <id_contenedor> bash
# - Run the mongo database:
#   > mongod
# - To connect compass or another gui with mongo use the IP of docker: 192.168.99.100 and the port 27017, or another that you indicate in the command
# https://stackoverflow.com/questions/33558506/how-to-create-a-mongo-docker-image-with-default-collections-and-data
# https://stackoverflow.com/questions/43575295/how-to-import-data-to-mongodb-container-and-creating-an-image

FROM       ubuntu:16.04
MAINTAINER Docker

# Installation:
RUN apt-get update && apt-get install -y build-essential python3.9 
RUN apt-get install -y python-setuptools
RUN apt-get install -y python-pip
RUN apt-get install -y nano
RUN apt-get install -y telnet
RUN apt-get install -y vim

# Import MongoDB public GPG key AND create a MongoDB list file
RUN apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv 7F0CEB10
RUN echo 'deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen' | tee /etc/apt/sources.list.d/10gen.list

# Update apt-get sources AND install MongoDB
RUN apt-get update && apt-get install -y mongodb-org

# Create the MongoDB data directory
RUN mkdir -p /data/db

# Create the MongoDB data directory
RUN mkdir -p /data/code

RUN pip install bson
RUN pip install duckduckpy
RUN pip install pymongo
RUN pip install glob
RUN pip install pandas
RUN pip install json

# Expose port #27017 from the container to the host
EXPOSE 27017

# Set /usr/bin/mongod as the dockerized entry-point application
ENTRYPOINT ["/bin/bash"]
