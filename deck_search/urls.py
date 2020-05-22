from django.urls import path, include
from . import views

urlpatterns = [
    path('search_deck/', views.search_deck),
    path('deck_page/<id>', views.deck_page),
    path('copy_deck/<id>', views.copy_deck),
    path('new_deck/', views.new_deck),
    path('new_deck_name/<type1>', views.new_deck_name),
    path('delete_deck/<id>', views.delete_deck),
    path('publish_deck/<id>', views.publish_deck_v),
    path('sample_hand/<id>', views.sample_hand),
    path('deck_display/<hash_tags>', views.deck_display)

    
]