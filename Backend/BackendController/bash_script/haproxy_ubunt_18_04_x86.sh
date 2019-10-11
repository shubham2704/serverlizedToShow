#!/bin/bash

sudo apt-get -y update
sudo apt install -y haproxy
sudo apt-get install -y unzip
rm /etc/haproxy/haproxy.cfg
service apache2 stop