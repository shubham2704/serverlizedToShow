from celery.decorators import task
from django.conf import settings
import paramiko
import json
from ..server_config import SERVER_OS_DISTRIBUTION, STACK_DIST, PACKAGES, PYTHON_VERSION_DIC
from Backend.servers.models import list as server_list, Pkg_inst_data, output as server_output
from Backend.lamp.models import domain as domain_s, mysql_user, mysql_database, ssl, lets_encrypt, ftp_account
from Backend.django_auto.models import virtual_env, deploy as dj_dep
from Backend.loadBalancer.models import config as HAPoxyModel, domains as HAProxy_Domains, replicate_file
from ..contri import sendNotification
from ..ConfigBuilder import HAProxy as HAProxyBuilder
import os, traceback, ntpath, requests, sys

PROJECT_PATH = os.path.abspath(os.path.dirname(__name__))




@task(name="Deploy Django Project")
def DeployDjango(insert_id = 0):
    try:
        inse_id = dj_dep.objects.get(id = insert_id)
        get_server = inse_id.server
        os_id = get_server.distribution_id
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.load_system_host_keys()
        client.connect(get_server.server_ip, username=get_server.superuser, password=get_server.password)
        t = paramiko.Transport(get_server.server_ip, 22)
        t.connect(username=get_server.superuser,password=get_server.password)
        sftp = paramiko.SFTPClient.from_transport(t)

        GetPKG = PACKAGES[8]['CONTROL_PANEL']['Django Projects']['Deploy']['COMMAND'][get_server.distribution_id][1]
        file_upload =  os.path.join(PROJECT_PATH,'Backend','BackendController', 'bash_script', GetPKG)
        sftp.put(file_upload, "/etc/serverlized/" + ntpath.basename(file_upload))
        client.exec_command("cd  /etc/serverlized/; chmod +x " + ntpath.basename(file_upload))
        v = PYTHON_VERSION_DIC[inse_id.python_inter][get_server.distribution_id][0]
        cmd = " " + v  + " " + inse_id.envirnment_name + " CREATE"
        print(" cd  /etc/serverlized/; ./" + ntpath.basename(file_upload) + cmd)
        stdidn,stddout,stdderr=client.exec_command(" cd  /etc/serverlized/; ./" + ntpath.basename(file_upload) + cmd)
        
        
        response = []
                        
        for lin in stdderr:
            response.append(str(lin))

        server_output.objects.create(
            server = get_server,
            user = get_server.user_id,
            PackageId = 6,
            command = "Deploy Django Env - " + inse_id.domain.domain_name,
            output = json.dumps(response)
        )


        notifications.objects.create(
            server = get_server,
            message = "Django Environment Projects is Deployed",
            seen = False,
            icon = "check",
            color = "success",
            user = get_server.user_id
        )


        sendNotification(get_server.user_id.id, 'toast', 'success', "Django Project Deployed" , 'Django Project is succesfully Deployed on ' + get_server.server_name + '  (' + get_server.server_ip + ').')
        inse_id.status = "Configured"
        inse_id.save()

    except Exception as e:
        print(e)
        sendNotification(get_server.user_id.id, 'toast', 'error', ' Error Ocurred', 'Django Project is not Deployed on ' + get_server.server_name + '  (' + get_server.server_ip + ').')    
        inse_id.delete()



