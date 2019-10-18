from django.shortcuts import render, redirect
from django.http import  JsonResponse, HttpResponse
from django.core.signing import Signer
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import paramiko
from instamojo_wrapper import Instamojo
from django.db.models import Q
from ..BackendController.contri import randomString, randomNumber, verfiy_email
from ..signup.models import user, transation
from ..BackendController.tasks.install_stack import installStack, RestartPackage, StopPackage, InstallServerPackage
from ..BackendController.contri import CheckLogin, getUser, rewrite_menu, logout
from ..BackendController.server_config import STACK_DIST,SERVER_OS_DISTRIBUTION, PACKAGES_DETAILS, PACKAGES
from .models import list as server_list, projects, Pkg_inst_data, output as ser_output, server_stats, notifications, billing
import json, traceback
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def payment_status(request):

    login = CheckLogin(request)
    if login == True:
        params = {}
        params['status'] = False
        user = getUser(request)
        params['user'] = user
        if request.method == "GET":
            try:
                
                payment_id = request.GET['payment_request_id']
                payment_status = request.GET['payment_status']
                if payment_status == "Credit":
                    get_payment = transation.objects.get(transation_id=payment_id, status=False)
                    get_payment.status = True
                    get_payment.save()
                    params['amount'] = get_payment.amount
                    
                    get_payment.user.money = get_payment.user.money + get_payment.amount
                    get_payment.user.save()
                    params['status'] = True
                else:
                    params['status'] = True
            except:
                params['status'] = False
    else:
        return redirect("/login")

    return render(request, "user/payment.html", params)


def verify_account(request, email_hash):
    
    params = False
    try:
        checkhash =  user.objects.get(email_hash = email_hash, email_verify = False)
        checkhash.email_verify = True
        checkhash.save()
        params = True

    except:
        params = False    

    return render(request, "user/verifyaccount.html", { "data" : params})

    



def verify_email(request):
    login = CheckLogin(request)
    if login == True:
        params = {}
        user = getUser(request)
        params['status'] = "ok"
        try :
            verfiy_email(user.email)


        except Exception as e:
            print(e)
            traceback.print_exc()
            
            params['status'] = "Error"

    return JsonResponse(params)

def projects_view(request):
    

    login = CheckLogin(request)
    if login == True:
        params = {}
        user = getUser(request)
        params['user'] = user
        get_project = projects.objects.filter(user_id=user)
        params['payments'] = transation.objects.filter(user=user)[:5]
        
        if request.method=="POST":
            if 'deposit' in request.POST:
                amount = request.POST['amount']
                if int(amount) >= 100:

                    api = Instamojo(api_key="26557ce6c525d1c0c1eb3c5973fa1a2e",
                auth_token="0c0e7a123bf679f79af2ed61c81ec374")
                    
                    create_pay = api.payment_request_create(
                    amount=amount,
                    purpose='Crediting your Serverlized Account',
                    send_email=True,
                    email=user.email,
                    buyer_name = user.first_name + " " + user.last_name,
                    phone= user.phone_no,
                    redirect_url="https://www.serverlized.com/wpanel/paymentstatus"
                    )
                    print(create_pay)
                   
                    if create_pay['success'] == True:
                        insert = transation.objects.create(user = user, transation_id = create_pay['payment_request']['id'], amount = float(create_pay['payment_request']['amount']))
                        if insert:
                            
                            return redirect(create_pay['payment_request']['longurl'])

                        


                else:
                    messages.warning(request, "Amount should be greater or equal to Rs. 100")

            if 'project' in request.POST:
                name = request.POST['pr_name']
                pr_des = request.POST['pr_des']
                if name!='':
                    insert = projects.objects.create(
                        user_id = user,
                        project_name = name,
                        project_description = pr_des
                    )

                    if insert:
                        messages.success(request, "New project succesfully added!")

                else:
                    messages.warning(request, "Project name can not be empty.")


            if 'password' in request.POST:
                
                old = request.POST['old']
                new = request.POST['new']
                if old!='' and new!='':
                    sig = Signer()
                    em = sig.unsign(user.password)
                    if em == old:
                        update = sig.sign(new)
                        user.password = update
                        user.save()

                        messages.success(request, "Your password is sucesfully changem, you have logged out!")
                        logout(request)


                    else:
                        messages.warning(request, "Wrong old password")



                else:
                    messages.warning(request, "Enter old and new password")


            if 'account' in request.POST:
                insert = True
                last_name = request.POST['last_name']
                first_name = request.POST['first_name']
                phone_no = request.POST['phone']

                if last_name=='' or len(last_name) == 0:
                    insert = False
                    messages.warning(request, "Enter a valid last name")

                if first_name=='' or len(first_name) == 0:
                    insert = False
                    messages.warning(request, "Enter a valid first name")

                if len(phone_no) != 10:
                    insert = False
                    messages.warning(request, "Enter a valid 10 digit phone number")


                if insert == True:
                    user.first_name = first_name
                    user.last_name = last_name
                    user.phone_no = phone_no
                    user.save()
                    messages.success(request, "Account updated")


        params['projects'] = {}
        i = 0
        for project in get_project:

            params['projects'][i]={
                'name':project.project_name,
                'id':i,
                'des':project.project_description,
                'server_count' : server_list.objects.filter(project_id = project).count()
            }

            i =i + 1


        return render(request, "user/projects.html", params)
    else:
        return redirect("/login")

