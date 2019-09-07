from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.core.signing import Signer
from django.core.validators import validate_email
from django.contrib import messages
from ..BackendController.contri import CheckLogin
from ..signup.models import user as usr
# Create your views here.

def login(request):

    if CheckLogin(request) == True:
        return redirect("/wpanel/")

    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        try:
            validate_email(email)
            user = usr.objects.get(email=email, status="Active")
            sign = Signer()
            unsign = sign.unsign(user.password)

            if unsign == password:
                request.session['user_login'] = sign.sign(user.email)
                return redirect("/wpanel/")
            else:
                messages.warning(request, "Invalid email or password")
        except:
            messages.warning(request, "Invalid email or email does not exist.")

    return render(request, "user/login.html")