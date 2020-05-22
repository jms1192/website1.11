from django.shortcuts import render
from .forms import card_searchform, search_function
from home.models import cards
from home.models import UserProfile, decks, cards_in_deck
from django import forms


def search(request):
    if request.method == 'POST':
        form = card_searchform(request.POST)
        if form.is_valid(): 
            
            search_list = search_function(form)
            if request.user.is_authenticated == True:
                return render(request, 'card_search/cards_user_display.html', {'search_list': search_list})
            else:
                return render(request, 'card_search/cards_display.html', {'search_list': search_list})
            #change this to a redirect to the display page 

    
        
    form = card_searchform()
    if request.user.is_authenticated == True:
        return render(request, 'card_search/user_card_search.html', {'form': form})
    else:
        return render(request, 'card_search/card_search.html', {'form': form})


def card_page(request, card_id):

    card = cards.objects.filter(id=card_id)[0]

    if request.user.is_authenticated == True:
        DECKS = []
        current_user = (UserProfile.objects.filter(user=request.user))[0]
        deck_list = decks.objects.filter(deck_creator = current_user)   
        for i in deck_list:
            j = (str(i.id), str(i.deck_name))
            DECKS.append(j)
    
        class card_add(forms.Form):
            deck = forms.ChoiceField(required= True, widget=forms.RadioSelect, choices=DECKS)

        if request.method == 'POST':
            form = card_add(request.POST)
            if form.is_valid(): 
                deck_id = form.cleaned_data.get("deck")
                user_deck = (decks.objects.filter(id=deck_id))[0]


            new_add = cards_in_deck(deck=user_deck, card=card)
            new_add.save()


        form = card_add()
        return render(request, 'card_search/user_card_page.html', {'card': card, 'form': form})
    else:
        return render(request, 'card_search/card_page.html', {'card': card})