def delserver(request, server_id):
    login = CheckLogin(request)
    if login == True:
        params = {}
        user = getUser(request)
        params['user'] = user
        try:

            dis = {'status' : "ok"}
            getserver_server = server_list.objects.get(id=server_id).delete()
            getserver_node = server_list.objects.filter(parent_server=server_id).delete()

        except Exception as e:
            print(e)
            dis = {'status' : "Error"}

        return JsonResponse(dis)
    else:
        return redirect("/login")


def notification(request, ty):
    login = CheckLogin(request)
    if login == True:
        params = {}
        user = getUser(request)
        params['user'] = user
        try:
            dis = {'notifications':{}}
            getnot = notifications.objects.filter(user=user, seen=False)
            i = 0
            dis['count'] = getnot.count()
            if ty == "b":
                getnot = notifications.objects.filter(user=user)
                for notify in getnot:
                    dis['notifications'][i] = {
                        'color':notify.color,
                        'icon':notify.icon,
                        'seen':notify.seen,
                        'msg':notify.message,
                        'time':notify.date,
                    }

                    i = i + 1
                    notify.seen = True
                    notify.save()
            
           
        except Exception as e:
            print(e)

        return JsonResponse(dis)
    else:
        return redirect("/login")

@csrf_exempt
def server_api(request, server_id):
    #print(request.POST)
    
    ram_data = {
        'memory_total': request.POST['memory_total'],
        'memory_used': request.POST['memory_used'],
        'memory_used_percent': request.POST['memory_used_percent'],
     }
    
    storage = {
        'storage_total': request.POST['storage_total'],
        'storage_used': request.POST['storage_used'],
     }

     

    cpu_data = request.POST['cpu_usage']

    insert = server_stats.objects.create(
        server_id = server_id, 
        json_data = json.dumps(request.POST),
        ram_data = json.dumps(ram_data),
        cpu_data = cpu_data,
        storage_data = json.dumps(storage), 
    )

    cpu_js = []

    get_set = server_stats.objects.filter(server=server_id).order_by('-id')[:25][::-1]
    i = 0
    for dat in get_set:
        cpu_js.append([i, dat.cpu_data])
        i = i+1
    
    print(cpu_js)

    layer = get_channel_layer()
    async_to_sync(layer.group_send)(str(server_id), {
        'data': request.POST,
        'cpu_data' : cpu_js,
        'type': 'events.alarm',
    })


    return HttpResponse(request, "")


def terminal(request, server_id):
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
           
        except Exception as e:
            print(e)

        return render(request, "user/terminal.html", params)
    else:
        return redirect("/login")


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
            server_output = ser_output.objects.filter(server=server_id)[:5]
            params['menu'] = rewrite_menu(getserver.JSON_PKG_LST, server_id)
            params['server'] = getserver
            params['server_output'] = server_output
            getinstalled_pkg = Pkg_inst_data.objects.filter(user=user, server=getserver, ViewPKGOption = True)
            params['inst_pkg'] = getinstalled_pkg
            params['server'] = getserver
            json_pkg = json.loads(getserver.JSON_PKG_LST)

            cpu_js = []

            get_set = server_stats.objects.filter(server=server_id).order_by('-id')[:25][::-1]
            i = 0
            for dat in get_set:
                cpu_js.append([i, float(dat.cpu_data)])
                i = i+1
            
            print(cpu_js)

            params['cpu'] = cpu_js
            newdic = {}
            for key, pkg in PACKAGES.items():

                if key in json_pkg:
                    pass
                else:
                    newdic[key] = pkg

            
            params['avail'] = newdic
            



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
        print(request.POST)

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
                                billing.objects.create(
                                    user = user,
                                    server = obj,
                                    message = "Stack Billing Server " + str(obj.id),
                                    status = True,
                                    monthly_amount = STACK_DIST[int(stack)]['PRICE']
                                    
                                )

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
    #verfiy_email('rs188282@gmail.com');
    if login == True:
        params = {}
        user = getUser(request)
        params['user'] = user
        
        get_all_servers = server_list.objects.filter(user_id=user, ServerType="MASTER",parent_server=None)
        params['servers'] = get_all_servers
        print("ds")
        
        
        params['server_count'] = get_all_servers.count()
        print(params)
        return render(request, "user/dashboard.html", params)
    else:
        return redirect("/login")

