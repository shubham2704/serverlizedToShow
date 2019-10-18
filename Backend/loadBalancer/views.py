from django.shortcuts import render, redirect
from django.http import  JsonResponse
from django.core.signing import Signer
from django.contrib import messages
import paramiko
from django.utils.crypto import get_random_string
from django.db.models import Q
from ..BackendController.contri import randomString, randomNumber
from ..signup.models import user
from ..BackendController.tasks.install_stack import CreateFTPAccount, ConfigureLampDomain, installStack, RestartPackage, StopPackage, InstallServerPackage, ConfigHAProxyWeb, ConfigHAProxyDomain,ReplicateHAProxyFiles
from ..BackendController.contri import CheckLogin, getUser, rewrite_menu
from ..BackendController.server_config import STACK_DIST,SERVER_OS_DISTRIBUTION, PACKAGES_DETAILS, PACKAGES
from Backend.servers.models import list as server_list, projects, Pkg_inst_data, output as ser_output
from Backend.BackendController.ConfigBuilder import HAProxy as ConfigBuilder_HAProxy
from .models import config as HAProxy_Config, domains as HAProxy_Domains, replicate_file
from ..lamp.models import domain, ftp_account
from querystring_parser import parser
from datetime import datetime
import json, sys, traceback, tldextract, os,zipfile 
from django.core.files.storage import FileSystemStorage

PKG_ID = 1
PROJECT_PATH = os.path.abspath(os.path.dirname(__name__))

def ftp(request, manage_id):
    
    
    login = CheckLogin(request)
    #ConfigHAProxyDomain(5)
    
    if login == True:
        
        params = {}
        user = getUser(request)
        params['user'] = user
        params['menu'] = {}
        try:
            getserver = server_list.objects.get(id=manage_id)
            domains = HAProxy_Domains.objects.filter(server=getserver, user=user)
            print(domains)
            params['domains'] = domains
            getPKG = json.loads(getserver.JSON_PKG_LST)
            
            if PKG_ID in getPKG == False:
                return redirect("/wpanel/")


            if request.method == "POST":

                
                try:
                    

                    uploaded_file = request.FILES['file']
                    upload_dir = request.POST['FOLDER']
                    did = request.POST['did']
                    print(request.POST)
                    if upload_dir!='' and did!='':
                        fs = FileSystemStorage()
                        ext = os.path.splitext(uploaded_file.name)[1]
                        if ext == '.zip' or ext=='.png':
                            filename_uploaded = str(user.id) + user.first_name.lower() + str(datetime.now().strftime("%H-%M-%S"))+ext
                            print(filename_uploaded)
                            upload = fs.save(filename_uploaded, uploaded_file)
                            upload_path = fs.url(upload)
                            if upload:
                                zf = zipfile.ZipFile(os.path.join(PROJECT_PATH,'templates','media', filename_uploaded))
                                try:
                                    zf.testzip()
                                    print("uploaded")
                                    dom = HAProxy_Domains.objects.get(id = did)
                                    obj, insert = replicate_file.objects.get_or_create(
                                        server = getserver,
                                        user = user,
                                        connected_domain = dom,
                                        file_name = filename_uploaded,
                                        folder = upload_dir,
                                        status = 'Transferring',

                                    )


                                    if insert:

                                        deco = json.loads(dom.domain_insert_withftp_dict)
                                        inse_dic = {}
                                        for key, send_async_request in json_ld.items():
                                            inse_dic[key] = {
                                                    'domain': send_async_request['domain'],
                                                    'ftp' :send_async_request['ftp'],
                                                    'file_replication_status' : "Not Done",
                                                    'server' : send_async_request['server']
                                                }

                                        dom.domain_insert_withftp_dict = json.dumps(inse_dic)
                                        dom.save()
                                        
                                        ReplicateHAProxyFiles.delay(obj.id)
                                        messages.success(request, "File succfully upooad on Serverlized you file will uploaded soon on  all node server.")
                                except RuntimeError as e:
                                    if 'encrypted' in str(e):
                                        print ('Golly, this zip has encrypted files! Try again with a password!')
                                        messages.warning(request, "Zip files seems password proteted please upload a unprotected Zip File")
                                    else:
                                        # RuntimeError for other reasons....
                                        print(e)
                                       

                        else:
                            messages.warning(request, "Only Zip file is allowed")
                    else:
                            messages.warning(request, "Enter path where should file be uploaded and unzipped")
                except Exception as e:
                    print(e)
                    messages.warning(request, "Please select a valid Zip file")


            params['server'] = getserver
            params['menu'] = rewrite_menu(getserver.JSON_PKG_LST, manage_id)

                    
        except Exception as e:
            print(e, "Exc")
            traceback.print_exc(limit=1, file=sys.stdout)
            
        
        return render(request, "user/haproxy_ftp.html", params)

    else:
        return redirect("/login")



