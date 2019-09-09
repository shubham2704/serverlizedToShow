
SERVER_OS_DISTRIBUTION = {
    1: ['Ubuntu', '18.04 x64']
}

STACK_DIST = {
    1:{
        'NAME' : 'LAMP',
        'DESCRIPTION' : 'A LAMP Stack is a set of software that can be used to create and host websites and web applications.',
        'PRICE' : 0.00 ,
        'PACKAGES':(1, 2, 3),
        'PACKAGES_COUNT': 3
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
            1:[('sudo apt-get update', 'sudo apt-get upgrade')],
        },
        'INSTALLATION_COMMAND' : {
            1:[('INSTALLATION', 'sudo apt get install apache2')]
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
        'INSTALLATION_COMMAND' : {
            1:[('INSTALLATION', 'sudo apt get install mysql-server'), ('PHPMYADMIN', 'sudo apt get install mysql-server')]
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
        'NAME' : 'PHP 7',
        'NAV_NAME' : 'PHP',
        'APP_NAME' : 'lamp',
        'DESCRIPTION':'',
        'VERSION':'7.5',
        'INIT_COMMAND' : {
            1:[('sudo apt-get update', 'sudo apt-get upgrade')],
        },
        'INSTALLATION_COMMAND' : {
            1:[('INSTALLATION', 'sudo apt get install mysql-server')]
        },
        'CONTROL_PANEL' : {}
        }

    }
