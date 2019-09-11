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
