from django.urls import path, include
from ..BackendController.server_config import PACKAGES
from django.utils.module_loading import import_string
from . import views

urlpatterns = [
    path('wpanel/', views.panel, name='User Sign Up, Code => /Backend/servers/'),
    path('wpanel/<int:server_id>', views.manage_server, name='Manage Server, Code => /Backend/servers/'),
    path('wpanel/<int:server_id>/package', views.package_manager, name='Manage Package, Code => /Backend/servers/'),
    path('wpanel/deploy', views.deploy, name='Deploy Server, Code => /Backend/servers/'),
    path('wpanel/package/<int:pkg_id>', views.pkg_details, name='Package Details, Code => /Backend/servers/'),
]

control_url = []

for key, pkg in PACKAGES.items():
    control = pkg['CONTROL_PANEL']
    for key, cntr in control.items():
        for key_a, cop in cntr.items():
            if key_a != 'ICON':
            
                control_url.append(path(cop['URL'][0], import_string(cop['URL'][1])))
            
urlpatterns += control_url
