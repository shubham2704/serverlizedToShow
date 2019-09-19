from django.shortcuts import render, redirect
from django.core.signing import Signer
from django.contrib import messages
import paramiko
from django.db.models import Q
from ..BackendController.contri import randomString, randomNumber
from ..signup.models import user
from ..BackendController.tasks.install_stack import ConfigureLampDomain, DeleteLampDomain, MySQLUserAdd, MySQLUserDelete, MySQLDatabaseCreate, MySQLDatabaseDelete, ConfigLetsEncrypt
from ..BackendController.contri import CheckLogin, getUser, rewrite_menu
from ..BackendController.server_config import STACK_DIST,SERVER_OS_DISTRIBUTION, PACKAGES
from ..servers.models import list as server_list, projects
import json
from .models import domain, mysql_user, mysql_database, ssl as tcp_ssl, lets_encrypt
import tldextract


# Create your views here.
PKG_ID = 1

def letsencrypt(request, manage_id):
    login = CheckLogin(request)
    print(login)
    if login == True:
        params = {}
        user = getUser(request)
        params['user'] = user
        params['menu'] = {}

        try:
            getserver = server_list.objects.get(id=manage_id)
            params['server'] = getserver
            params['ssls'] = lets_encrypt.objects.filter(server=getserver, user=user)
            params['domains'] = domain.objects.filter(server=getserver, user=user)
            params['menu'] = rewrite_menu(getserver.JSON_PKG_LST, manage_id)
            if request.method == "POST":
                domain_id = request.POST['domain_id']
                domain_got = domain.objects.get(id = domain_id)
                count_l = lets_encrypt.objects.filter(domain = domain_got).count()
                count_d = tcp_ssl.objects.filter(domain = domain_got).count()
                
                if count_l == 0 and count_d == 0:

                    obj, insert = lets_encrypt.objects.get_or_create(
                        server = getserver,
                        user = user,
                        domain = domain_got,
                        status = "Installing"
                    )

                    if insert:
                        ConfigLetsEncrypt.delay(obj.id)
                        messages.success(request, "Let's Encrypt will be installed soon.")

                else:
                    messages.error(request, "It seem you have already a SSL for selected domain.", extra_tags="danger")
            
        except Exception as e:
            print(e)
            

        
        return render(request, "user/ssl-letsencrypt.html", params)

    else:
        return redirect("/login")


def ssl(request, manage_id):
    login = CheckLogin(request)
    
    print(login)
    if login == True:
        params = {}
        user = getUser(request)
        params['user'] = user
        params['menu'] = {}

        try:
            getserver = server_list.objects.get(id=manage_id)
            params['server'] = getserver
            params['ssls'] = tcp_ssl.objects.filter(server=getserver, user=user)
            params['domains'] = tcp_ssl.objects.filter(server=getserver, user=user)
            params['menu'] = rewrite_menu(getserver.JSON_PKG_LST, manage_id)
            

        
       
        except Exception as e:
            pass


        return render(request, "user/ssl.html", params)

    else:
        return redirect("/login")


def apachelog(request, manage_id):
    login = CheckLogin(request)
    
    print(login)
    if login == True:
        params = {}
        user = getUser(request)
        params['user'] = user
        params['menu'] = {}

        try:
            getserver = server_list.objects.get(id=manage_id)
            params['server'] = getserver
            params['dbs'] = mysql_database.objects.filter(server=getserver, user=user)
            params['users'] = mysql_user.objects.filter(server=getserver, user=user)
            
            getPKG = json.loads(getserver.JSON_PKG_LST)
            params['menu'] = rewrite_menu(getserver.JSON_PKG_LST, manage_id)

            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.load_system_host_keys()
            client.connect(getserver.server_ip, username=getserver.superuser, password=getserver.password)

            get_LogCommand = PACKAGES[1]['CONTROL_PANEL']['WEBSITE']['Apache Logs']['COMMAND'][getserver.distribution_id]
            if get_LogCommand[0] == "COMMAND":
                cmd = get_LogCommand[1]
                
                stdidn,stddout,stdderr=client.exec_command(cmd)
                #print(stddout.readlines())
                

            
                
            
                params['abs'] = stddout.readlines()
       
        except Exception as e:
            pass


        return render(request, "user/apache-log.html", params)

    else:
        return redirect("/login")


