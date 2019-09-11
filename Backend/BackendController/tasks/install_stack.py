from celery.decorators import task
from django.conf import settings
import paramiko
import json
from ..server_config import SERVER_OS_DISTRIBUTION, STACK_DIST, PACKAGES
from Backend.servers.models import list as server_list
from ..contri import sendNotification
import os
import ntpath


PROJECT_PATH = os.path.abspath(os.path.dirname(__name__))


@task(name="install Server")

def installStack(insert_id = 0):
    
    
    try:
        get_server = server_list.objects.get(id=insert_id)
        os_id = get_server.distribution_id
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.load_system_host_keys()
        client.connect(get_server.server_ip, username=get_server.superuser, password=get_server.password)
        t = paramiko.Transport(get_server.server_ip, 22)
        t.connect(username=get_server.superuser,password=get_server.password)
        sftp = paramiko.SFTPClient.from_transport(t)
        PKG_LST = json.loads(get_server.JSON_PKG_LST)
        stdin,stdout,stderr=client.exec_command( SERVER_OS_DISTRIBUTION[os_id][2] + " mkdir /etc/serverlized")
        #print(stderr.readlines)
        
        
        for pkg_id in PKG_LST:
            Package = PACKAGES[pkg_id]['INSTALLATION_BASH_SCRIPT']
            sel_OS = Package[os_id]
            for get_cmd in sel_OS:
                    
                    #sendNotification(get_server.user_id.id, 'toast', 'success', 'Package Installed', '<b>'+STACK_DIST[get_server.stack_id]['NAME'] +'</b> is succesfully installed in ' + get_server.server_name + '  (' + get_server.server_ip + ').')
                    

                    if get_cmd[0] == "SCRIPT":
                        file_upload =  os.path.join(PROJECT_PATH,'Backend','BackendController', 'bash_script', get_cmd[1])
                        sftp.put(file_upload, "/etc/serverlized/" + ntpath.basename(file_upload))
                        print(" cd  /etc/serverlized/; ./" + ntpath.basename(file_upload))
                        print(" cd  /etc/serverlized/; chmod +x " + ntpath.basename(file_upload))
                        sendNotification(get_server.user_id.id, 'toast', 'success', 'Started Installing', '<b>'+ PACKAGES[pkg_id]['NAME'] +'</b> is started installing on ' + get_server.server_name + '  (' + get_server.server_ip + ').')
                        client.exec_command("cd  /etc/serverlized/; chmod +x " + ntpath.basename(file_upload))
                        stdidn,stddout,stdderr=client.exec_command(" cd  /etc/serverlized/; ./" + ntpath.basename(file_upload))
                        client.exec_command( SERVER_OS_DISTRIBUTION[os_id][2] + " rm /etc/serverlized/" + ntpath.basename(file_upload))
                        print ("stderr: ", stdderr.readlines())
                        print ("pwd: ", stddout.readlines())
                        print ("INSTALLED : " +  ntpath.basename(file_upload))
                        sendNotification(get_server.user_id.id, 'toast', 'success', 'Package Installed', '<b>'+ PACKAGES[pkg_id]['NAME'] +'</b> is succesfully installed on ' + get_server.server_name + '  (' + get_server.server_ip + ').')
        
                        

                    if get_cmd[0] == "COMMAND":
                        client.exec_command( SERVER_OS_DISTRIBUTION[os_id][2] + get_cmd[1])
                        print ("COMMAND : " +  get_cmd[1])

                    if get_cmd[0] == "FUNCTION":
                        if get_cmd[1] == "welcomepage":
                            client.exec_command( SERVER_OS_DISTRIBUTION[os_id][2] + " rm /var/www/html/index.html")
                            file_upload =  os.path.join(PROJECT_PATH,'Backend','BackendController', 'bash_script', 'welcome.html')
                            #print(file_upload)
                            sftp.put(file_upload, "/var/www/html/index.html")

        get_server.server_status = "Active"
        get_server.running_status = "Running"
        get_server.save()
                        
           
        client.close()
        sftp.close()
        sendNotification(get_server.user_id.id, 'toast', 'success', 'Stack Installed', '<b>'+ STACK_DIST[get_server.stack_id]['NAME'] +'</b> is succesfully installed in ' + get_server.server_name + '  (' + get_server.server_ip + ').')
        
        return "Installed"

        
    except Exception as e:
        if get_server.user_id.id is not None:
            print("Send")
            get_server.server_status = "Error"
            get_server.running_status = "Error"
            get_server.save()
            sendNotification(get_server.user_id.id, 'toast', 'error', 'Error Occured', 'Error was occured while installing Stack on ' + get_server.server_name + '  (' + get_server.server_ip + '), Please contact use for asistance.')
        print(e)
    

    