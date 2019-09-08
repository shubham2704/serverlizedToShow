from django.urls import path
from . import views

urlpatterns = [
    path('wpanel/', views.panel, name='User Sign Up, Code => /Backend/servers/'),
    path('wpanel/deploy', views.deploy, name='Deploy Server, Code => /Backend/servers/')
]