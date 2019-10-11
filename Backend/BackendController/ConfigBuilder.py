from django.http import  JsonResponse
from django.core.signing import Signer
from django.contrib import messages
import paramiko
from django.db.models import Q
from .contri import randomString, randomNumber
from ..signup.models import user
from .contri import CheckLogin, getUser, rewrite_menu
from ..loadBalancer.models import config as HAPROXY_CONFIG
from ..servers.models import list as server_list, projects, Pkg_inst_data, output as ser_output
from django.utils.crypto import get_random_string
from querystring_parser import parser
import json
import os
import ntpath

PROJECT_PATH = os.path.abspath(os.path.dirname(__name__))


def HAProxy(insert_id):

    algo = {
        'Round Robin':'roundrobin',
        'Least Connection':'leastconn',
        'Static Round Robin':'static-rr',
    }

    HAPROXY_OUTPUT =  """

global
    log 127.0.0.1 local0 notice
    maxconn 2000
    user haproxy
    group haproxy

defaults
    log     global
    mode    http
    option  httplog
    option  dontlognull
    timeout connect 5000
    timeout client  50000
    timeout server  50000
    errorfile 400 /etc/haproxy/errors/400.http
    errorfile 403 /etc/haproxy/errors/403.http
    errorfile 408 /etc/haproxy/errors/408.http
    errorfile 500 /etc/haproxy/errors/500.http
    errorfile 502 /etc/haproxy/errors/502.http
    errorfile 503 /etc/haproxy/errors/503.http
    errorfile 504 /etc/haproxy/errors/504.http
    
    """

    HAConfig = HAPROXY_CONFIG.objects.get(id = insert_id)
    
    NodeServer = server_list.objects.filter(ServerType = "SLAVE", parent_server = HAConfig.server)
    server = HAConfig.server
    user = HAConfig.user
    
    
    health = """"""
    if HAConfig.monitor == True:
        pwd = str(get_random_string(length=8))
        HAConfig.monitor_user = user.email
        HAConfig.monitor_pass = pwd
        HAConfig.save()
        health = """
        
listen  stats
    mode            http
    log             global
    bind            *:1936
    timeout queue   100s
    bind *:80
    stats enable
    stats hide-version
    stats refresh 30s
    stats show-node
    stats auth """ + user.email + """:""" + pwd  +"""
    stats uri  /loadbalance?stats

        """
    
    main_config = """
        
listen """ + HAConfig.label + """
    mode http
    bind *:80
    balance """ + algo[HAConfig.algorithm] + """
    option httpclose
    http-request set-header X-Forwarded-Port %[dst_port]
    http-request add-header X-Forwarded-Proto https if { ssl_fc }
    option forwardfor"""

    server_str = """"""
    for ser in NodeServer:
        c = """
    server """+ ser.hostname +""" """+ ser.server_ip +""":80 check
    """
        server_str = server_str + c

    header_str = """"""
    for line in HAConfig.header.splitlines():
        
        header_str = header_str + line + """ 
    """



    main_config = HAPROXY_OUTPUT + health + main_config
    main_config += header_str  
    main_config += server_str
    

    file_name = "haproxy"+ str(server.id) +".cfg"
    
    try:
        os.remove(os.path.join(PROJECT_PATH,'Backend','BackendController', 'write_files', file_name))
        
    except:
        pass

        
    f = open(os.path.join(PROJECT_PATH,'Backend','BackendController', 'write_files', file_name),"w+")
    f.write(main_config)
    f.close()

    
    return file_name