def mysql_db_delete(request, manage_id, muser_id):
    login = CheckLogin(request)
    
    print(login)
    if login == True:
        params = {}
        user = getUser(request)
        params['user'] = user
        params['menu'] = {}
        try:
            getserver = server_list.objects.get(id=manage_id)
            params['server'] = getserver
            params['dbs'] = mysql_database.objects.filter(server=getserver, user=user)
            params['users'] = mysql_user.objects.filter(server=getserver, user=user)
            
            getPKG = json.loads(getserver.JSON_PKG_LST)
            params['menu'] = rewrite_menu(getserver.JSON_PKG_LST, manage_id)
            if 2 in getPKG == False:
                return redirect("/wpanel/")
            else:
                getDB = mysql_database.objects.get(id=muser_id)
                MySQLDatabaseDelete.delay(getDB.id)
                messages.success(request, "We have got your request, MySQL Database will be deleted.")

              

       
        except Exception as e:
            return redirect("/wpanel/"+ str(getserver.id) + "/mysql/create/database" )

        return render(request, "user/mysql-database.html", params)

    else:
        return redirect("/login")



def mysql_database_add(request, manage_id):
    login = CheckLogin(request)
    
    print(login)
    if login == True:
        params = {}
        user = getUser(request)
        params['user'] = user
        params['menu'] = {}
        try:
            getserver = server_list.objects.get(id=manage_id)
            params['server'] = getserver
            params['dbs'] = mysql_database.objects.filter(server=getserver, user=user)
            params['users'] = mysql_user.objects.filter(server=getserver, user=user)
            
            getPKG = json.loads(getserver.JSON_PKG_LST)
            params['menu'] = rewrite_menu(getserver.JSON_PKG_LST, manage_id)
            if 2 in getPKG == False:
                return redirect("/wpanel/")
            else:
                if request.method == "POST":  
                    db_user = request.POST['user']
                    db_name = request.POST['name']
                    
                    if db_user != '' and db_name != '':
                        db_user = mysql_user.objects.get(id = db_user)
                        obj, insert = mysql_database.objects.get_or_create(
                            server = getserver,
                            user = user,
                            database_name = db_name,
                            mysql_user = db_user,
                        )

                        if insert:
                            #MySQLUserAdd.delay(obj.id)
                            messages.success(request, "We have got your request, MySQL Database will be created.")
                            MySQLDatabaseCreate.delay(obj.id)
                
                    else:
                        messages.warning(request, "All fields are mandatory")


       
        except Exception as e:
            print(e, "Exc")

        return render(request, "user/mysql-database.html", params)

    else:
        return redirect("/login")




def mysql_user_delete(request, manage_id, muser_id):
    login = CheckLogin(request)
    #ConfigureLampDomain.delay(9)
    print(login)
    if login == True:
        params = {}
        user = getUser(request)
        params['user'] = user
        params['menu'] = {}
        try:
            getserver = server_list.objects.get(id=manage_id)
            params['server'] = getserver
            params['users'] = mysql_user.objects.filter(server=getserver, user=user)
            getPKG = json.loads(getserver.JSON_PKG_LST)
            params['menu'] = rewrite_menu(getserver.JSON_PKG_LST, manage_id)
            if 2 in getPKG == False:
                return redirect("/wpanel/")
            else:
                get_mysql_user = mysql_user.objects.get(id = muser_id)
                MySQLUserDelete.delay(get_mysql_user.id)
                messages.success(request, "We have got your request, MySQL user will be deleted.")
                


       
        except Exception as e:
            print(e, "Exc")

        print(params)
        return render(request, "user/mysql-user.html", params)

    else:
        return redirect("/login")




