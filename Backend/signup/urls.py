from django.urls import path
from . import views

urlpatterns = [
    path('signup', views.signup, name='User Sign Up, Code => /Backend/signup/')
]