@task(name="Setup Virtual")
def SetupVirtualENV(insert_id = 0):
    try:
        inse_id = virtual_env.objects.get(id = insert_id)
        get_server = inse_id.server
        os_id = get_server.distribution_id
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.load_system_host_keys()
        client.connect(get_server.server_ip, username=get_server.superuser, password=get_server.password)
        t = paramiko.Transport(get_server.server_ip, 22)
        t.connect(username=get_server.superuser,password=get_server.password)
        sftp = paramiko.SFTPClient.from_transport(t)

        GetPKG = PACKAGES[9]['CONTROL_PANEL']['Virtual Environment']['SetupEnV']['COMMAND'][get_server.distribution_id][1]
        file_upload =  os.path.join(PROJECT_PATH,'Backend','BackendController', 'bash_script', GetPKG)
        sftp.put(file_upload, "/etc/serverlized/" + ntpath.basename(file_upload))
        client.exec_command("cd  /etc/serverlized/; chmod +x " + ntpath.basename(file_upload))
        v = PYTHON_VERSION_DIC[inse_id.python_inter][get_server.distribution_id][0]
        cmd = " " + v  + " " + inse_id.envirnment_name + " CREATE"
        print(" cd  /etc/serverlized/; ./" + ntpath.basename(file_upload) + cmd)
        stdidn,stddout,stdderr=client.exec_command(" cd  /etc/serverlized/; ./" + ntpath.basename(file_upload) + cmd)
        
        
        response = []
                        
        for lin in stdderr:
            response.append(str(lin))

        server_output.objects.create(
            server = get_server,
            user = get_server.user_id,
            PackageId = 6,
            command = "Setup Virtual Env - " + inse_id.envirnment_name,
            output = json.dumps(response)
        )
        sendNotification(get_server.user_id.id, 'toast', 'success', "Virtual Env Created" , 'Virtual Env is succesfully created on ' + get_server.server_name + '  (' + get_server.server_ip + ').')
        inse_id.status = "Configured"
        inse_id.save()

    except Exception as e:
        print(e)
        sendNotification(get_server.user_id.id, 'toast', 'error', ' Error Ocurred', 'Virtual Env is not created on ' + get_server.server_name + '  (' + get_server.server_ip + ').')    
        inse_id.delete()




@task(name="Create FTP Account")
def CreateFTPAccount(insert_id = 0):
    try:
        inse_id = ftp_account.objects.get(id = insert_id)
        get_server = inse_id.server
        os_id = get_server.distribution_id
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.load_system_host_keys()
        client.connect(get_server.server_ip, username=get_server.superuser, password=get_server.password)
        t = paramiko.Transport(get_server.server_ip, 22)
        t.connect(username=get_server.superuser,password=get_server.password)
        sftp = paramiko.SFTPClient.from_transport(t)

        GetPKG = PACKAGES[7]['CONTROL_PANEL']['FTP Account']['Create FTP Account']['COMMAND'][get_server.distribution_id][1]
        file_upload =  os.path.join(PROJECT_PATH,'Backend','BackendController', 'bash_script', GetPKG)
        sftp.put(file_upload, "/etc/serverlized/" + ntpath.basename(file_upload))
        client.exec_command("cd  /etc/serverlized/; chmod +x " + ntpath.basename(file_upload))
        cmd = " " + inse_id.password + " " + inse_id.username + " " + inse_id.folder + " CREATE"
        print(" cd  /etc/serverlized/; ./" + ntpath.basename(file_upload) + cmd)
        stdidn,stddout,stdderr=client.exec_command(" cd  /etc/serverlized/; ./" + ntpath.basename(file_upload) + cmd)
        
        response = []
                        




@task(name="Delete FTP Account")
def DeleteFTPAccount(insert_id = 0):
    try:
        inse_id = ftp_account.objects.get(id = insert_id)
        get_server = inse_id.server
        os_id = get_server.distribution_id
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.load_system_host_keys()
        client.connect(get_server.server_ip, username=get_server.superuser, password=get_server.password)
        t = paramiko.Transport(get_server.server_ip, 22)
        t.connect(username=get_server.superuser,password=get_server.password)
        sftp = paramiko.SFTPClient.from_transport(t)

        GetPKG = PACKAGES[7]['CONTROL_PANEL']['FTP Account']['Create FTP Account']['COMMAND'][get_server.distribution_id][1]
        file_upload =  os.path.join(PROJECT_PATH,'Backend','BackendController', 'bash_script', GetPKG)
        sftp.put(file_upload, "/etc/serverlized/" + ntpath.basename(file_upload))
        client.exec_command("cd  /etc/serverlized/; chmod +x " + ntpath.basename(file_upload))
        cmd = " " + inse_id.password + " " + inse_id.username + " " + inse_id.folder + " DELETE"
        print(" cd  /etc/serverlized/; ./" + ntpath.basename(file_upload) + cmd)
        stdidn,stddout,stdderr=client.exec_command(" cd  /etc/serverlized/; ./" + ntpath.basename(file_upload) + cmd)
        
        response = []
                        
        
        sendNotification(get_server.user_id.id, 'toast', 'success', "FTP Account Deleted" , 'FTP account is succesfully deleted on ' + get_server.server_name + '  (' + get_server.server_ip + ').')
        inse_id.delete()

    except Exception as e:
        print(e)
        sendNotification(get_server.user_id.id, 'toast', 'error', ' Error Ocurred', 'FTP account is not deleted, try again, on ' + get_server.server_name + '  (' + get_server.server_ip + ').')    
       





