#!/bin/bash

apt-get install -y software-properties-common
add-apt-repository -y ppa:ondrej/php
sudo apt-get -y update
apt-get install -y php7.3
apt-get install -y php-pear php7.3-curl php7.3-dev
apt-get install -y php7.3-gd php7.3-mbstring
apt-get install -y php7.3-zip php7.3-mysql;apt-get install -y php7.3-xml