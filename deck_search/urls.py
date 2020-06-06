from django.urls import path, include
from . import views
from .views import search_deck1, deck_display1, deck_page1
#this file takes urls from the web and redirects them to the views that will exicue a function baced on the url entered
urlpatterns = [
    path('search_deck/', search_deck1.as_view()),
    path('deck_page/<id>', deck_page1.as_view()),
    path('copy_deck/<id>', views.copy_deck),
    path('new_deck/', views.new_deck),
    path('new_deck_name/<type1>', views.new_deck_name),
    path('delete_deck/<id>', views.delete_deck),
    path('publish_deck/<id>', views.publish_deck_v),
    path('sample_hand/<id>', views.sample_hand),
    path('deck_display/<page>/<hash_tags>', deck_display1.as_view()),
    path('popular_decks/', views.popular_decks),
    path('make_commander/<id_c>/<id_d>', views.make_commander),
    path('add_sideboard/<id_c>/<id_d>', views.add_sideboard),
    path('delete_card/<id_c>/<id_d>', views.remonve_card_from_deck),
    path('move_from_sideboard/<id_c>/<id_d>', views.from_sideboard_to_deck),
    path('deck_analysis/<d_id>', views.deck_analysis)
    

    
]