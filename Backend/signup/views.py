from django.shortcuts import render
from django.core.mail import EmailMessage
from django.core.signing import Signer
from django.http import HttpResponse
from django.core.validators import validate_email
from django.contrib import messages
from django.db.models import Q
from ..BackendController.contri import randomString, randomNumber
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
        try:
            validate_email(email)
            if first_name!='' and last_name!='' and email!='' and phone_no!='' and password!='' and confirm!='' and len(phone_no) == 10:

                if password==confirm:

                        email_hash = randomString(25)
                        otp = randomNumber(5)
                        signer = Signer()
                        password = signer.sign(password)
                        
                        check_usr = user.objects.filter(Q(email__icontains=email) | 
                                Q(phone_no__icontains=phone_no)).count()
                        print(check_usr)
                        if check_usr == 0:
                        
                            insert_user = user.objects.create(contry_code=91, first_name=first_name, last_name=last_name, email=email, phone_no=phone_no,password=password, status='Active', email_hash=email_hash, phone_otp=otp, phone_verify=False, email_verify=False)
                            if insert_user:
                                messages.success(request, "Account succesfully created, You may login now.")
                        else:
                            messages.warning(request, "Email or phone no. already exist.")
                else:
                    messages.warning(request, "Password does not match")

        except :
            messages.warning(request, "Email address is invalid")
                
        else:
            messages.warning(request, "All fields are mandatory *")
    return render(request, "user/signup.html")