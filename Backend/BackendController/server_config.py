
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
        'DESCRIPTION' : '',
        'PRICE' : 0.00 ,
        'PACKAGES':(),
        'PACKAGES_COUNT': 2
    }
    
}

PACKAGES = {
    1:{
        'NAME' : 'APACHE WEB SERVER',
        'NAV_NAME' : 'DOMAIN',
        'APP_NAME' : 'lamp',
        'DESCRIPTION':'',
        'VERSION':'2.2',
        'INIT_COMMAND' : {
            1:[('sudo apt-get -y update', 'sudo apt-get -y upgrade')],
        },
        'INSTALLATION_BASH_SCRIPT' : {
            1:[('SCRIPT', 'apache_ubunt_18_04_x86.sh')]
        },
        'CONTROL_PANEL' : {
            'WEBSITE':{
                        "Add Domain" : {
                             "URL":('wpanel/<int:manage_id>/domain/add', "Backend.lamp.views.add")
                         },
                         "Edit Domain" : {
                             "URL":('wpanel/<int:manage_id>/domain/edit/<int:domain_id>', "Backend.lamp.views.edit")
                         },
                         "Delete Domain" : {
                             "URL":('wpanel/<int:manage_id>/domain/delete//<int:domain_id>', "Backend.lamp.views.delete")
                         }
              }
               
                }
        },
        
        2:{
        'NAME' : 'MySQL',
        'NAV_NAME' : 'Database',
        'APP_NAME' : 'lamp',
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
                        "Add Database" : {
                             "URL":('wpanel/<int:manage_id>/mysql/add', "Backend.lamp.views.add")
                         },
                         "Edit Database" : {
                             "URL":('wpanel/<int:manage_id>/mysql/edit/<int:db_id>', "Backend.lamp.views.edit")
                         },
                         "Delete Database" : {
                             "URL":('wpanel/<int:manage_id>/mysql/delete//<int:db_id>', "Backend.lamp.views.delete")
                         }
              }
               
                }
        },
        3:{
        'NAME' : 'PHP 7.3',
        'NAV_NAME' : 'PHP',
        'APP_NAME' : 'lamp',
        'DESCRIPTION':'',
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
        'APP_NAME' : 'lamp',
        'DESCRIPTION':'',
        'VERSION':'7.5',
        'INIT_COMMAND' : {
            1:[('sudo apt-get update', 'sudo apt-get upgrade')],
        },
        'INSTALLATION_BASH_SCRIPT' : {
            1:[('SCRIPT', 'phpmyadmin_ubunt_18_04_x86.sh'), ('FUNCTION', 'welcomepage')]
        },
        'CONTROL_PANEL' : {}
        }

    }
