#!/usr/bin/env bash


action=$1
user=$2
password=$3
host_get=$4


set -o errexit
set -o nounset

if [ "$action" == 'create' ]
    then
        if ! echo "SELECT COUNT(*) FROM mysql.user WHERE user = '$user';" | mysql | grep 1 &> /dev/null; then
            
            echo "CREATE USER '$user'@'$host_get' IDENTIFIED BY '$password';
                GRANT ALL PRIVILEGES ON *.* TO '$user'@'$host_get' IDENTIFIED BY '$password';
                FLUSH PRIVILEGES;" | mysql
            echo "created"      
        else
            echo "already"
        fi
fi

if [ "$action" == 'delete' ]
    then
        if ! echo "SELECT COUNT(*) FROM mysql.user WHERE user = '$user';" | mysql | grep 1 &> /dev/null; then
            echo "DROP USER '$user'@'$host_get';" | mysql
            echo "created"      
        else
            echo "DROP USER '$user'@'$host_get';" | mysql
        fi        
fi