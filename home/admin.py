from django.contrib import admin
from .models import decks, UserProfile,cards_in_deck, follow_modle, cards

#this file allows the admin to look at what data is is what modles in the django built in admin page 
admin.site.register(decks)
admin.site.register(UserProfile)
admin.site.register(cards_in_deck)
admin.site.register(follow_modle)
admin.site.register(cards)


