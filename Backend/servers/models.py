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
    Charges = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)
    date = models.DateTimeField(auto_now_add=True)
    running_status = models.CharField(max_length=45)
    password = models.CharField(max_length=250,default="")
    parent_server = models.CharField(max_length=250,default="")

