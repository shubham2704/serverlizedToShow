from django.core.signing import Signer
from ..signup.models import user as usr
import random
import string

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


