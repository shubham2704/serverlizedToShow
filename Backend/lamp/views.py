from django.shortcuts import render, redirect
from django.core.signing import Signer
from django.contrib import messages
import paramiko
from django.db.models import Q
from ..BackendController.contri import randomString, randomNumber
from ..signup.models import user
from ..BackendController.tasks.install_stack import ConfigureLampDomain
from ..BackendController.contri import CheckLogin, getUser, rewrite_menu
from ..BackendController.server_config import STACK_DIST,SERVER_OS_DISTRIBUTION, PACKAGES
from ..servers.models import list as server_list, projects
import json
from .models import domain
import tldextract


# Create your views here.
PKG_ID = 1

def add(request, manage_id ):
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

            if request.method == "POST":
                domain_name = request.POST['domain']
                folder = request.POST['folder']
                

                if domain != '' and folder != '':
                    ext = tldextract.extract(domain_name)
                    if ext.domain!='' and ext.suffix!='':

                        obj, insert = domain.objects.get_or_create(
                            server = getserver,
                            user = user,
                            domain_name = ext.domain,
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

def delete(request,manage_id,domain_id ):
    pass