def configure(request, manage_id):
    login = CheckLogin(request)
    if login == True:
        params = {}
        user = getUser(request)
        params['user'] = user
        params['menu'] = {}
        
        

        try:
            
            getserver = server_list.objects.get(id=manage_id)
            params['server'] = getserver
            params['menu'] = rewrite_menu(getserver.JSON_PKG_LST, manage_id)
            getConfig = HAProxy_Config.objects.filter(user=user, server=getserver)
            print(getConfig.count())
            if getConfig.count() > 0:
                params['config_ha'] = getConfig[0]
                params['already'] = True
                
                mainconfig = HAProxy_Config.objects.get(id = getConfig[0].id)
                print(mainconfig.header)
         
                if request.method == "POST":
                    algo = request.POST['algo']
                    header = request.POST['header']

                    health = request.POST.get("health", False)
                    if health == 'yes':
                        health = True
                    else:
                        health = False
                        
                    if health == True:
                        mainconfig.monitor_user = None
                        mainconfig.monitor_pass = None



                    mainconfig.monitor = health
                    mainconfig.algorithm = algo

                    if header!='':
                        mainconfig.header = header
                    
                    mainconfig.save()

                    messages.success(request, "HAProxy will be reconfigured soon!")
                    ConfigHAProxyWeb.delay(getConfig[0].id)


            else:
                if request.method == "POST":
                    node = {}
                    
                    if 'server[0]' in request.POST:

                        nodes = parser.parse(request.POST.urlencode())['server']

                        print(nodes)

                        
                        
                        if len(nodes) != 0:
                            
                            pass_server = True
                            
                            for node in nodes:
                                pass
                            
                            if pass_server == False:
                                messages.error(request, "Make sure all node server are communicable or check you login. ", extra_tags="danger")
                            else:
                                label = request.POST['label']
                                algo = request.POST['algo']
                                software = request.POST['software']
                                
                                header = request.POST['header']
                                
                                health = request.POST.get("health", False)
                                if health == 'yes':
                                    health = True
                                else:
                                    health = False    

                                

                                if label!='' and algo!='' and software!='':
                                    
                                    obj, insert = HAProxy_Config.objects.get_or_create(
                                        server = getserver,
                                        user = user,
                                        label = label,
                                        monitor = health,
                                        algorithm = algo,
                                        status = 'Configuring',
                                        header = header,
                                        
                                    )
                                    
                                    print(obj)
                                    

                                    if insert:
                                        
                                        for key, node in nodes.items():
                                        
                                            ob, ins = server_list.objects.get_or_create(
                                                server_name =  "Node Server " + str(key) +" "+ label,
                                                user_id = user,
                                                distribution_id = getserver.distribution_id,
                                                stack_id = getserver.stack_id,
                                                superuser = "root",
                                                ServerType = "SLAVE",
                                                server_status = "Installing",
                                                server_ip = node[1],
                                                project_id = getserver.project_id,
                                                JSON_PKG_LST = "[1, 3, 7]",
                                                Charges = 0.00,
                                                running_status = "Running",
                                                password = node[2],
                                                hostname = node[0],
                                                stack_name="Loadbalancer Node Server #" + str(key)  +" of " + str(getserver.server_name),
                                                parent_server = getserver
                                            )

                                            installStack.delay(ob.id)
                                    
                                        

                                    if insert:
                                        ConfigHAProxyWeb.delay(obj.id)
                                        messages.success(request, "HAProxy will be configured soon!")

                                else:
                                    messages.error(request, "Fields are mandatory marked * ", extra_tags="danger")
                        else:
                            messages.error(request, "Enter at least one node server.", extra_tags="danger")
                    else:
                        messages.error(request, "Enter d at least one node server.", extra_tags="danger")

        except Exception as e:
            
            traceback.print_exc(limit=1, file=sys.stdout)
            print(e)
            
            
        
        return render(request, "user/haproxy_http.html", params)

    else:
        return redirect("/login")
    

    


