from django.shortcuts import render, redirect
from django.core.signing import Signer
from django.contrib import messages
import paramiko
from django.db.models import Q
from ..BackendController.contri import randomString, randomNumber
from ..signup.models import user
from ..BackendController.tasks.install_stack import installStack
from ..BackendController.contri import CheckLogin, getUser
from ..BackendController.server_config import STACK_DIST,SERVER_OS_DISTRIBUTION
from .models import list as server_list, projects
import json

def deploy(request):
    
    login = CheckLogin(request)
    if login == True:
        params = {}
        user = getUser(request)

        params['user'] = user
        params['STACK'] = STACK_DIST
        proj = projects.objects.filter(user_id=user)
        params['PROJECT'] = proj
        params['SERVER_OS_DISTRIBUTION'] = SERVER_OS_DISTRIBUTION

        if request.method == 'POST':

            start_install = True
            
            if 'os' in request.POST:
                os = request.POST['os']
            else:
                start_install = False


            if 'stack' in request.POST:
                stack = request.POST['stack'] 
            else:
                start_install = False  

            ip = request.POST['ip']   
            username = request.POST['username']   
            password = request.POST['password']  
            project = request.POST['project']        
            sr_name = request.POST['sr_name']  
                
            if start_install == True:
                if sr_name!='' and username!='' and password!='' and ip!='' and project!='':
                    try:

                        client = paramiko.SSHClient()
                        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                        client.load_system_host_keys()
                        client.connect(ip, username=username, password=password)
                        get_project = projects.objects.get(id=int(project))
                        count_exis = server_list.objects.filter(server_ip=ip).count()
                        
                        if count_exis == 0:
                            stk = str(STACK_DIST[int(stack)]['NAME']) + " in " + str(SERVER_OS_DISTRIBUTION[int(os)][0] + SERVER_OS_DISTRIBUTION[int(os)][1])
                            
                            obj, insert = server_list.objects.get_or_create(
                                server_name = sr_name,
                                superuser = username,
                                user_id = user,
                                distribution_id = os,
                                stack_id = stack,
                                stack_name = stk,
                                ServerType = "MASTER",
                                server_status = "Installing",
                                server_ip = ip,
                                password = password,
                                project_id = get_project,
                                JSON_PKG_LST = json.dumps(STACK_DIST[int(stack)]['PACKAGES']),
                                Charges = 0.00,
                                running_status = "Installing"
                            )
                            if insert:
                                
                                messages.success(request, "Test Connection is succeed! , Your Stack will be installed in 1  or 2 min and you are ready to manage your server without touching command line. ")
                                installStack.delay(obj.id)

                        else:
                            messages.warning(request, "This server is already managed by Serverlized.")
                        



                    except Exception as e:
                        print(e)
                        messages.warning(request, "Test Connection was failed! , please enter a valid server ip or/and superuser name or/and password.")
                            
                        

                else:
                    messages.warning(request, "Enter your server Super username, IP and password.")

            else:
                messages.warning(request, "Select a OS AND Stack which you want to install on your server and manage.")

        return render(request, "user/deploy.html", params)

    else:
        return redirect("/login")

def panel(request):
    login = CheckLogin(request)
    if login == True:
        params = {}
        user = getUser(request)
        params['user'] = user
        print(user.first_name)
        get_all_servers = server_list.objects.filter(user_id=user, ServerType="MASTER",parent_server='')
        params['servers'] = get_all_servers
        
        params['server_count'] = get_all_servers.count()
        print(params)
        return render(request, "user/dashboard.html", params)
    else:
        return redirect("/login")