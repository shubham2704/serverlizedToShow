from django.db import models

class user(models.Model):

    first_name = models.CharField(max_length=75)
    last_name = models.CharField(max_length=75)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=250)
    email_verify = models.BooleanField(default=False)
    email_hash = models.CharField(max_length=100)
    contry_code = models.IntegerField()
    phone_no = models.IntegerField()
    phone_otp = models.IntegerField()
    phone_verify = models.BooleanField(default=False)
    status = models.CharField(max_length=75)
    money = models.DecimalField(max_digits=4, decimal_places=2)
    gstin = models.CharField(max_length=75)
    date = models.DateTimeField(auto_now_add=True)


class address(models.Model):
    user_id = models.ForeignKey(user, on_delete=models.CASCADE)
    address = models.CharField(max_length=150)
    state = models.CharField(max_length=75)
    city = models.CharField(max_length=75)
    pincode = models.IntegerField()
    country = models.CharField(max_length=25)
    isPrimary = models.BooleanField(default=False)
