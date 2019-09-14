from django.db import models
from ..signup.models import user
from ..servers.models import list as server_id

# Create your models here.

class domain(models.Model):
    
    server = models.ForeignKey(server_id, on_delete=models.CASCADE)
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    domain_name = models.CharField(max_length=100)
    subdomain = models.CharField(max_length=100,default="")
    folder = models.CharField(max_length=100,default="")
    status = models.CharField(max_length=45)
    date = models.DateTimeField(auto_now_add=True)


class mysql_user(models.Model):
    
    server = models.ForeignKey(server_id, on_delete=models.CASCADE)
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    name = models.CharField(max_length=100,default="")
    remote = models.BooleanField(default=False)
    password = models.CharField(max_length=100,default="")
    permissions = models.TextField()
    status = models.CharField(max_length=45)
    date = models.DateTimeField(auto_now_add=True)


class mysql_database(models.Model):
    
    server = models.ForeignKey(server_id, on_delete=models.CASCADE)
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    database_name = models.CharField(max_length=100)
    mysql_user = models.ForeignKey(mysql_user, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)