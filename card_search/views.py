from django.shortcuts import render, redirect
from .forms import card_searchform, search_function
from home.models import cards
from home.models import UserProfile, decks, cards_in_deck
from django import forms
import math
from django.http import HttpRequest
import ast
from django.views import View 



#probabably should add some real time display to the card search page with jquery and ajax


class search1(View):

    def get(self, request):
        form = card_searchform()

        if request.user.is_authenticated == True:
            return render(request, 'card_search/user_card_search.html', {'form': form})
        else:
            return render(request, 'card_search/card_search.html', {'form': form})

    def post(self, request):
        form = card_searchform(request.POST)
        if form.is_valid(): 
            
            #search_list = search_function(form)

            send_list2 = []
            form_list = ['cmc','cmc_op', 'color', 'cost', 'legal', 'name', 'power', 'power_op', 'price', 'rules_text', 'sub_type', 'super_type', 'toughness', 'toughness_op', 'card_type']
            for i in form_list:
                check2 = form.cleaned_data[i]
                if check2 == None:
                    check2 = ""
                send_list2.append(check2)

            return redirect(('http://localhost:8000/card_search/card_display/1/' + str(send_list2)))


class card_display1(View):

    def get(self, request, send_list, page):
        send_list = ast.literal_eval(send_list)
        search_list = search_function(send_list)

        if len(search_list) > 60:
            number_pages = math.ceil((len(search_list))/60)
            page_list = []
            for p in range(number_pages):
                if p == number_pages:
                    page_cards = search_list[((p-1) * 60):]
                    next_page = False 
                else:
                    page_cards = search_list[((p-1) * 60):(p * 60)]
                    next_page = True
                page_list.append(page_cards)
                current_page = page_list[(page-1)]

            if page == 1:
                previous_page = False
                next_page = True
            elif page == number_pages:
                previous_page = True
                next_page = False
            else:
                previous_page = True
                next_page = True         

        else:
            current_page = search_list
            previous_page = False
            next_page = False
            number_pages = 1

    
        if request.user.is_authenticated == True:
            return render(request, 'card_search/cards_user_display.html', {'search_list': current_page, 'next_page': next_page, 'send_list':send_list, 'page': page, 'previous_page':previous_page, 'number_pages':number_pages})
        else:
            return render(request, 'card_search/cards_display.html', {'search_list': current_page, 'next_page': next_page, 'send_list':send_list,'page':page, 'previous_page':previous_page, 'number_pages':number_pages})



#CHANGE THIS
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
#should add some ajax and jquery to the card page so user can see diffrent card images bace on set 





#turn the card page into a class baced view 
class card_page1(View):

    def get(self ,request , card_id):
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













