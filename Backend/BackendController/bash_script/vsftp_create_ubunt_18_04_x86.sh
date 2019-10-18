#!/bin/bash

PWD=$1
USERNAME=$2
DIR_NAME=$3
ACTION=$4


if [ "$ACTION" == "CREATE" ]
    
    then

    if [ ! -d "/var/www/$DIR_NAME" ] 
        then

            echo "Create FTP user action"
            mkdir -p /var/www/$DIR_NAME
            
            touch /etc/vsftpd/user_config_dir/$USERNAME
            useradd -m $USERNAME
            echo "$USERNAME:$PWD" | sudo chpasswd
            chown -R $USERNAME: /var/www/$DIR_NAME
            echo  "$USERNAME" >> /etc/vsftpd.user_list
            echo "
            local_root=/var/www/$DIR_NAME
            allow_writeable_chroot=YES
            write_enable=YES
            " >> /etc/vsftpd/user_config_dir/$USERNAME

            
            sudo /etc/init.d/vsftpd restart


    else
            echo "Create FTP user action"
            touch /etc/vsftpd/user_config_dir/$USERNAME
            useradd -m $USERNAME
            echo "$USERNAME:$PWD" | sudo chpasswd
            echo  "$USERNAME" >> /etc/vsftpd.user_list
            chown -R $USERNAME: /var/www/$DIR_NAME
            echo "
            local_root=/var/www/$DIR_NAME
            allow_writeable_chroot=YES
            write_enable=YES
            " >> /etc/vsftpd/user_config_dir/$USERNAME

            
            sudo /etc/init.d/vsftpd restart

    fi
elif [ "$ACTION" == "DELETE" ]

    then

    sed -i -e "/$USERNAME/d" /etc/vsftpd.user_list
    rm -R /etc/vsftpd/user_config_dir/$USERNAME
    sudo deluser $USERNAME
    sudo /etc/init.d/vsftpd restart

fi