@task(name="Configure Lets Encrypt")
def ConfigLetsEncrypt(insert_id = 0):
    try:
        inse_id = lets_encrypt.objects.get(id = insert_id)
        get_server = inse_id.server
        domain_get = inse_id.domain
        os_id = get_server.distribution_id
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.load_system_host_keys()
        client.connect(get_server.server_ip, username=get_server.superuser, password=get_server.password)
        
     
                            
            for lin in stdderr:
                response.append(str(lin))

            server_output.objects.create(
                server = get_server,
                user = get_server.user_id,
                PackageId = 6,
                command = "Configure Lets Encrypt - " + a,
                output = json.dumps(response)
            )
            sendNotification(get_server.user_id.id, 'toast', 'success', "SSL Configured" , 'Lets encrypt is succesfully configured for '+ a +' on ' + get_server.server_name + '  (' + get_server.server_ip + ').')
            inse_id.status = "Configured"
            inse_id.save()

    except Exception as e:
        print(e)
        sendNotification(get_server.user_id.id, 'toast', 'error', ' Error Ocurred', 'Lets encrypt is not configured for '+ a +' on ' + get_server.server_name + '  (' + get_server.server_ip + ').')    
        inse_id.delete()




@task(name="Package Restart")
def RestartPackage(package_id = 0, server_id = 0, dic_name = ""):
    try:
        get_server = server_list.objects.get(id=server_id)
        get_package = Pkg_inst_data.objects.get(server=get_server, PackageId = package_id)
        os_id = get_server.distribution_id
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.load_system_host_keys()
        client.connect(get_server.server_ip, username=get_server.superuser, password=get_server.password)
        GetRestartCommand = PACKAGES[package_id]['CONTROL_PANEL'][dic_name]['Restart']['COMMAND'][os_id][1]
        
        stdidn,stddout,stdderr=client.exec_command( SERVER_OS_DISTRIBUTION[os_id][2] + " " + GetRestartCommand)
        print ("pwd: ", stddout.readlines())
        sendNotification(get_server.user_id.id, 'toast', 'success', PACKAGES[package_id]['NAME'] + ' RESTARTED', ''+ PACKAGES[package_id]['NAME'] +' is succesfully restart on ' + get_server.server_name + '  (' + get_server.server_ip + ').')
        get_package.PackageStatus = "RUNNING"
        get_package.save()

    except:
        sendNotification(get_server.user_id.id, 'toast', 'error', ' Error Ocurred', ''+ PACKAGES[package_id]['NAME'] +' is unable to restart on ' + get_server.server_name + '  (' + get_server.server_ip + ').')    




