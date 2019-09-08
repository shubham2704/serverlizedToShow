SERVER_OS_DISTRIBUTION = {
    1: ['Ubuntu', '18.8'],
    2: ['CentOS', '2']
}

STACK_DIST = {
    1:{
        'NAME' : 'LAMP',
        'DESCRIPTION' : 'LAMP',
        'PACKAGES':(1, 2, 3),
        'PACKAGES_COUNT': 3
    }
}


PACKAGES = {
    1:{
        'NAME' : 'APACHE WEB SERVER',
        'DESCRIPTION':'',
        'VERSION':'',
        'INIT_COMMAND' : {
            1:[('sudo apt-get update', 'sudo apt-get upgrade')],
        },
        'INSTALLATION_COMMAND' : {
            1:[('INSTALLATION', 'sudo aptget install apache2')]
        },
        'CONTROL_PANEL' : {
            1:{
                'WEBSITE':{
                    'ADD DOMAIN':{
                     'PARAMETER':2,
                     'BASH_SCRIPT':'',
                     'PARAMETER_NAME':('domain_name', 'website_folder')
                    }
                }
            }
        }

    }
}