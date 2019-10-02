from django.shortcuts import render, redirect
from django.http import  JsonResponse
from django.core.signing import Signer
from django.contrib import messages
import paramiko
from django.db.models import Q
from ..BackendController.contri import randomString, randomNumber
from ..signup.models import user
from ..BackendController.tasks.install_stack import installStack, RestartPackage, StopPackage, InstallServerPackage, SetupVirtualENV
from ..BackendController.contri import CheckLogin, getUser, rewrite_menu
from ..BackendController.server_config import STACK_DIST,SERVER_OS_DISTRIBUTION, PACKAGES_DETAILS, PACKAGES, PYTHON_VERSION_DIC
from Backend.servers.models import list as server_list, projects, Pkg_inst_data, output as ser_output
from .models import virtual_env as vir_en, deploy as dj_ep
from Backend.lamp.models import domain, ftp_account
from Backend.servers.models import Pkg_inst_data
import json, tldextract
# Create your views here.

def deploy(request, manage_id):

    login = CheckLogin(request)
    if login == True:
        params = {}
        user = getUser(request)
        params['user'] = user
        try:
            getserver = server_list.objects.get(id=manage_id, user_id=user)
            params['server'] = getserver
            getPKG = json.loads(getserver.JSON_PKG_LST)
            PyPKG = PYTHON_VERSION_DIC
            params['PyPKG'] = PyPKG
            params['envs'] = vir_en.objects.filter( user_id=user, server=getserver)
            params['deploys'] = dj_ep.objects.filter(user_id=user, server=getserver)
            params['menu'] = rewrite_menu(getserver.JSON_PKG_LST, manage_id)

            if request.method == "POST":

                Insert = True
                
                domain_name = request.POST['domain']
                wsgi = request.POST['wsgi']
                static = request.POST['static']
                env = request.POST['env']

                try:
                    ftp = request.POST['ftp']
                    ftp = True
                except:
                    ftp = False


                ver = request.POST['ver']

                ext = tldextract.extract(domain_name)
                    
                folder = "/var/www/" + domain_name

                if domain == '':

                    Insert = False
                    messages.error(request, "Enter a valid domain name without http(s)", extra_tags="danger")
                
                if wsgi == '':

                    Insert = False
                    messages.error(request, "Enter a django wsgi filename", extra_tags="danger")
                
                if static == '':

                    Insert = False
                    messages.error(request, "Enter a django wsgi static dir", extra_tags="danger")
                
                if env == '':

                    Insert = False
                    messages.error(request, "Enter a django virtual environment", extra_tags="danger")
                    
                
                else:
                    
                    chec_ex = dj_ep.objects.filter(Environment=env).count()

                    if chec_ex > 0:
                        Insert = False
                        messages.error(request, "Cannot deploy multiple deploy on same Environment please create new environment", extra_tags="danger")

                
                if ver == '':

                    Insert = False
                    messages.error(request, "Enter a django version", extra_tags="danger")
                


                if Insert == True:

                    print(env)
                    obj, insert = domain.objects.get_or_create(
                        server = getserver,
                        user = user,
                        domain_name = ext.domain + "." + ext.suffix,
                        subdomain = ext.subdomain,
                        folder = folder,
                        status = "Configuring"
                    )

                    if ftp:
                        
                        ck = Pkg_inst_data.objects.filter(PackageId=7, server=getserver, user=user).count()
                        if ck == 1:
                            obj, insert = ftp_account.objects.get_or_create(
                                server = getserver,
                                user = user,
                                username = domain_name,
                                password = randomString(),
                                folder = folder,
                                status = "Configuring",
                            )

                        else:
                            messages.error(request, "FTP account could not be created since vsftpd Package is not installed")

                    obj, insert = dj_ep.objects.get_or_create(
                        server = getserver,
                        user = user,
                        domain = obj,
                        Environment_id = int(env),
                        status = "Configuring",
                        django_ver = ver
                    )

                    if insert:
                        messages.success(request, "A deploy project folder will be create make sure to upload the project on that folder & restart the Apache server on Package Manager Page. ")


        
        except Exception as e:
            print(e)
            messages.success(request, "A deploy project folder will be create make sure to upload the project on that folder & restart the Apache server on Package Manager Page. ")

        return render(request, "user/django_deploy.html", params)
    else:
        return redirect("/login")


def virtual_env_ide(request, manage_id, ide):
    
    login = CheckLogin(request)
    if login == True:
        params = {}
        user = getUser(request)
        params['user'] = user
        try:
            getserver = server_list.objects.get(id=manage_id, user_id=user)
            params['server'] = getserver
            getPKG = json.loads(getserver.JSON_PKG_LST)
            PyPKG = PYTHON_VERSION_DIC
            params['PyPKG'] = PyPKG
            params['envs'] = vir_en.objects.filter( user_id=user, server=getserver)
            
            params['menu'] = rewrite_menu(getserver.JSON_PKG_LST, manage_id)

            
        except Exception as e:
            print(e)

        return render(request, "user/virtual_env_ide.html", params)
    else:
        return redirect("/login")

def virtual_env_view(request, manage_id):
    
    login = CheckLogin(request)
    if login == True:
        params = {}
        user = getUser(request)
        params['user'] = user
        try:
            getserver = server_list.objects.get(id=manage_id, user_id=user)
            params['server'] = getserver
            getPKG = json.loads(getserver.JSON_PKG_LST)
            PyPKG = PYTHON_VERSION_DIC
            params['PyPKG'] = PyPKG
            params['envs'] = vir_en.objects.filter( user_id=user, server=getserver)
            
            params['menu'] = rewrite_menu(getserver.JSON_PKG_LST, manage_id)

            if request.method == "POST":
                env_name=request.POST['env']
                py_v=request.POST['ver']

                if env_name !='' and py_v!='':

                    getv = PYTHON_VERSION_DIC[py_v][getserver.distribution_id]
                    install_dir = "/root/.pyenv/versions/"+ getv[0]  +"/envs/"+ env_name
                    py_inter_full = "/root/.pyenv/versions/"+ getv[0] + "/envs/"+ env_name + getv[4]

                    obj, ins = vir_en.objects.get_or_create(
                        server = getserver,
                        user = user,
                        envirnment_name = env_name,
                        install_dir = install_dir,
                        python_inter_full = py_inter_full,
                        python_inter = py_v,
                        status = "Configuring"
                        
                    )

                    SetupVirtualENV.delay(obj.id)
                    
                    messages.info(request, "Environment will be created soon!")

        except Exception as e:
            print(e)

        return render(request, "user/virtual_env.html", params)
    else:
        return redirect("/login")