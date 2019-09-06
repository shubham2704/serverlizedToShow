from django.shortcuts import render
from django.core.mail import EmailMessage
from django.core.signing import Signer
from django.http import HttpResponse
from django.contrib import messages
from .models import user

# Create your views here.


def signup(request):

    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone_no = request.POST['phone_no']
        password = request.POST['password']
        confirm = request.POST['confirm']

        if first_name!='' and last_name!='' and email!='' and phone_no!='' and password!='' and confirm!='':

             if password==confirm:

                 if email_verify==False and phone_verify==False:

                     obj, insert_user = user.objects.get_or_create(first_name=first_name, last_name=last_name, email=email, phone_no=phone_no,password=password, status='Active', email_hash=email_hash, otp=otp, phone_status='Not Verified', email_status='Not Verified')
    return render(request, "user/signup.html")