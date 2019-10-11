from django.db import models
from ..signup.models import user
from ..servers.models import list as server_id
from ..lamp.models import domain, ftp_account

# Create your models here.

class config(models.Model):
    
    server = models.ForeignKey(server_id, on_delete=models.CASCADE)
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    label = models.CharField(max_length=100, default="")
    header = models.CharField(max_length=500,  default=None, null=True)
    monitor = models.BooleanField(default=False)
    monitor_user = models.CharField(max_length=45, default=None, null=True)
    monitor_pass = models.CharField(max_length=45, default=None, null=True)
    algorithm = models.CharField(max_length=45, default="Round Robin")
    status = models.CharField(max_length=45)
    node_servers = models.CharField(max_length=100, default="")
    date = models.DateTimeField(auto_now_add=True)



class domains(models.Model):
    
    server = models.ForeignKey(server_id, on_delete=models.CASCADE)
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    domain_insert_withftp_dict = models.TextField(default="")
    domain_name = models.CharField(max_length=100)
    subdomain = models.CharField(max_length=100,default="")
    folder = models.CharField(max_length=100,default="")
    status = models.CharField(max_length=45)
    date = models.DateTimeField(auto_now_add=True)


class replicate_file(models.Model):
    
    server = models.ForeignKey(server_id, on_delete=models.CASCADE)
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    connected_domain = models.ForeignKey(domains, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=100)
    folder = models.CharField(max_length=100,default="")
    status = models.CharField(max_length=45)
    date = models.DateTimeField(auto_now_add=True)