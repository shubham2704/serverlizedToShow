from celery.decorators import task
from django.conf import settings
import paramiko
import json
from ..server_config import SERVER_OS_DISTRIBUTION, STACK_DIST, PACKAGES
from Backend.servers.models import list as server_list
from Backend.lamp.models import domain as domain_s, mysql_user, mysql_database
from ..contri import sendNotification
import os
import ntpath

PROJECT_PATH = os.path.abspath(os.path.dirname(__name__))


@task(name="MySQL Database Delete")

def MySQLDatabaseDelete(insert_id = 0):
    try:
        mysql_database_det = mysql_database.objects.get(id=insert_id)
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.load_system_host_keys()
        client.connect(mysql_database_det.server.server_ip, username=mysql_database_det.server.superuser, password=mysql_database_det.server.password)
        t = paramiko.Transport(mysql_database_det.server.server_ip, 22)
        t.connect(username=mysql_database_det.server.superuser,password=mysql_database_det.server.password)
        sftp = paramiko.SFTPClient.from_transport(t)
        GetPKG = PACKAGES[2]['CONTROL_PANEL']['MySQL']['Delete Database']['COMMAND'][mysql_database_det.server.stack_id][1]
        file_upload =  os.path.join(PROJECT_PATH,'Backend','BackendController', 'bash_script', GetPKG)
        sftp.put(file_upload, "/etc/serverlized/" + ntpath.basename(file_upload))
        client.exec_command("cd  /etc/serverlized/; chmod +x " + ntpath.basename(file_upload))
        
        if mysql_database_det.mysql_user.remote == True :
            a = mysql_database_det.server.server_ip
        else:
            a = "localhost"
        

        cmd = " delete " + mysql_database_det.mysql_user.name + " " + mysql_database_det.mysql_user.password + " " + a + " " + mysql_database_det.database_name
        print(" cd  /etc/serverlized/; ./" + ntpath.basename(file_upload) + cmd)
        stdidn,stddout,stdderr=client.exec_command(" cd  /etc/serverlized/; ./" + ntpath.basename(file_upload) + cmd)
        
        sendNotification(mysql_database_det.user.id, 'toast', 'success', 'MySQL Database Deleted', ''+ mysql_database_det.database_name +' is succesfully deleted on ' + mysql_database_det.server.server_name + '  (' + mysql_database_det.server.server_ip + ').')
        
        mysql_database_det.delete()
        
    
    except Exception as e:
         if mysql_database_det.user.id is not None:
            mysql_database_det.status = "Error"
            mysql_database_det.save()
            sendNotification(mysql_database_det.user.id, 'toast', 'error', 'Error Occured', 'Error was occured while deleting Database on ' + mysql_database_det.server.server_name + '  (' + mysql_database_det.server.server_ip + '), Please contact use for asistance.')
         
         print(e)



@task(name="Create MySQL Database")

def MySQLDatabaseCreate(insert_id = 0):
    try:
        mysql_database_det = mysql_database.objects.get(id=insert_id)
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.load_system_host_keys()
        client.connect(mysql_database_det.server.server_ip, username=mysql_database_det.server.superuser, password=mysql_database_det.server.password)
        t = paramiko.Transport(mysql_database_det.server.server_ip, 22)
        t.connect(username=mysql_database_det.server.superuser,password=mysql_database_det.server.password)
        sftp = paramiko.SFTPClient.from_transport(t)
        GetPKG = PACKAGES[2]['CONTROL_PANEL']['MySQL']['Create Database']['COMMAND'][mysql_database_det.server.stack_id][1]
        file_upload =  os.path.join(PROJECT_PATH,'Backend','BackendController', 'bash_script', GetPKG)
        sftp.put(file_upload, "/etc/serverlized/" + ntpath.basename(file_upload))
        client.exec_command("cd  /etc/serverlized/; chmod +x " + ntpath.basename(file_upload))
        
        if mysql_database_det.mysql_user.remote == True :
            a = mysql_database_det.server.server_ip
        else:
            a = "localhost"
        

        cmd = " create " + mysql_database_det.mysql_user.name + " " + mysql_database_det.mysql_user.password + " " + a + " " + mysql_database_det.database_name
        print(" cd  /etc/serverlized/; ./" + ntpath.basename(file_upload) + cmd)
        stdidn,stddout,stdderr=client.exec_command(" cd  /etc/serverlized/; ./" + ntpath.basename(file_upload) + cmd)
        
        sendNotification(mysql_database_det.user.id, 'toast', 'success', 'MySQL Database Created', ''+ mysql_database_det.database_name +' is succesfully created on ' + mysql_database_det.server.server_name + '  (' + mysql_database_det.server.server_ip + ').')
        mysql_database_det.status = "Configured"
        mysql_database_det.save()
        
    
    except Exception as e:
         if mysql_database_det.user.id is not None:
            mysql_database_det.status = "Error"
            mysql_database_det.save()
            sendNotification(mysql_database_det.user.id, 'toast', 'error', 'Error Occured', 'Error was occured while Creating Database on ' + mysql_database_det.server.server_name + '  (' + mysql_database_det.server.server_ip + '), Please contact use for asistance.')
         
         print(e)