def mysql_user_add(request, manage_id):
    login = CheckLogin(request)
    #ConfigureLampDomain.delay(9)
    print(login)
    if login == True:
        params = {}
        user = getUser(request)
        params['user'] = user
        params['menu'] = {}
        try:
            getserver = server_list.objects.get(id=manage_id)
            params['server'] = getserver
            params['users'] = mysql_user.objects.filter(server=getserver, user=user)
            getPKG = json.loads(getserver.JSON_PKG_LST)
            params['menu'] = rewrite_menu(getserver.JSON_PKG_LST, manage_id)
            if 2 in getPKG == False:
                return redirect("/wpanel/")
            else:
                if request.method == "POST":
                    print(request.POST)    
                    username = request.POST['user']
                    password = request.POST['password']
                    remote = False
                    if "remote" in request.POST:
                        remote = True

                    if username != '' and password != '':
                        obj, insert = mysql_user.objects.get_or_create(
                            server = getserver,
                            user = user,
                            name = username,
                            remote = remote,
                            password = password,
                            permissions = "",
                            status = "Configuring"
                        )

                        if insert:
                            MySQLUserAdd.delay(obj.id)
                            messages.success(request, "We have got your request, MySQL user will be created.")


                    else:
                        messages.warning(request, "All fields are required.")    

       
        except Exception as e:
            print(e, "Exc")

        print(params)
        return render(request, "user/mysql-user.html", params)

    else:
        return redirect("/login")



def phpmyadmin(request, manage_id):
    login = CheckLogin(request)
    #ConfigureLampDomain.delay(9)
    print(login)
    if login == True:
        params = {}
        user = getUser(request)
        params['user'] = user
        params['menu'] = {}
        
        try:
            getserver = server_list.objects.get(id=manage_id)
            getPKG = json.loads(getserver.JSON_PKG_LST)
            
            params['server'] = getserver

            if 4 in getPKG == False:
                return redirect("/wpanel/")
 
            return redirect("http://"+getserver.server_ip + "/phpmyadmin")

                    
        except Exception as e:
            print(e, "Exc")
            
        print(params)
        return render(request, "user/domain-add.html", params)

    else:
        return redirect("/login")


def delete(request, manage_id,domain_id):
    login = CheckLogin(request)
    #ConfigureLampDomain.delay(9)
    print(login)
    if login == True:
        params = {}
        user = getUser(request)
        params['user'] = user
        params['menu'] = {}
        try:
            getserver = server_list.objects.get(id=manage_id)
            getPKG = json.loads(getserver.JSON_PKG_LST)
            params['menu'] = rewrite_menu(getserver.JSON_PKG_LST, manage_id)
            if PKG_ID in getPKG == False:
                return redirect("/wpanel/")
 
            params['server'] = getserver
            getdomains = domain.objects.filter(server=getserver, user=user)
            domain_got = domain.objects.get(user=user, id = domain_id)
            params['domains'] = getdomains
            params['menu'] = rewrite_menu(getserver.JSON_PKG_LST, manage_id)
            DeleteLampDomain.delay(domain_got.id)
            messages.success(request, "We have got your request, your domain will be deleted soon.")    
                    
        except Exception as e:
            print(e, "Exc")
            
        print(params)
        return render(request, "user/domain-add.html", params)

    else:
        return redirect("/login")

def add(request, manage_id ):
    login = CheckLogin(request)
    #ConfigureLampDomain.delay(9)
    
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

            getdomains = domain.objects.filter(server=getserver, user=user)
            params['domains'] = getdomains

            params['menu'] = rewrite_menu(getserver.JSON_PKG_LST, manage_id)

            if request.method == "POST":
                domain_name = request.POST['domain']
                folder = request.POST['folder']
                

                if domain != '' and folder != '':
                    ext = tldextract.extract(domain_name)
                    if ext.domain!='' and ext.suffix!='':

                        obj, insert = domain.objects.get_or_create(
                            server = getserver,
                            user = user,
                            domain_name = ext.domain + "." + ext.suffix,
                            subdomain = ext.subdomain,
                            folder = folder,
                            status = "Configuring"
                        )

                        if insert:
                            ConfigureLampDomain.delay(obj.id)
                            messages.success(request, "We have got your request, your domain will be added soon.")    

                        


                    else:
                        messages.warning(request, "Enter a valid domain name.")    


                else:
                    messages.warning(request, "All fields are mandatory")

                    
        except Exception as e:
            print(e, "Exc")
            
        
        return render(request, "user/domain-add.html", params)

    else:
        return redirect("/login")



def edit(request,manage_id,domain_id ):
    pass

