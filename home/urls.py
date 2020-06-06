from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from . import views
from .views import create_account1, login_page1

#this file takes urls from the web and redirects them to the views that will exicue a function baced on the url entered 
urlpatterns = [
    path('', views.home),
    path('about/', views.about),
    path('create_account/', create_account1.as_view()),
    path('login/', login_page1.as_view()),
    path('logout/', views.logout_page),
]