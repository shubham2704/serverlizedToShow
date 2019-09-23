#!/bin/bash

sudo apt-get -y update
sudo apt install -y apache2-utils
sudo apt-get install vsftpd libpam-pwdfile
sudo mv /etc/vsftpd.conf /etc/vsftpd.conf.bak
echo "
listen=YES
anonymous_enable=NO
local_enable=YES
write_enable=YES
local_umask=022
nopriv_user=vsftpd
virtual_use_local_privs=YES
guest_enable=YES
user_sub_token=\$USER
local_root=/var/www/\$USER
chroot_local_user=YES
allow_writeable_chroot=YES
hide_ids=YES
guest_username=vsftpd

" >> /etc/vsftpd.conf
sudo mkdir /etc/vsftpd
sudo mv /etc/pam.d/vsftpd /etc/pam.d/vsftpd.bak
echo "
auth required pam_pwdfile.so pwdfile /etc/vsftpd/ftpd.passwd
account required pam_permit.so
" >> /etc/pam.d/vsftpd
sudo useradd --home /home/vsftpd --gid nogroup -m --shell /bin/false vsftpd
echo "" >> /etc/vsftpd/ftpd.passwd
sudo /etc/init.d/vsftpd restart