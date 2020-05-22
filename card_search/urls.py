from django.urls import path, include
from . import views

urlpatterns = [
    path('search/', views.search),
    path('card_page/<card_id>', views.card_page)
    
]