from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from . import views

#this file takes urls from the web and redirects them to the views that will exicue a function baced on the url entered 
urlpatterns = [
    path('', views.home),
    path('about/', views.about),
    path('create_account/', views.create_account),
    path('login/', views.login_page),
    path('logout/', views.logout_page),
]