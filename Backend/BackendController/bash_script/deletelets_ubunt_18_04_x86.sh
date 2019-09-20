#!/bin/bash

domain=$1
sudo certbot delete --cert-name $domain
sudo a2dissite $domain-le-ssl.conf
rm /etc/apache2/sites-available/$domain-le-ssl.conf
systemctl reload apache2