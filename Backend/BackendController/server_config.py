SERVER_OS_DISTRIBUTION = {
    1: ['Ubuntu', '18.04 x64', 'sudo', 'bash']
}

STACK_DIST = {
    1:{
        'NAME' : 'LAMP',
        'DESCRIPTION' : 'A LAMP Stack is a set of software that can be used to create and host websites and web applications.',
        'PRICE' : 0.00 ,
        'PACKAGES':(1, 2, 3, 4),
        'PACKAGES_COUNT': 3
    },2:{
        'NAME' : 'Load Balancer',
        'DESCRIPTION' : 'A Load Balancer stack is a set of software that can be used for TCP and HTTP-based applications that spreads requests across multiple servers.',
        'PRICE' : 0.00 ,
        'PACKAGES':(5),
        'PACKAGES_COUNT': 1
    }
    
}


PACKAGES = {
    1:{
        'NAME' : 'APACHE WEB SERVER',
        'SERVICE_VIEW' : True,
        'NAV_NAME' : 'DOMAIN',
        'APP_NAME' : 'lamp',
        'DEPENDENCIES' : [],
        'DESCRIPTION':'The Apache HTTP Server, colloquially called Apache, is free and open-source cross-platform web server software, released under the terms of Apache License 2.0. Apache is developed and maintained by an open community of developers under the auspices of the Apache Software Foundation.',
        'VERSION':'2.2',
        'INIT_COMMAND' : {
            1:[('sudo apt-get -y update', 'sudo apt-get -y upgrade')],
        },
        'INSTALLATION_BASH_SCRIPT' : {
            1:[('SCRIPT', 'apache_ubunt_18_04_x86.sh')]
        },
        'CONTROL_PANEL' : {
            'Website':{
                        "ICON" : {
                             "URL":('fa fa-globe', "", False)
                         },
                        "Addon Domain" : {
                             "URL":('wpanel/<int:manage_id>/domain/add', "Backend.lamp.views.add", True),
                              "COMMAND":{
                                 1:('SCRIPT', 'apache_virtual_host_ubuntu_18_04x86.sh')
                                 }
                         },
                         "Edit Domain" : {
                             "URL":('wpanel/<int:manage_id>/domain/edit/<int:domain_id>', "Backend.lamp.views.edit", False)
                         },
                         "Delete Domain" : {
                             "URL":('wpanel/<int:manage_id>/domain/delete/<int:domain_id>', "Backend.lamp.views.delete", False)
                         },
                         
                         "Restart" : {
                             "URL":('wpanel/<int:manage_id>/package/<int:package_id>/restart', "Backend.servers.views.restart_pkg", False),
                             "COMMAND":{
                                 1:('COMMAND', 'service apache2 restart')
                                 }
                         },
                         
                         "Stop" : {
                             "URL":('wpanel/<int:manage_id>/package/<int:package_id>/stop', "Backend.servers.views.stop_pkg", False),
                             "COMMAND":{
                                 1:('COMMAND', 'service apache2 stop')
                                 }
                         },
                         "Apache Logs" : {
                             "URL":('wpanel/<int:manage_id>/apache/log', "Backend.lamp.views.apachelog", True),
                             "COMMAND":{
                                 1:('COMMAND', 'sudo tail -50 /var/log/apache2/error.log')
                                 }
                         }
              },
              'SSL/TLS':{
                        "ICON" : {
                             "URL":('fa fa-certificate', "", False)
                         },
                         "Configure SSL" : {
                             "URL":('wpanel/<int:manage_id>/ssl', "Backend.lamp.views.ssl", True)
                         },
              },
              
              
               
                }

                
        },
        
        2:{
        'NAME' : 'MySQL',
        'NAV_NAME' : 'Database',
        'SERVICE_VIEW' : True,
        'APP_NAME' : 'lamp',
        'DEPENDENCIES' : [],
        'DESCRIPTION':'',
        'VERSION':'2.2',
        'INIT_COMMAND' : {
            1:[('sudo apt-get update', 'sudo apt-get upgrade')],
        },
        'INSTALLATION_BASH_SCRIPT' : {
           1:[('SCRIPT', 'mysql_ubunt_18_04_x86.sh')]
        },
        'CONTROL_PANEL' : {
            'MySQL':{   
                        "ICON" : {
                             "URL":('fa fa-database', "Backend.lamp.views.add", False)
                         },
                        "Create User" : {
                             "URL":('wpanel/<int:manage_id>/mysql/create/user', "Backend.lamp.views.mysql_user_add", True),
                              "COMMAND":{
                                 1:('SCRIPT', 'mysql_user_18_04_x86.sh')
                                 }
                         },

                         "Delete User" : {
                             "URL":('wpanel/<int:manage_id>/mysql/user/delete/<int:muser_id>', "Backend.lamp.views.mysql_user_delete", False),
                              "COMMAND":{
                                 1:('SCRIPT', 'mysql_user_18_04_x86.sh')
                                 }
                         },"Create Database" : {
                             "URL":('wpanel/<int:manage_id>/mysql/create/database', "Backend.lamp.views.mysql_database_add", True),
                              "COMMAND":{
                                 1:('SCRIPT', 'mysql_db_create_18_04_x86.sh')
                                 }
                         },
                         "Delete Database" : {
                             "URL":('wpanel/<int:manage_id>/mysql/database/delete/<int:muser_id>', "Backend.lamp.views.mysql_db_delete", False),
                              "COMMAND":{
                                 1:('SCRIPT', 'mysql_db_create_18_04_x86.sh')
                                 }
                         }
                         
              }
               
                }
        },
        3:{
        'NAME' : 'PHP 7.3',
        'NAV_NAME' : 'PHP',
        'SERVICE_VIEW' : False,
        'APP_NAME' : 'lamp',
        'DESCRIPTION':'',
        'DEPENDENCIES' : [1],
        'VERSION':'7.5',
        'INIT_COMMAND' : {
            1:[('sudo apt-get update', 'sudo apt-get upgrade')],
        },
        'INSTALLATION_BASH_SCRIPT' : {
            1:[('SCRIPT', 'php_ubunt_18_04_x86.sh')]
        },
        'CONTROL_PANEL' : {}
        },

        
        4:{
        'NAME':'PhpMyAdmin',
        'NAV_NAME' : 'PHP',
        'SERVICE_VIEW' : False,
        'APP_NAME' : 'lamp',
        'DESCRIPTION':'',
        'DEPENDENCIES' : [1,2,3],
        'VERSION':'7.5',
        'INIT_COMMAND' : {
            1:[('sudo apt-get update', 'sudo apt-get upgrade')],
        },
        'INSTALLATION_BASH_SCRIPT' : {
            1:[('SCRIPT', 'phpmyadmin_ubunt_18_04_x86.sh'), ('FUNCTION', 'welcomepage')]
        },
        'CONTROL_PANEL' : {
            'phpMyAdmin':{
                        "ICON" : {
                             "URL":('fa fa-external-link', "Backend.lamp.views.add", False)
                         },
                        "Open phpMyAdmin" : {
                             "URL":('wpanel/<int:manage_id>/phpmyadmin', "Backend.lamp.views.phpmyadmin", True)
                         },
              }
        
        }
        },
        6:{
        'NAME':'Lets Encrypt SSL',
        'SERVICE_VIEW' : True,
        'NAV_NAME' : 'PHP',
        'APP_NAME' : 'lamp',
        'DESCRIPTION':'',
        'DEPENDENCIES' : [1],
        'VERSION':'7.5',
        'INIT_COMMAND' : {
            1:[('sudo apt-get update', 'sudo apt-get upgrade')],
        },
        'INSTALLATION_BASH_SCRIPT' : {
            1:[('SCRIPT', 'lets_encrypt_18_04_x86.sh')]
        },
        'CONTROL_PANEL' : {
            'Lets Encrypt':{
                        "ICON" : {
                             "URL":('fa fa-certificate', "Backend.lamp.views.add", False)
                         },
                        "Create Certificate" : {
                             "URL":('wpanel/<int:manage_id>/letsencrypt', "Backend.lamp.views.letsencrypt", True),
                             
                         },
                         "Delete Certificate" : {
                             "URL":('wpanel/<int:manage_id>/letsencrypt/<int:insert_id>/delete', "Backend.lamp.views.letsencrypt_delete", False),
                           "COMMAND":{
                                 1:('SCRIPT', 'deletelets_ubunt_18_04_x86.sh')
                                 }
                         },
                         "Renew Certificate" : {
                             "URL":('wpanel/<int:manage_id>/letsencrypt/<int:insert_id>/renew', "Backend.lamp.views.letsencrypt_renew", False)
                         },
              }
        
        }
        },

        5:{
        'NAME':'HaProxy',
        'NAV_NAME' : 'HAPoxy',
        'APP_NAME' : 'loadBalancer',
        'DESCRIPTION':'HAProxy is a software that provides a high availability load balancer and proxy server for TCP and HTTP-based applications that spreads requests across multiple servers.',
        'VERSION':'1.8',
        'INIT_COMMAND' : {
            1:[('sudo apt-get update')],
        },
        'INSTALLATION_BASH_SCRIPT' : {
            1:[('SCRIPT', 'haproxy_ubunt.sh')]
        },

        'CONTROL_PANEL' : {}
        },
        7:{
        'NAME':'vsftpd',
        'SERVICE_VIEW' : True,
        'NAV_NAME' : 'PHP',
        'APP_NAME' : 'lamp',
        'DESCRIPTION':'',
        'DEPENDENCIES' : [1],
        'VERSION':'7.5',
        'INIT_COMMAND' : {
            1:[('sudo apt-get update', 'sudo apt-get upgrade')],
        },
        'INSTALLATION_BASH_SCRIPT' : {
            1:[('SCRIPT', 'lets_encrypt_18_04_x86.sh')]
        },
        'CONTROL_PANEL' : {
            'Lets Encrypt':{
                        "ICON" : {
                             "URL":('fa fa-certificate', "Backend.lamp.views.add", False)
                         },
                        "Create Certificate" : {
                             "URL":('wpanel/<int:manage_id>/letsencrypt', "Backend.lamp.views.letsencrypt", True),
                             
                         },
                         "Delete Certificate" : {
                             "URL":('wpanel/<int:manage_id>/letsencrypt/<int:insert_id>/delete', "Backend.lamp.views.letsencrypt_delete", False),
                           "COMMAND":{
                                 1:('SCRIPT', 'deletelets_ubunt_18_04_x86.sh')
                                 }
                         },
                         "Renew Certificate" : {
                             "URL":('wpanel/<int:manage_id>/letsencrypt/<int:insert_id>/renew', "Backend.lamp.views.letsencrypt_renew", False)
                         },
              }
        
        }
        }

    }


