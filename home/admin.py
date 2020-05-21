from django.contrib import admin
from .models import decks, UserProfile,cards_in_deck, follow_modle, cards


admin.site.register(decks)
admin.site.register(UserProfile)
admin.site.register(cards_in_deck)
admin.site.register(follow_modle)
admin.site.register(cards)

