from django.shortcuts import render, redirect
from home.models import decks, cards_in_deck, UserProfile, cards
from .forms import add_deck, publish_deck, deck_searchform
import collections
import random

# Create your views here.
def search_deck(request):

    if request.method == 'POST':
        form = deck_searchform(request.POST)
        if form.is_valid():
            
            hash_tags = form.cleaned_data.get("hash_tags")

            link = 'http://localhost:8000/deck_search/deck_display/' + (str(hash_tags))[1:]
            return redirect(link)

    form = deck_searchform()

    if request.user.is_authenticated == True:
        return render(request,'deck_search/user_search.html', {'form':form})
    else:
        return render(request, 'deck_search/search.html', {'form':form})



def deck_display(request, hash_tags):
    deck_list = decks.objects.filter(deck_publish=True)

    tag_list = hash_tags.split('#')
    for i in tag_list:
        deck_list = deck_list.filter(hash_tags__icontains=i)

    if request.user.is_authenticated == True:
        return render(request,'deck_search/user_deck_display.html',{'deck_list': deck_list})
    else:
        return render(request,'deck_search/deck_display.html', {'deck_list': deck_list})


def deck_page(request,id):
    deck = decks.objects.filter(id = id)
    card2 = cards_in_deck.objects.filter(deck = deck[0])
    hash_tags1 =[i.hash_tags for i in deck] 
    tags = list([(i[1:]).split('#') for i in hash_tags1])
    if len(tags) == 1:
        tags = tags[0]
    card1 = []
    for i in card2:
        j = i.card
        card1.append(j)
    
    card3 = list((collections.Counter(card1)).items())

    context = {'cards': card3, 'id1': id,'tags': tags }

    try:
        user = UserProfile.objects.filter(user = request.user)[0]
    except:
        user = 1

    deck1 = decks.objects.get(id=id)
    deck1.deck_views = deck1.deck_views + 1
    deck1.save(update_fields=['deck_views'])



    if request.user.is_authenticated == True:
        if UserProfile.objects.filter(user = request.user)[0] == ((decks.objects.filter(id = id))[0]).deck_creator:
            return render(request, 'deck_search/my_deck_page.html', context)
        else:
            return render(request, 'deck_search/user_deck_page.html', context)
    else:
        return render(request, 'deck_search/deck_page.html', context)

#under this are deck page functions

def copy_deck(request,id):

    deck = decks.objects.filter(id = id)

    deck_creator = UserProfile.objects.filter(user = request.user)[0]
    deck_name =  deck[0].deck_name + '-copy'
    hash_tags = ''
    deck_discription = ''
    deck_views = 0
    deck_copies = 0
    deck_type = deck[0].deck_type

    new_deck = decks(deck_creator=deck_creator, deck_name=deck_name, hash_tags=hash_tags, deck_discription=deck_discription, deck_views=deck_views, deck_copies=deck_copies, deck_type=deck_type)
    new_deck.save()

    card2 = cards_in_deck.objects.filter(deck = deck[0])
    current_user = UserProfile.objects.filter(user = request.user)[0]
    deck_list = decks.objects.filter(deck_creator = current_user)
    deck2 = deck_list[(len(deck_list)-1)]

    for i in card2:
        j = i.card
        new_card = cards_in_deck(deck=deck2, card=j)
        new_card.save()

    
    deck1 = decks.objects.get(id=id)
    deck1.deck_copies = deck1.deck_copies + 1
    deck1.save(update_fields=['deck_copies'])


    return redirect('http://localhost:8000/user_social/user_home')


def new_deck(request):

    return render(request, 'deck_search/new_deck.html')

def new_deck_name(request,type1):

    if request.method == 'POST':
        form = add_deck(request.POST)
        if form.is_valid():

            deck_creator = UserProfile.objects.filter(user = request.user)[0]
            deck_name =  form.cleaned_data.get("deck_name")
            hash_tags = ''
            deck_discription = ''
            deck_views = 0
            deck_copies = 0
            deck_type = str(type1)

            new_deck = decks(deck_creator=deck_creator, deck_name=deck_name, hash_tags=hash_tags, deck_discription=deck_discription, deck_views=deck_views, deck_copies=deck_copies, deck_type=deck_type )
            new_deck.save()

            return redirect('http://localhost:8000/user_social/user_home')

    form = add_deck()

    return render(request, 'deck_search/new_deck_name.html', {'form': form})


def delete_deck(request, id):

    decks.objects.filter(id=id).delete()

    return redirect('http://localhost:8000/user_social/user_home')



def publish_deck_v(request, id):

    if request.method == 'POST':
        form = publish_deck(request.POST)
        if form.is_valid():
            deck1 = decks.objects.get(id=id)

            deck1.hash_tags = form.cleaned_data.get('hash_tags')
            deck1.deck_discription =  form.cleaned_data.get("deck_discription")
            deck1.deck_publish = True
            
            deck1.save(update_fields=['hash_tags','deck_discription', 'deck_publish', 'date_publish'])
            return redirect('http://localhost:8000/user_social/user_home')

    
    form =  publish_deck()
        

    return render(request, 'deck_search/publish_deck.html', {'form': form}) 


def sample_hand(request, id):
    deck = (decks.objects.filter(id=id))[0]
    cards = list(cards_in_deck.objects.filter(deck=deck))
    number_of_cards = len(cards) 
    if number_of_cards > 7:
        hand = (random.sample(cards, 7))
        hand2 = [i.card for i in hand]


        if request.user.is_active == True:
            return render(request,'deck_search/user_sample_hand.html', {'hand': hand2, 'id': id})
        else:
            return render(request,'deck_search/sample_hand.html', {'hand': hand2, 'id':id})
    else:
        return redirect('/deck_search/deck_page/' + str(id))


def popular_decks(request):
    deck_list = decks.objects.filter(deck_publish=True)
    deck_list = deck_list.extra( order_by = ['-deck_copies'])
    
    if request.user.is_active == True:
        return render(request, 'deck_search/user_popular_decks.html', {'deck_list': deck_list})
    else:
        return render(request, 'deck_search/popular_decks.html', {'deck_list': deck_list})