PACKAGES_DETAILS = {
        1:{
            'NAME' : 'APACHE WEB SERVER',
            'SERVICE_VIEW' : True,
            'NAV_NAME' : 'DOMAIN',
            'APP_NAME' : 'lamp',
            'DESCRIPTION':'The Apache HTTP Server, colloquially called Apache, is free and open-source cross-platform web server software, released under the terms of Apache License 2.0. Apache is developed and maintained by an open community of developers under the auspices of the Apache Software Foundation.',
            'TAG':'Software',
            'VERSION':'v2.2',
            'CONTROL_TREE':{
                'Website' : ['Addon Domain', 'Delete Domain'],
                'Monitor' : ['Apache Logs', 'Error Logs']
                
            },
            'HTML':'',
            'IMG' : [],
            'BUNDLE' : ['LAMP STACK']

        },
        6:{
            'NAME' : 'Lets Encrypt SSL',
            'SERVICE_VIEW' : True,
            'NAV_NAME' : 'DOMAIN',
            'APP_NAME' : 'lamp',
            'DESCRIPTION':'Lets Encrypt is a non-profit certificate authority run by Internet Security Research Group that provides X.509 certificates for Transport Layer Security encryption at no charge. The certificate is valid for 90 days, during which renewal can take place at any time.',
            'TAG':'Software',
            'VERSION':'',
            'CONTROL_TREE':{
                'Website' : ['Create Certificate', 'Renew Certificate' ],
                'Alert' : ['Expiry Notifier']
                
            },
            'HTML':'',
            'IMG' : [],
            'BUNDLE' : ['LAMP STACK']

        }
    }