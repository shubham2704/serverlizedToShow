#!/bin/bash

sudo apt-get -y update
<<<<<<< HEAD
sudo apt install -y haproxy
=======
sudo apt install -y haproxy
sudo apt-get install -y unzip
rm /etc/haproxy/haproxy.cfg
service apache2 stop
>>>>>>> 39dc7436f277c3059a230b50ccd54ba19acc2d31
