#!/bin/bash

sudo apt-get -y update
sudo apt-get -y upgrade
sudo apt-get install -y mysql-server

#!/bin/bash

echo "Updating mysql configs in /etc/mysql/my.cnf."
sudo sed -i "s/.*bind-address.*/bind-address = 0.0.0.0/" /etc/mysql/my.cnf
echo "Updated mysql bind address in /etc/mysql/my.cnf to 0.0.0.0 to allow external connections."
sudo service mysql stop
sudo service mysql start