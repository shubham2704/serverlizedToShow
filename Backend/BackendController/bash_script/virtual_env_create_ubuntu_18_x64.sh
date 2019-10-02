#!/bin/bash

PYV=$1
VIR_EN=$2
ACTION=$3

if [ "$ACTION" == "CREATE" ]
    
    then
        CONFIGURE_OPTS=--enable-shared /root/.pyenv/bin/pyenv install $PYV
        /root/.pyenv/bin/pyenv virtualenv $PYV $VIR_EN

elif [ "$ACTION" == "DELETE" ]

    then

        sed -i -e "/$USERNAME/d" /etc/vsftpd.user_list
        rm -R /etc/vsftpd/user_config_dir/$USERNAME
        sudo deluser $USERNAME
        sudo /etc/init.d/vsftpd restart

fi        