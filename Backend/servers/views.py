from django.shortcuts import render, redirect
from django.core.signing import Signer
from django.contrib import messages
from django.db.models import Q
from ..BackendController.contri import randomString, randomNumber
from ..signup.models import user
from ..BackendController.tasks.install_stack import installServer
from ..BackendController.contri import CheckLogin, getUser
from .models import list as server_list


# Create your views here.

def deploy(request):
    login = CheckLogin(request)
    if login == True:
        params = {}
        user = getUser(request)
        params['user'] = user
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
        get_all_servers = server_list.objects.filter(user_id=user)
        params['servers'] = get_all_servers
        
        params['server_count'] = get_all_servers.count()
        print(params)
        return render(request, "user/dashboard.html", params)
    else:
        return redirect("/login")