#!/bin/bash

sudo apt-get -y update
sudo apt install -y apache2-utils
sudo apt-get install vsftpd
sudo mv /etc/vsftpd.conf /etc/vsftpd.conf.bak
echo "
listen=YES
# Disable anonymous login
anonymous_enable=NO

# Enable the userlist 
userlist_enable=YES

# Configure the userlist to act as a whitelist (only allow users who are listed there)
userlist_deny=NO

# Allow the local users to login to the FTP (if they're in the userlist)
local_enable=YES

# Allow virtual users to use the same privileges as local users
virtual_use_local_privs=YES

# Setup the virtual users config folder
user_config_dir=/etc/vsftpd/user_config_dir/

chroot_local_user=YES
local_umask=022
write_enable=YES
" >> /etc/vsftpd.conf
sudo mkdir -p /etc/vsftpd/user_config_dir/

sudo /etc/init.d/vsftpd restart