@task(name="Package Stop")
def StopPackage(package_id = 0, server_id = 0, dic_name = ""):
    try:
        get_server = server_list.objects.get(id=server_id)
        get_package = Pkg_inst_data.objects.get(server=get_server, PackageId = package_id)
        os_id = get_server.distribution_id
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.load_system_host_keys()
        client.connect(get_server.server_ip, username=get_server.superuser, password=get_server.password)
        GetStopCommand = PACKAGES[package_id]['CONTROL_PANEL'][dic_name]['Stop']['COMMAND'][os_id][1]
        print(SERVER_OS_DISTRIBUTION[os_id][2] + " " + GetStopCommand)
        stdidn,stddout,stdderr=client.exec_command( SERVER_OS_DISTRIBUTION[os_id][2] + " " + GetStopCommand)
        print ("pwd: ", stdderr.readlines())
        sendNotification(get_server.user_id.id, 'toast', 'success', PACKAGES[package_id]['NAME'] + ' STOPPED', ''+ PACKAGES[package_id]['NAME'] +' is succesfully stopped on ' + get_server.server_name + '  (' + get_server.server_ip + ').')
        get_package.PackageStatus = "STOP"
        get_package.save()
        
    except:
        sendNotification(get_server.user_id.id, 'toast', 'error', ' Error Ocurred', ''+ PACKAGES[package_id]['NAME'] +' is unable to stopped on ' + get_server.server_name + '  (' + get_server.server_ip + ').')    



@task(name="MySQL Database Delete")

def MySQLDatabaseDelete(insert_id = 0):
    try:
        mysql_database_det = mysql_database.objects.get(id=insert_id)
        get_server = mysql_database_det.server
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
        get_server = mysql_database_det.server
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
        get_server = mysql_user_det.server
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
        get_server = mysql_user_det.server
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
        
       
    
    except Exception as e:
         if mysql_user_det.user.id is not None:

            notifications.objects.create(
            server = get_server,
            message = "Error Occured, Database Use is Not Created - " + mysql_user_det.name + ", Try Again!",
            seen = False,
            icon = "times",
            color = "danger",
            user = get_server.user_id
            )

            mysql_user_det.status = "Error"
            mysql_user_det.save()
            sendNotification(mysql_user_det.user.id, 'toast', 'error', 'Error Occured', 'Error was occured while Configuring Domain on ' + mysql_user_det.server.server_name + '  (' + mysql_user_det.server.server_ip + '), Please contact use for asistance.')
            mysql_user_det.delete()
            
         print(e)

@task(name="Lamp Domain Delete")

def DeleteLampDomain(insert_id = 0):
    
    try:
        domain_get = domain_s.objects.get(id=insert_id)
        client = paramiko.SSHClient()
        get_server = domain_get.server
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.load_system_host_keys()
        client.connect(domain_get.server.server_ip, username=domain_get.server.superuser, password=domain_get.server.password)
        t = paramiko.Transport(domain_get.server.server_ip, 22)
        t.connect(username=domain_get.server.superuser,password=domain_get.server.password)
        sftp = paramiko.SFTPClient.from_transport(t)
        GetPKG = PACKAGES[1]['CONTROL_PANEL']['Website']['Addon Domain']['COMMAND'][domain_get.server.stack_id][1]
        file_upload =  os.path.join(PROJECT_PATH,'Backend','BackendController', 'bash_script', GetPKG)
        
        sftp.put(file_upload, "/etc/serverlized/" + ntpath.basename(file_upload))
        client.exec_command("cd  /etc/serverlized/; chmod +x " + ntpath.basename(file_upload))
       

        
    except Exception as e:
         if domain_get.user.id is not None:
            domain_get.status = "Error"
            domain_get.save()
            sendNotification(domain_get.user.id, 'toast', 'error', 'Error Occured', 'Error was occured while Configuring Domain on ' + domain_get.server.server_name + '  (' + domain_get.server.server_ip + '), Please contact use for asistance.')
         print(e)
    





