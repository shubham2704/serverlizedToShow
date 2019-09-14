#!/usr/bin/env bash


action=$1
user=$2
password=$3
host_get=$4
db=$5


set -o errexit
set -o nounset

if [ "$action" == 'create' ]
    then
        if ! echo "SELECT COUNT(*) FROM mysql.user WHERE user = '$user';" | mysql | grep 1 &> /dev/null; then
             echo "No User"      
        else

            echo "CREATE DATABASE $db;
                  GRANT ALL PRIVILEGES ON $db.* TO '$user'@'$host_get' IDENTIFIED BY '$password';
                  FLUSH PRIVILEGES;" | mysql
            echo "Created"

        fi
fi

if [ "$action" == 'delete' ]
    then
        if ! echo "SELECT COUNT(*) FROM mysql.user WHERE user = '$user';" | mysql | grep 1 &> /dev/null; then
             echo "No User"      
        else

            echo "DROP DATABASE $db;
                  FLUSH PRIVILEGES;" | mysql
            echo "Deleted"

        fi       
fi