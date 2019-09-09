from django.urls import path, include
from ..BackendController.server_config import PACKAGES
from django.utils.module_loading import import_string
from . import views

urlpatterns = [
    path('wpanel/', views.panel, name='User Sign Up, Code => /Backend/servers/'),
    path('wpanel/deploy', views.deploy, name='Deploy Server, Code => /Backend/servers/'),
]

control_url = []

for key, pkg in PACKAGES.items():
    control = pkg['CONTROL_PANEL']
    for key, cntr in control.items():
        for key_a, cop in cntr.items():
            
            control_url.append(path(cop['URL'][0], import_string(cop['URL'][1])))
            
urlpatterns += control_url
