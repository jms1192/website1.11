from django.urls import path, include
from . import views
from .views import search1, card_display1

#this file takes urls from the web and redirects them to the views that will exicue a function baced on the url entered 
urlpatterns = [
    path('search/', search1.as_view()),
    path('card_page/<card_id>', views.card_page),
    path('card_display/<page>/<send_list>', card_display1.as_view())
    
]