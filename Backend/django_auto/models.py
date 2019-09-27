from django.db import models
from django.db import models
from Backend.signup.models import user, projects
from Backend.servers.models import list
# Create your models here.


class virtual_env(models.Model):
       
    server = models.ForeignKey(list, on_delete=models.CASCADE)
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    envirnment_name = models.CharField(default="", max_length=250)
    install_dir = models.CharField(default="", max_length=250)
    python_inter_full = models.CharField(default="", max_length=250)
    python_inter = models.CharField(default="", max_length=250)
    date = models.DateTimeField(auto_now_add=True)
    