@task(name="Install Pacakge in Managed Server")
def InstallServerPackage(server_id = 0, package_id = 0):
    try:
        getserver = server_list.objects.get(id=server_id)
        get_installed_pkg_lst = json.loads(getserver.JSON_PKG_LST)
        
        package_details = PACKAGES[package_id]
        get_server = getserver
        check = package_id in get_installed_pkg_lst
        print(check)

        if check == False:
            
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.load_system_host_keys()
            client.connect(getserver.server_ip, username=getserver.superuser, password=getserver.password)
            t = paramiko.Transport(getserver.server_ip, 22)
            t.connect(username=getserver.superuser,password=getserver.password)
            sftp = paramiko.SFTPClient.from_transport(t)

            for get_cmd in package_details['INSTALLATION_BASH_SCRIPT'][getserver.distribution_id]:
               

    except Exception as e:
        print(e)
        sendNotification(getserver.user_id.id, 'toast', 'error', 'Installation Failed', '<b> ' + package_details['NAME'] +'</b> is succesfully installed in ' + getserver.server_name + '  (' + getserver.server_ip + ').')
        



@task(name="Lamp Domain Add")

def ConfigureLampDomain(insert_id = 0):
    
    try:
        domain_get = domain_s.objects.get(id=insert_id)
        get_server = domain_get.server
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.load_system_host_keys()
        client.connect(domain_get.server.server_ip, username=domain_get.server.superuser, password=domain_get.server.password)
        t = paramiko.Transport(domain_get.server.server_ip, 22)
        t.connect(username=domain_get.server.superuser,password=domain_get.server.password)
        sftp = paramiko.SFTPClient.from_transport(t)
        GetPKG = PACKAGES[3]['CONTROL_PANEL']['Website']['Addon Domain']['COMMAND'][domain_get.server.distribution_id][1]
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
        file_upload =  os.path.join(PROJECT_PATH,'Backend','BackendController', 'bash_script', 'welcome.html')
        #print(file_upload)
        sftp.put(file_upload, "/var/www/"+ domain_get.folder +"/index.html")

        #client.exec_command( SERVER_OS_DISTRIBUTION[domain_get.server.distribution_id][2] + " rm /etc/serverlized/" + ntpath.basename(file_upload))

        domain_get.status = "Active"
        domain_get.save()
                        
           
     
        
    except Exception as e:
         traceback.print_exc(limit=1, file=sys.stdout)
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
        
        
       
        
    except Exception as e:
        if get_server.user_id.id is not None:
            print("Send")
            get_server.server_status = "Error"
            get_server.running_status = "Error"
            get_server.save()
            sendNotification(get_server.user_id.id, 'toast', 'error', 'Error Occured', 'Error was occured while installing Stack on ' + get_server.server_name + '  (' + get_server.server_ip + '), Please contact use for asistance.')
        print(e)


@task(name="Renew Lets Encrypt")

def RenweLetsEncrypt(insert_id = 0):
      try:
        inse_id = lets_encrypt.objects.get(id = insert_id)
        get_server = inse_id.server
        domain_get = inse_id.domain
        os_id = get_server.distribution_id
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.load_system_host_keys()
        client.connect(get_server.server_ip, username=get_server.superuser, password=get_server.password)
        
        if domain_get.subdomain != '':
            a = domain_get.subdomain + "." + domain_get.domain_name
        else:
            a = domain_get.domain_name

        #conn = requests.get("https://"+a)
        #print(conn.status_code)
        conn = 200
        if conn == 200:

            
            GetConfigCommand = "certbot renew --cert-name "+ a +" --dry-run"
            
            print(GetConfigCommand)
            stdidn,stddout,stdderr=client.exec_command( SERVER_OS_DISTRIBUTION[os_id][2] + " " + GetConfigCommand)
            print ("pwd: ", stddout.readlines())
            response = []
                            
            for lin in stdderr:
                response.append(str(lin))

            server_output.objects.create(
                server = get_server,
                user = get_server.user_id,
                PackageId = 6,
                command = "Renew Lets Encrypt - " + a,
                output = json.dumps(response)
            )
            sendNotification(get_server.user_id.id, 'toast', 'success', "SSL Renewed" , 'Lets encrypt is succesfully renewed for '+ a +' on ' + get_server.server_name + '  (' + get_server.server_ip + ').')
            inse_id.status = "Configured"
            inse_id.save()

      except Exception as e:
        print(e)
        sendNotification(get_server.user_id.id, 'toast', 'error', ' Error Ocurred', 'Lets encrypt is not renewed for '+ a +' on ' + get_server.server_name + '  (' + get_server.server_ip + ').')    
        #inse_id.delete()


