#!/bin/bash

PWD=$1
USERNAME=$2
DIR_NAME=$3

if [ ! -d "/var/www/$DIR_NAME" ] 
then
    sudo htpasswd -db /etc/vsftpd/ftpd.passwd $USERNAME $PWD
    mkdir -p /var/www/$DIR_NAME

else
    echo "Directory /path/to/dir DOES NOT exists." 
    exit 9999 # die with error code 9999

fi