@task(name="Delete MySQL User")

def MySQLUserDelete(insert_id = 0):
    try:
        mysql_user_det = mysql_user.objects.get(id=insert_id)
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.load_system_host_keys()
        client.connect(mysql_user_det.server.server_ip, username=mysql_user_det.server.superuser, password=mysql_user_det.server.password)
        t = paramiko.Transport(mysql_user_det.server.server_ip, 22)
        t.connect(username=mysql_user_det.server.superuser,password=mysql_user_det.server.password)
        sftp = paramiko.SFTPClient.from_transport(t)
        GetPKG = PACKAGES[2]['CONTROL_PANEL']['MySQL']['Create User']['COMMAND'][mysql_user_det.server.stack_id][1]
        file_upload =  os.path.join(PROJECT_PATH,'Backend','BackendController', 'bash_script', GetPKG)
        sftp.put(file_upload, "/etc/serverlized/" + ntpath.basename(file_upload))
        client.exec_command("cd  /etc/serverlized/; chmod +x " + ntpath.basename(file_upload))
        
        if mysql_user_det.remote == True :
            a = mysql_user_det.server.server_ip
        else:
            a = "localhost"
        

        cmd = " delete " + mysql_user_det.name + " " + mysql_user_det.password + " " + a
        print(" cd  /etc/serverlized/; ./" + ntpath.basename(file_upload) + cmd)
        stdidn,stddout,stdderr=client.exec_command(" cd  /etc/serverlized/; ./" + ntpath.basename(file_upload) + cmd)
        
        sendNotification(mysql_user_det.user.id, 'toast', 'success', 'MySQL User Deleted', ''+ mysql_user_det.name +' is Succesfully Deleted on ' + mysql_user_det.server.server_name + '  (' + mysql_user_det.server.server_ip + '), Please contact use for asistance.')
        mysql_user_det.delete()
        
    
    except Exception as e:
         if mysql_user_det.user.id is not None:
            mysql_user_det.status = "Error"
            mysql_user_det.save()
            sendNotification(mysql_user_det.user.id, 'toast', 'error', 'Error Occured', 'Error was occured while Configuring Domain on ' + mysql_user_det.server.server_name + '  (' + mysql_user_det.server.server_ip + '), Please contact use for asistance.')
         
         print(e)



@task(name="Create MySQL User")

def MySQLUserAdd(insert_id = 0):
    try:
        mysql_user_det = mysql_user.objects.get(id=insert_id)
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.load_system_host_keys()
        client.connect(mysql_user_det.server.server_ip, username=mysql_user_det.server.superuser, password=mysql_user_det.server.password)
        t = paramiko.Transport(mysql_user_det.server.server_ip, 22)
        t.connect(username=mysql_user_det.server.superuser,password=mysql_user_det.server.password)
        sftp = paramiko.SFTPClient.from_transport(t)
        GetPKG = PACKAGES[2]['CONTROL_PANEL']['MySQL']['Create User']['COMMAND'][mysql_user_det.server.stack_id][1]
        file_upload =  os.path.join(PROJECT_PATH,'Backend','BackendController', 'bash_script', GetPKG)
        sftp.put(file_upload, "/etc/serverlized/" + ntpath.basename(file_upload))
        client.exec_command("cd  /etc/serverlized/; chmod +x " + ntpath.basename(file_upload))
        
        if mysql_user_det.remote == True :
            a = mysql_user_det.server.server_ip
        else:
            a = "localhost"
        

        cmd = " create " + mysql_user_det.name + " " + mysql_user_det.password + " " + a
        print(" cd  /etc/serverlized/; ./" + ntpath.basename(file_upload) + cmd)
        stdidn,stddout,stdderr=client.exec_command(" cd  /etc/serverlized/; ./" + ntpath.basename(file_upload) + cmd)
        mysql_user_det.status = "Configured"
        mysql_user_det.save()
        sendNotification(mysql_user_det.user.id, 'toast', 'success', 'MySQL User Created', ''+ mysql_user_det.name +' is Succesfully Created on ' + mysql_user_det.server.server_name + '  (' + mysql_user_det.server.server_ip + '), Please contact use for asistance.')
         
        
    
    except Exception as e:
         if mysql_user_det.user.id is not None:
            mysql_user_det.status = "Error"
            mysql_user_det.save()
            sendNotification(mysql_user_det.user.id, 'toast', 'error', 'Error Occured', 'Error was occured while Configuring Domain on ' + mysql_user_det.server.server_name + '  (' + mysql_user_det.server.server_ip + '), Please contact use for asistance.')
         
         print(e)

@task(name="Lamp Domain Delete")

