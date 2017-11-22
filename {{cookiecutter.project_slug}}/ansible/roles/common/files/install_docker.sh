#!/usr/bin/env bash

# this script is used to install docker 

sudo sh -c "echo deb https://apt.dockerproject.org/repo ubuntu xenial main > /etc/apt/sources.list.d/docker.list"
# : Adding the Docker repository GPG key
sudo apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D

sudo apt-get update

sudo apt-get install docker.io

# check status
# sudo docker info 