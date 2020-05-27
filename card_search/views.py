from django.shortcuts import render
from .forms import card_searchform, search_function
from home.models import cards
from home.models import UserProfile, decks, cards_in_deck
from django import forms
import math
from django.http import HttpRequest

#this function takes that data that the users seached and covertit into a page/url where all the cards that fit there critera are shown 
def search(request):
    if request.method == 'POST':
        form = card_searchform(request.POST)
        if form.is_valid(): 
            
            search_list = search_function(form)

            send_list2 = []
            form_list = ['cmc','cmc_op', 'color', 'cost', 'Keyword', 'legal', 'name', 'power', 'price', 'rules_text', 'sub_type', 'super_type', 'toughness']
            for i in form_list:
                check2 = form.cleaned_data[i]
                send_list2.append([i,check2])
            
            
            
            check = request.POST
            send_list = []
            for k, v in check.items():
                if not (v == '' or v == 'all' or k == 'csrfmiddlewaretoken'):
                    send_list.append((k,v))

            
            if request.user.is_authenticated == True:
                return render(request, 'card_search/cards_user_display.html', {'search_list': search_list1})
            else:
                return render(request, 'card_search/cards_display.html', {'search_list': search_list})
            #change this to a redirect to the display page 

        
    form = card_searchform()

    if request.user.is_authenticated == True:
        return render(request, 'card_search/user_card_search.html', {'form': form})
    else:
        return render(request, 'card_search/card_search.html', {'form': form})


def card_search_display(search_list):
    if len(search_list) > 60:
        number_pages = math.ceil((len(search_list))/60)
        page_list = []
        for p in range(number_pages):
            if p == math.ceil((len(search_list))/60):
                page_cards = search_list[((p-1) * 60):]
            else:
                page_cards = search_list[((p-1) * 60):(p * 60)]
            page_list.append(page_cards)
    else:
        page_list = search_list




#this takes all the information of a card and isplays it on one page 
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
            quantity = forms.DecimalField()

        if request.method == 'POST':
            form = card_add(request.POST)
            if form.is_valid(): 
                deck_id = form.cleaned_data.get("deck")
                user_deck = (decks.objects.filter(id=deck_id))[0]
                quantity = int(form.cleaned_data.get("quantity"))

            for i in range(quantity):
                new_add = cards_in_deck(deck=user_deck, card=card)
                new_add.save()


        form = card_add()
        return render(request, 'card_search/user_card_page.html', {'card': card, 'form': form})
    else:
        return render(request, 'card_search/card_page.html', {'card': card})