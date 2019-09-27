from django.shortcuts import render, redirect
from django.http import  JsonResponse
from django.core.signing import Signer
from django.contrib import messages
import paramiko
from django.db.models import Q
from ..BackendController.contri import randomString, randomNumber
from ..signup.models import user
from ..BackendController.tasks.install_stack import installStack, RestartPackage, StopPackage, InstallServerPackage
from ..BackendController.contri import CheckLogin, getUser, rewrite_menu
from ..BackendController.server_config import STACK_DIST,SERVER_OS_DISTRIBUTION, PACKAGES_DETAILS, PACKAGES
from .models import list as server_list, projects, Pkg_inst_data, output as ser_output
import json

def server_output(request, server_id):
    login = CheckLogin(request)
    if login == True:
        params = {}
        user = getUser(request)
        params['user'] = user
        try:
            getserver = server_list.objects.get(id=server_id)
            params['server'] = getserver
            getPKG = json.loads(getserver.JSON_PKG_LST)
            params['menu'] = rewrite_menu(getserver.JSON_PKG_LST, server_id)
            params['outputs'] = ser_output.objects.filter(user=user, server=getserver)

        except Exception as e:
            print(e)

        return render(request, "user/server_output.html", params)
    else:
        return redirect("/login")


def server_output_view(request, server_id, output_id):
    login = CheckLogin(request)
    if login == True:
        params = {}
        user = getUser(request)
        params['user'] = user
        try:
            getserver = server_list.objects.get(id=server_id)
            params['server'] = getserver
            getPKG = json.loads(getserver.JSON_PKG_LST)
            params['menu'] = rewrite_menu(getserver.JSON_PKG_LST, server_id)
            params['output'] = ser_output.objects.get(id=output_id)
            params['output_js'] = json.loads(params['output'].output)

        except Exception as e:
            print(e)

        return render(request, "user/server_output_view.html", params)
    else:
        return redirect("/login")

def pkg_details(request, pkg_id):
    login = CheckLogin(request)
    if login == True:
        params = {}
        user = getUser(request)
        params['user'] = user
        if pkg_id in PACKAGES_DETAILS:

            params['package'] = PACKAGES_DETAILS[pkg_id]

        return render(request, "user/package_details.html", params)


def pkg_details_server(request,server_id, pkg_id):
    login = CheckLogin(request)
    if login == True:
        params = {}
        user = getUser(request)
        params['user'] = user
        params['pkg_id'] = pkg_id
        if pkg_id in PACKAGES_DETAILS:

            params['package'] = PACKAGES_DETAILS[pkg_id]
            getserver = server_list.objects.get(id=server_id)
            params['server'] = getserver

        return render(request, "user/package_details_server.html", params)



def install_package(request,server_id, pkg_id):
    login = CheckLogin(request)
    if login == True:
        params = {}
        user = getUser(request)
        params['status'] = "error"
        if pkg_id in PACKAGES_DETAILS:
            getserver = server_list.objects.get(id=server_id)
            get_installed_pkg_lst = json.loads(getserver.JSON_PKG_LST)
            

            check = pkg_id in get_installed_pkg_lst

            if check == False:
                InstallServerPackage.delay(server_id, pkg_id)
                params['status'] = "ok"




            

        return JsonResponse(params)





def restart_pkg(request, manage_id, package_id):
    login = CheckLogin(request)
    if login == True:
        params = {}
        try:
            getserver = server_list.objects.get(id=manage_id)
            getpkg = json.loads(getserver.JSON_PKG_LST)

            if package_id in getpkg:
                pk_g = PACKAGES[package_id]
                if pk_g['SERVICE_VIEW'] == True:
                    get_key = ""
                    
                    for key, pkg in PACKAGES.items():
                        control = pkg['CONTROL_PANEL']
                        for key, cntr in control.items():
                            for key_a, cop in cntr.items():
                                if key_a == 'Restart':
                                    get_key = key

                    
                    RestartPackage.delay(package_id, manage_id, get_key)
                    params['status'] = "ok"


        except Exception as e:
            params['status'] = "error"
    
    return JsonResponse(params)


def stop_pkg(request, manage_id, package_id):
    login = CheckLogin(request)
    if login == True:
        params = {}
        try:
            getserver = server_list.objects.get(id=manage_id)
            getpkg = json.loads(getserver.JSON_PKG_LST)

            if package_id in getpkg:
                pk_g = PACKAGES[package_id]
                if pk_g['SERVICE_VIEW'] == True:
                    get_key = ""
                    
                    for key, pkg in PACKAGES.items():
                        control = pkg['CONTROL_PANEL']
                        for key, cntr in control.items():
                            for key_a, cop in cntr.items():
                                if key_a == 'Stop':
                                    get_key = key

                    
                    StopPackage.delay(package_id, manage_id, get_key)
                    params['status'] = "ok"


        except Exception as e:
            params['status'] = "error"
            print(e)
    
    return JsonResponse(params)



def package_manager(request, server_id):
    login = CheckLogin(request)
    if login == True:
        params = {}
        user = getUser(request)
        params['user'] = user
        params['menu'] = {}
        try:
            getserver = server_list.objects.get(id=server_id)
            params['menu'] = rewrite_menu(getserver.JSON_PKG_LST, server_id)
            getinstalled_pkg = Pkg_inst_data.objects.filter(user=user, server=getserver, ViewPKGOption = True)
            params['inst_pkg'] = getinstalled_pkg
            params['server'] = getserver
            json_pkg = json.loads(getserver.JSON_PKG_LST)
            newdic = {}
            for key, pkg in PACKAGES.items():

                if key in json_pkg:
                    pass
                else:
                    newdic[key] = pkg

            
            params['avail'] = newdic
        except Exception as e:
            print(e)
            
        
        return render(request, "user/package-manager.html", params)

    else:
        return redirect("/login")

def manage_server(request, server_id):
    login = CheckLogin(request)
    if login == True:
        params = {}
        user = getUser(request)
        params['user'] = user
        params['menu'] = {}
        try:
            getserver = server_list.objects.get(id=server_id)
            params['menu'] = rewrite_menu(getserver.JSON_PKG_LST, server_id)
            



        except Exception as e:
            print(e)
            
        
        return render(request, "user/server-home.html", params)

    else:
        return redirect("/login")
    

def deploy(request):
    
    login = CheckLogin(request)
    #installStack(27)
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