@task(name="Delete Lets Encrypt")

def DeleteLetsEncrypt(insert_id = 0):
      try:
        inse_id = lets_encrypt.objects.get(id = insert_id)
        get_server = inse_id.server
        domain_get = inse_id.domain
        os_id = get_server.distribution_id
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.load_system_host_keys()
        client.connect(get_server.server_ip, username=get_server.superuser, password=get_server.password)
        t = paramiko.Transport(get_server.server_ip, 22)
        t.connect(username=get_server.superuser,password=get_server.password)
        sftp = paramiko.SFTPClient.from_transport(t)
        
        if domain_get.subdomain != '':
            a = domain_get.subdomain + "." + domain_get.domain_name
        else:
            a = domain_get.domain_name

        #conn = requests.get("https://"+a)
        #print(conn.status_code)
        conn = 200
     


@task(name="Replicate Files")
def ReplicateHAProxyFiles(insert_id = 0):
    try:
        inse_id = replicate_file.objects.get(id = insert_id)
        get_server = inse_id.server
        filename_uploaded = inse_id.file_name
        os_id = get_server.distribution_id
        json_ld = json.loads(inse_id.connected_domain.domain_insert_withftp_dict)
        ROOT_COMMAND = SERVER_OS_DISTRIBUTION[os_id][2]
       
        inse_dic = {}
        for key, send_async_request in json_ld.items():
            server_id = send_async_request['server']
            getnode = server_list.objects.get(id = server_id)
            ftp = send_async_request['ftp']
            status = send_async_request['file_replication_status']

            if status == "Not Done":
            
                getftp = ftp_account.objects.get(id = ftp)
                
                upload_path = "/var/www/" + getftp.folder + '/uploaded_serverlized_file.zip'
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                client.load_system_host_keys()
                client.connect(getnode.server_ip, username=getnode.superuser, password=getnode.password)
                t = paramiko.Transport(getnode.server_ip, 22)
                t.connect(username=getnode.superuser,password=getnode.password)
                sftp = paramiko.SFTPClient.from_transport(t)
                file_ip = os.path.join(PROJECT_PATH,'templates','media', filename_uploaded)
                
                st = sftp.put(file_ip, upload_path)
                print(" cd /var/www/" + getftp.folder + '; unzip uploaded_serverlized_file.zip; rm -R uploaded_serverlized_file.zip')
                stdidn,stddout,stdderr=client.exec_command("cd /var/www/" + getftp.folder + '; unzip uploaded_serverlized_file.zip; rm -R uploaded_serverlized_file.zip')
                sendNotification(get_server.user_id.id, 'toast', 'success', "File Replicated in a Server" , 'File is Replicated to node servers ' + getnode.server_name + '  (' + getnode.server_ip + ').')
                
                inse_dic[key] = {
                                'domain': send_async_request['domain'],
                                'ftp' :send_async_request['ftp'],
                                'file_replication_status' : "Done",
                                'server' : send_async_request['server']
                            }
                inse_id.connected_domain.domain_insert_withftp_dict = json.dumps(inse_dic)
                inse_id.connected_domain.save()
                

            
            print(st)

            #ConfigureLampDomain(send_async_request['domain'])
            #CreateFTPAccount(send_async_request['ftp'])


        sendNotification(get_server.user_id.id, 'toast', 'success', "File Replicated" , 'File is Replicated to all node servers of main ' + get_server.server_name + '  (' + get_server.server_ip + ').')
        inse_id.status = "Configured"
        inse_id.save()

    except Exception as e:
        print(e)
        traceback.print_exc(limit=1, file=sys.stdout)
        sendNotification(get_server.user_id.id, 'toast', 'error', ' Error Ocurred', 'Domains is not Replicated to all node servers of main ' + get_server.server_name + '  (' + get_server.server_ip + ').')    
        #inse_id.delete()
