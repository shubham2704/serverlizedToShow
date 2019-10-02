#!/bin/bash

DOMAIN=$1
DJANGO_VER=$2
ENV_PATH=$3
rootDir=$4
WSGI_FILE=$5
ACTION=$6
INSTALL_DJANGO=$7


email='webmaster@localhost'
sitesEnabled='/etc/apache2/sites-enabled/'
sitesAvailable='/etc/apache2/sites-available/'
userDir='/var/www/'
sitesAvailabledomain=$sitesAvailable$DOMAIN.conf

if [ "$rootDir" == "" ]; then
	rootDir=${domain//./}
fi

### if root dir starts with '/', don't use /var/www as default starting point
if [[ "$rootDir" =~ ^/ ]]; then
	userDir=''
fi

rootDir=$userDir$rootDir


if [ "$ACTION" == "CREATE" ]
    
    then


        . $ENV_PATH/bin/activate
        if [ "$INSTALL_DJANGO" == "INSTALL_DJANGO" ]; then
	    pip install Django==$DJANGO_VER
        fi
        

        if ! echo "
		<VirtualHost *:80>
			ServerAdmin $email
			ServerName $DOMAIN
			ServerAlias $DOMAIN
            WSGIDaemonProcess $DOMAIN python-path=$rootDir:$ENV_PATH
            WSGIProcessGroup $DOMAIN
			WSGIScriptAlias / $rootDir$WSGI_FILE
            WSGIPythonPath $rootDir

            <Directory $rootDir>
            <Files wsgi.py>
                Order deny,allow
                Allow from all
            </Files>
            </Directory>
			ErrorLog /var/log/apache2/$domain-error.log
			LogLevel error
			CustomLog /var/log/apache2/$domain-access.log combined

		</VirtualHost>" > $sitesAvailabledomain

        then
			echo -e $"There is an ERROR creating $domain file"
			exit;
		else
			echo -e $"\nNew Virtual Host Created\n"
		fi

        a2ensite $DOMAIN

        /etc/init.d/apache2 reload

      

fi