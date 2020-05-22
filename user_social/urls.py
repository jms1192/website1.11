from django.urls import path, include
from . import views

urlpatterns = [
    path('user_home', views.user_home),
    path('social_home', views.social_home),
    path('follow_page/<id>/<kind>', views.follow_list),
    path('other_player_profile/<id>', views.other_player_profile),
    
]