def NodeServer(request, manage_id):
    login = CheckLogin(request)
    if login == True:
        params = {}
        user = getUser(request)
        params['user'] = user
        params['menu'] = {}
        
        

        try:
            
            getserver = server_list.objects.get(id=manage_id)
            params['server'] = getserver
            params['menu'] = rewrite_menu(getserver.JSON_PKG_LST, manage_id)
            getservers = server_list.objects.filter(parent_server=getserver)
            params['nodes'] = getservers

            if request.method == "POST":
                    node = {}
                    
                    if 'server[0]' in request.POST:

                        nodes = parser.parse(request.POST.urlencode())['server']

                        print(nodes)
                        if len(nodes) != 0:
                            
                            pass_server = True
                            
                            for node in nodes:
                                pass
                            
                            if pass_server == False:
                                messages.error(request, "Make sure all node server are communicable or check you login. ", extra_tags="danger")
                            else:

                                rep_domain = 'yes'
                                rep_backup = request.POST['rep_backup']
                                print(request.POST)
                                
                                if rep_backup=='exist_file':
                                    
                                    for key, node in nodes.items():
                                        ob, ins = server_list.objects.get_or_create(
                                            server_name =  "Node Server " + str(key),
                                            user_id = user,
                                            distribution_id = getserver.distribution_id,
                                            stack_id = getserver.stack_id,
                                            superuser = "root",
                                            ServerType = "SLAVE",
                                            server_status = "Installing",
                                            server_ip = node[1],
                                            project_id = getserver.project_id,
                                            JSON_PKG_LST = "[1, 3, 7, 12]",
                                            Charges = 0.00,
                                            running_status = "Running",
                                            password = node[2],
                                            hostname = node[0],
                                            stack_name="Loadbalancer Node Server #" + str(key)  +" of " + str(getserver.server_name),
                                            parent_server = getserver
                                        )
                                        
                                        installStack.delay(ob.id)
                                        get_dom = HAProxy_Domains.objects.filter(server=getserver, user=user)
                                        
                                        
                                        
                                        for dm in get_dom:

                                            
                                            
                                            dic_new = json.loads(dm.domain_insert_withftp_dict)
                                            dic_new_len = len(dic_new)
    
                                            objdomain, insert_domain = domain.objects.get_or_create(
                                            server = ob,
                                            user = user,
                                            domain_name = dm.domain_name,
                                            subdomain = dm.subdomain,
                                            folder = dm.folder,
                                            status = "Configuring"
                                            )

                                            ConfigureLampDomain.delay(objdomain.id)

                                            password = str(get_random_string(length=8))

                                            objftp, insert_ftp = ftp_account.objects.get_or_create(
                                            server = ob,
                                            user = user,
                                            username = dm.domain_name,
                                            password = password,
                                            folder = dm.folder,
                                            status = "Configuring"
                                            
                                            )

                                            CreateFTPAccount.delay(objftp.id)


                                            dic_new_len += 1 

                                            dic_new[dic_new_len] = {
                                                'domain': objdomain.id,
                                                'ftp' : objftp.id,
                                                'file_replication_status' : "Not Done",
                                                'server' : ob.id
                                            }


                                            print(dic_new)
                                            dm.domain_insert_withftp_dict = json.dumps(dic_new)
                                            #dm.save()
                                            rep_file = replicate_file.objects.filter(server=getserver, user=user)
                                            for rep in rep_file:
                                                ReplicateHAProxyFiles.delay(rep.id)

                                    messages.success(request, str(len(nodes)) +" server(s) will be added and configured then, "+ str(get_dom.count()) +" domain(s) & "+ str(rep_file.count()) +" files will be replicated!", extra_tags="success")
                                        

                                else:
                                    messages.error(request, "Fields are mandatory marked * ", extra_tags="danger")
                        else:
                            messages.error(request, "Enter at least one node server.", extra_tags="danger")
                    else:
                        messages.error(request, "Enter d at least one node server.", extra_tags="danger")
            
            
        except Exception as e:
            
            traceback.print_exc(limit=1, file=sys.stdout)
            print(e)
            
            
        
        return render(request, "user/haproxy_node_web.html", params)

    else:
        return redirect("/login")
    

    



