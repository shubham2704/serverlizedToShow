from django.db import models
from ..signup.models import user, projects
# Create your models here.

class list(models.Model):
    SERVER_TYPES = (
        ('MASTER', 'MASTER'),
        ('SLAVE', 'SLAVE'),
    )
    server_name = models.CharField(max_length=45)
    user_id = models.ForeignKey(user, on_delete=models.CASCADE)
    distribution_id = models.IntegerField()
    stack_id = models.IntegerField()
    stack_name = models.CharField(max_length=55,default="")
    superuser = models.CharField(max_length=55,default="")
    ServerType = models.CharField(
        max_length=25,
        choices=SERVER_TYPES,default='MASTER')
    server_status = models.CharField(max_length=45)
    server_ip = models.CharField(max_length=25)
    project_id = models.ForeignKey(projects, on_delete=models.CASCADE)
    JSON_PKG_LST = models.TextField(default="{}")
    Charges = models.DecimalField(max_digits=10, decimal_places=6, default=0.000000)
    date = models.DateTimeField(auto_now_add=True)
    running_status = models.CharField(max_length=45)
    password = models.CharField(max_length=250,default="")
    hostname = models.CharField(max_length=250,default="")
    parent_server = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)


class Pkg_inst_data(models.Model):
   
    server = models.ForeignKey(list, on_delete=models.CASCADE)
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    PackageId = models.IntegerField()
    ViewPKGOption = models.BooleanField(default=True)
    PackageName = models.CharField(max_length=250,default="")
    PackageStatus = models.CharField(max_length=250,default="")
    date = models.DateTimeField(auto_now_add=True)
    

class output(models.Model):
       
    server = models.ForeignKey(list, on_delete=models.CASCADE)
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    PackageId = models.IntegerField()
    command = models.CharField(default="", max_length=250)
    output = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    


class server_stats(models.Model):
       
    server = models.ForeignKey(list, on_delete=models.CASCADE)
    json_data = models.TextField()
    ram_data = models.TextField()
    cpu_data = models.TextField()
    storage_data = models.TextField()
    date = models.DateTimeField(auto_now_add=True)


class billing(models.Model):
    
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    server = models.ForeignKey(list, on_delete=models.CASCADE)
    message = models.CharField(max_length=75)
    status = models.BooleanField(default=True)
    monthly_amount = models.DecimalField(max_digits=10, decimal_places=6, default=0.000000)
    date = models.DateTimeField(auto_now_add=True)


class notifications(models.Model):
       
    server = models.ForeignKey(list, on_delete=models.CASCADE, null=True)
    message = models.TextField()
    seen = models.BooleanField(default=False)
    icon = models.CharField(default="", max_length=20)
    color = models.CharField(default="", max_length=20)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(user, on_delete=models.CASCADE)