def DeleteLampDomain(insert_id = 0):
    
    try:
        domain_get = domain_s.objects.get(id=insert_id)
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.load_system_host_keys()
        client.connect(domain_get.server.server_ip, username=domain_get.server.superuser, password=domain_get.server.password)
        t = paramiko.Transport(domain_get.server.server_ip, 22)
        t.connect(username=domain_get.server.superuser,password=domain_get.server.password)
        sftp = paramiko.SFTPClient.from_transport(t)
        GetPKG = PACKAGES[1]['CONTROL_PANEL']['WEBSITE']['Addon Domain']['COMMAND'][domain_get.server.stack_id][1]
        file_upload =  os.path.join(PROJECT_PATH,'Backend','BackendController', 'bash_script', GetPKG)
        
        sftp.put(file_upload, "/etc/serverlized/" + ntpath.basename(file_upload))
        client.exec_command("cd  /etc/serverlized/; chmod +x " + ntpath.basename(file_upload))
        if domain_get.subdomain != '':
            a = domain_get.subdomain + "." + domain_get.domain_name
            cmd = " delete " + a + " " + domain_get.folder
        else:
            a = domain_get.domain_name
            cmd = " delete " + domain_get.domain_name + " " + domain_get.folder

        print(" cd  /etc/serverlized/; ./" + ntpath.basename(file_upload) + cmd)
            
        stdidn,stddout,stdderr=client.exec_command(" cd  /etc/serverlized/; ./" + ntpath.basename(file_upload) + cmd)
        print ("stderr: ", stdderr.readlines())
        #client.exec_command( SERVER_OS_DISTRIBUTION[domain_get.server.distribution_id][2] + " rm /etc/serverlized/" + ntpath.basename(file_upload))

        domain_get.delete()
                        
           
        client.close()
        sftp.close()
        sendNotification(domain_get.user.id, 'toast', 'success', 'Domain Deleted', '<b> ' + a +'</b> is succesfully deleted in ' + domain_get.server.server_name + '  (' + domain_get.server.server_ip + ').')
        
        return "Installed"

        
    except Exception as e:
         if domain_get.user.id is not None:
            domain_get.status = "Error"
            domain_get.save()
            sendNotification(domain_get.user.id, 'toast', 'error', 'Error Occured', 'Error was occured while Configuring Domain on ' + domain_get.server.server_name + '  (' + domain_get.server.server_ip + '), Please contact use for asistance.')
         print(e)
    




@task(name="Lamp Domain Add")

def ConfigureLampDomain(insert_id = 0):
    
    try:
        domain_get = domain_s.objects.get(id=insert_id)
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.load_system_host_keys()
        client.connect(domain_get.server.server_ip, username=domain_get.server.superuser, password=domain_get.server.password)
        t = paramiko.Transport(domain_get.server.server_ip, 22)
        t.connect(username=domain_get.server.superuser,password=domain_get.server.password)
        sftp = paramiko.SFTPClient.from_transport(t)
        GetPKG = PACKAGES[1]['CONTROL_PANEL']['WEBSITE']['Addon Domain']['COMMAND'][domain_get.server.stack_id][1]
        file_upload =  os.path.join(PROJECT_PATH,'Backend','BackendController', 'bash_script', GetPKG)
        
        sftp.put(file_upload, "/etc/serverlized/" + ntpath.basename(file_upload))
        client.exec_command("cd  /etc/serverlized/; chmod +x " + ntpath.basename(file_upload))
        if domain_get.subdomain != '':
            a = domain_get.subdomain + "." + domain_get.domain_name
            cmd = " create " + a + " " + domain_get.folder
        else:
            a = domain_get.domain_name
            cmd = " create " + domain_get.domain_name + " " + domain_get.folder

        print(" cd  /etc/serverlized/; ./" + ntpath.basename(file_upload) + cmd)
            
        stdidn,stddout,stdderr=client.exec_command(" cd  /etc/serverlized/; ./" + ntpath.basename(file_upload) + cmd)
        print ("stderr: ", stdderr.readlines())
        #client.exec_command( SERVER_OS_DISTRIBUTION[domain_get.server.distribution_id][2] + " rm /etc/serverlized/" + ntpath.basename(file_upload))

        domain_get.status = "Active"
        domain_get.save()
                        
           
        client.close()
        sftp.close()
        sendNotification(domain_get.user.id, 'toast', 'success', 'Domain Configured', '<b> ' + a +'</b> is succesfully installed in ' + domain_get.server.server_name + '  (' + domain_get.server.server_ip + ').')
        
        return "Installed"

        
    except Exception as e:
         if domain_get.user.id is not None:
            domain_get.status = "Error"
            domain_get.save()
            sendNotification(domain_get.user.id, 'toast', 'error', 'Error Occured', 'Error was occured while Configuring Domain on ' + domain_get.server.server_name + '  (' + domain_get.server.server_ip + '), Please contact use for asistance.')
         print(e)
    



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
    
@task(name="install loadBalancer")

def installStack(insert_id = 0):

    try:
        pass
    except expression as identifier:
        pass
    