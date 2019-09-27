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
from Backend.servers.models import list as server_list, projects, Pkg_inst_data, output as ser_output
import json
# Create your views here.

def virtual_env(request, manage_id):
    login = CheckLogin(request)
    if login == True:
        params = {}
        user = getUser(request)
        params['user'] = user
        try:
            getserver = server_list.objects.get(id=manage_id, user_id=user)
            params['server'] = getserver
            getPKG = json.loads(getserver.JSON_PKG_LST)
            params['menu'] = rewrite_menu(getserver.JSON_PKG_LST, manage_id)

        except Exception as e:
            print(e)

        return render(request, "user/virtual_env.html", params)
    else:
        return redirect("/login")