def domains(request, manage_id):
    
    login = CheckLogin(request)
    #ConfigHAProxyDomain(5)
    
    if login == True:
        params = {}
        user = getUser(request)
        params['user'] = user
        params['menu'] = {}
        try:
            getserver = server_list.objects.get(id=manage_id)
            getPKG = json.loads(getserver.JSON_PKG_LST)
            if PKG_ID in getPKG == False:
                return redirect("/wpanel/")


            params['server'] = getserver

            getdomains = HAProxy_Domains.objects.filter(server=getserver, user=user)
            params['domains'] = getdomains

            params['menu'] = rewrite_menu(getserver.JSON_PKG_LST, manage_id)
            NodeServer = server_list.objects.filter(ServerType = "SLAVE", parent_server = getserver)

            if request.method == "POST":
                domain_name = request.POST['domain']
                folder = request.POST['folder']
                

                if domain_name != '' and folder != '':
                    ext = tldextract.extract(domain_name)
                    if ext.domain!='' and ext.suffix!='':

                        i = 0
                        inse_dic = {}
                        for ser in NodeServer:
                            
                            objdomain, insert_domain = domain.objects.get_or_create(
                            server = ser,
                            user = user,
                            domain_name = ext.domain + "." + ext.suffix,
                            subdomain = ext.subdomain,
                            folder = folder,
                            status = "Configuring"
                            )

                            password = str(get_random_string(length=8))

                            objftp, insert_ftp = ftp_account.objects.get_or_create(
                            server = ser,
                            user = user,
                            username = ext.domain,
                            password = password,
                            folder = folder,
                            status = "Configuring"
                            
                            )

                            inse_dic[i] = {
                                'domain': objdomain.id,
                                'ftp' : objftp.id,
                                'file_replication_status' : "Not Done",
                                'server' : ser.id
                            }


                            get_rep_files = replicate_file.objects.filter(server=getserver, user=user)
                            for rep in get_rep_files:
                                ReplicateHAProxyFiles.delay(rep.id)








                        obj, insert = HAProxy_Domains.objects.get_or_create(
                            server = getserver,
                            user = user,
                            domain_name = ext.domain + "." + ext.suffix,
                            subdomain = ext.subdomain,
                            folder = folder,
                            domain_insert_withftp_dict = json.dumps(inse_dic),
                            status = "Configuring"
                        )

                        print(obj)

                        if insert:

                            ConfigHAProxyDomain.delay(obj.id)
                            
                            messages.success(request, "We have got your request, your domain will be added soon.")    

                    else:
                        messages.warning(request, "Enter a valid domain name.")    


                else:
                    messages.warning(request, "All fields are mandatory")

                    
        except Exception as e:
            print(e, "Exc")
            traceback.print_exc(limit=1, file=sys.stdout)
            
        
        return render(request, "user/haproxy_domain.html", params)

    else:
        return redirect("/login")