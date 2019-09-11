from django.core.signing import Signer
from ..signup.models import user as usr
import random
import string
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .server_config import STACK_DIST,SERVER_OS_DISTRIBUTION, PACKAGES
import json


def rewrite_menu(menu_fir, server_id):
    d = {}
    for package in json.loads(menu_fir):
                control_panel = PACKAGES[package]['CONTROL_PANEL']
                #d.update(control_panel)
                for key, val in control_panel.items():
                    d[key] = {}
                    for key1, val in val.items():
                        d[key][key1] = {}
                        url = val['URL'][0]
                        new_url = url.replace("<int:manage_id>", str(server_id), 1)
                        d[key][key1]['URL'] = (new_url,val['URL'][1], val['URL'][2] )
                    
                
    #print(d)
    return d
    


def sendNotification(user_id, typ, status, title, content):
    layer = get_channel_layer()
    print(user_id)
    async_to_sync(layer.group_send)(str(user_id), {
        'type': 'events.alarm',
        'msg_type': typ,
        'css_a': status,
        'title': title,
        'content': content
    })

def CheckLogin(request):

    if 'user_login' in request.session:
        try:
            sig = Signer()
            sig.unsign(request.session['user_login'])
            return True

        except:
            return False
    else:
        return False


def getUser(request):

    if 'user_login' in request.session:
        try:
            sig = Signer()
            em = sig.unsign(request.session['user_login'])
            return usr.objects.get(email=em, status="Active")

        except:
            return False
    else:
        return False



def randomString(stringLength=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


def randomNumber(length=5):
    #put your letters in the following string
    your_letters='0123456789'
    return ''.join((random.choice(your_letters) for i in range(length)))


