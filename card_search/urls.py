from django.urls import path, include
from . import views
#this file takes urls from the web and redirects them to the views that will exicue a function baced on the url entered 
urlpatterns = [
    path('search/', views.search),
    path('card_page/<card_id>', views.card_page)
    
]