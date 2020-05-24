from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('about/', views.about),
    path('create_account/', views.create_account),
    path('login/', views.login_page),
    path('logout/', views.logout_page),
    path('user_conformation/', views.user_conformation)
]