from django.shortcuts import render, redirect
from home.models import decks, cards_in_deck, UserProfile, cards
from .forms import add_deck, publish_deck, deck_searchform, add_card_to_deck
import collections
import random
from django.views import View

#this loads the data for the deck search page 

class search_deck1(View):

    def get(self,request):
        form = deck_searchform()

        if request.user.is_authenticated == True:
            return render(request,'deck_search/user_search.html', {'form':form})
        else:
            return render(request, 'deck_search/search.html', {'form':form})
    
    def post(self, request):
        form = deck_searchform(request.POST)
        if form.is_valid():
            
            hash_tags = form.cleaned_data.get("hash_tags")

            link = 'http://localhost:8000/deck_search/deck_display/1/' + (str(hash_tags))[1:]
            return redirect(link)


#this loads the data for the results of the search page 

class deck_display1(View):
    def get(self, request, page, hash_tags):
        deck_list = decks.objects.filter(deck_publish=True)

        tag_list = hash_tags.split('#')
        for i in tag_list:
            deck_list = deck_list.filter(hash_tags__icontains=i)
            deck_list = deck_list.extra( order_by = ['-deck_copies'])

        if len(deck_list) > 30:
            number_pages = math.ceil((len(deck_page))/30)
            page_list = []
            for p in range(number_pages):
                if p == number_pages:
                    page_cards = deck_list[((p-1) * 30):]
                    next_page = False 
                else:
                    page_cards = deck_list[((p-1) * 30):(p * 30)]
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
            current_page = deck_list
            previous_page = False
            next_page = False
            number_pages = 1



        if request.user.is_authenticated == True:
            return render(request,'deck_search/user_deck_display.html',{'deck_list': current_page, 'previous_page':previous_page, 'number_pages':number_pages, 'next_page':next_page, 'hash_tags':hash_tags, 'page':page})
        else:
            return render(request,'deck_search/deck_display.html', {'deck_list': current_page, 'previous_page':previous_page, 'number_pages':number_pages, 'next_page':next_page, 'hash_tags':hash_tags, 'page':page})


#this loads the data for a deck pages on if the users is loged in and what kind of deck it is 


#under this are deck page functions

class deck_page1(View):

    def get(self, request, id):
        deck = decks.objects.filter(id = id)
        card2 = cards_in_deck.objects.filter(deck = deck[0]).exclude(is_commander = True).exclude(is_sideboard=True)
        hash_tags1 =[i.hash_tags for i in deck] 
        tags = list([(i[1:]).split('#') for i in hash_tags1])
        if len(tags) == 1:
            tags = tags[0]
        card1 = []
        for i in card2:
            j = i.card
            card1.append(j)
    
        card3 = list((collections.Counter(card1)).items())
        #can change type list to any othey card atribute to change how the cards are sorted
        type_list = [x[0].type1 for x in card3]
        type_list = list(dict.fromkeys(type_list))
        #sort_list = sort_function 

        cards_split = []
        for i in type_list:
            x = [x for x in card3 if x[0].type1 == i]
            y = sum([y[1] for y in x ])
            cards_split.append([i,y,x])
        #broken up baced on kind of could possibly be more efficent 
        deck_kind = deck[0].deck_type
        if deck[0].deck_type == 'Commander':
            try:
                commander =  (cards_in_deck.objects.filter(deck = deck[0]).filter(is_commander = True))[0].card
            except:
                commander = 2
            sideboard = 1
            context = {'cards': cards_split, 'id1': id,'tags': tags, 'commander':commander, 'sideboard': sideboard }


        elif (deck[0]).deck_type == 'Constructed':
            try:
                side = [(i.card) for i in cards_in_deck.objects.filter(deck = deck[0]).filter(is_sideboard= True)]
                sideboard = list((collections.Counter(side)).items())

            except:
                sideboard = 2
            commander = 1
            context = {'cards': cards_split, 'id1': id,'tags': tags, 'commander':commander, 'sideboard': sideboard }

        else:
            sideboard = 1
            commander = 1
            context = {'cards': cards_split, 'id1': id,'tags': tags, 'commander':1, 'sideboard': sideboard }

        try:
            user = UserProfile.objects.filter(user = request.user)[0]
        except:
            user = 1

        deck1 = (decks.objects.get(id=id))
        if not user == deck1.deck_creator:
            deck1.deck_views = deck1.deck_views + 1
            deck1.save(update_fields=['deck_views'])

        form = add_card_to_deck()
        context.update({'form':form})
        if request.user.is_authenticated == True:
            if UserProfile.objects.filter(user = request.user)[0] == ((decks.objects.filter(id = id))[0]).deck_creator:
                return render(request, 'deck_search/my_deck_page.html', context)
            else:
                return render(request, 'deck_search/user_deck_page.html', context)
        else:
            return render(request, 'deck_search/deck_page.html', context)
    
    def post(self, request, id):
        deck1 = (decks.objects.get(id=id))
        form = add_card_to_deck(request.POST)
        if form.is_valid():
                    #handel form
            card_name = form.cleaned_data.get("card_name")
            quantity = form.cleaned_data.get("quantity")
            try:
                card_added = (cards.objects.filter(name=card_name))[0]
            except:
                card_added = False 
            if not card_added == False:#should probably return else not a card        
                for i in range(quantity):
                    new_card = cards_in_deck(card=card_added, deck=deck1, is_commander=False, is_sideboard=False)
                    new_card.save()
            return redirect('http://localhost:8000/deck_search/deck_page/' + str(id))



#this function will make a new copie of a published deck that sombody does not have and put it in their decks 
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

#this will load the new deck page where you can choose what kind of deck you want 
def new_deck(request):

    return render(request, 'deck_search/new_deck.html')


#this will load the page where you can name your deck and acutaly creates the deck when you name it 
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

#this function lets somebody delete their own deck 
def delete_deck(request, id):

    decks.objects.filter(id=id).delete()

    return redirect('http://localhost:8000/user_social/user_home')


#this function lets somebody publish their own deck 
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

#this gives sombody a sample hand of thier deck 
def sample_hand(request, id):
    deck = (decks.objects.filter(id=id))[0]
    cards = list(cards_in_deck.objects.filter(deck=deck).filter(is_commander=False).filter(is_sideboard=False))
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

#this show the published decks with the most copies 
def popular_decks(request):
    deck_list = decks.objects.filter(deck_publish=True)
    deck_list = deck_list.extra( order_by = ['-deck_copies'])
    if len(deck_list) > 30:
        deck_list = deck_list[0:30]
    
    if request.user.is_active == True:
        return render(request, 'deck_search/user_popular_decks.html', {'deck_list': deck_list})
    else:
        return render(request, 'deck_search/popular_decks.html', {'deck_list': deck_list})

#this moves a card in your deck to the commander spot of your deck 
def make_commander(request,id_c,id_d):
    deck = decks.objects.filter(id=id_d)[0]
    card = cards.objects.filter(id=id_c)[0]
    new_commander = (cards_in_deck.objects.filter(card=card).filter(deck=deck))[0]

    try:
        old_commander = (cards_in_deck.objects.filter(deck=deck).filter(is_commander=True))[0]
        old_commander.is_commander = False
        old_commander.save(update_fields=['is_commander'])
    except:
        none = 'cool'

    new_commander.is_commander = True
    new_commander.save(update_fields=['is_commander'])

    return redirect(('http://localhost:8000/deck_search/deck_page/' + str(id_d)))


#this moves a card in your deck to the sideboard spot of your deck 
def add_sideboard(request,id_c,id_d):

    deck = decks.objects.filter(id=id_d)[0]
    card = cards.objects.filter(id=id_c)[0]
    moved_to_sideboard = (cards_in_deck.objects.filter(card=card).filter(deck=deck).exclude(is_sideboard=True))[0]
    moved_to_sideboard.is_sideboard = True
    moved_to_sideboard.save(update_fields=['is_sideboard'])
    return redirect(('http://localhost:8000/deck_search/deck_page/' + str(id_d)))

#this lets you move cards back to your deck from the sideboard 
def from_sideboard_to_deck(request,id_c,id_d):
    deck = decks.objects.filter(id=id_d)[0]
    card = cards.objects.filter(id=id_c)[0]
    moved_to_deck = (cards_in_deck.objects.filter(card=card).filter(deck=deck).filter(is_sideboard=True))[0]
    moved_to_deck.is_sideboard = False
    moved_to_deck.save(update_fields=['is_sideboard'])
    return redirect(('http://localhost:8000/deck_search/deck_page/' + str(id_d)))

#this removes a crard from your deck 
def remonve_card_from_deck(request,id_c,id_d):
    deck = decks.objects.filter(id=id_d)[0]
    card = cards.objects.filter(id=id_c)[0] 
    deck_deleted = (cards_in_deck.objects.filter(card=card).filter(deck=deck))[0]
    deck_deleted.delete()
    return redirect(('http://localhost:8000/deck_search/deck_page/' + str(id_d)))



#impelment this later as a function of the deckpage view
#def sort_function(sort_kind):
    #if sort_kind == "type":
        #sort_list = [x[0].type1 for x in card3]
        #sort_list = list(dict.fromkeys(sort_list))

    #elif sort_kind == 'sub_type':
        #sort_list = [x[0].subtypes for x in card3]
        #sort_list = list(dict.fromkeys(sort_list))

    #elif sort_kind == 'color':
        #sort_list = [x[0].colors if len(x[0].colors) <= 1 else 'multicolored' for x in card3]
        #sort_list = list(dict.fromkeys(sort_list))

    #elif sort_kind == 'cmc':
        #sort_list = [x[0].type1 for x in card3]
        #sort_list = list(dict.fromkeys(sort_list))
    
    #return(sort_list)


def deck_analysis(request,d_id):

    deck = (decks.objects.filter(id=d_id))[0]
    cards_deck = [i.card for i in cards_in_deck.objects.filter(deck__exact=deck)]

    total_cmc = 0 
    for i in cards_deck:
        total_cmc = total_cmc + i.convertedManaCost
    mana_needed = float(total_cmc)/4.9
    non_land_cards= [i for i in cards_deck if not i.type1 == 'land']


    white_mana_symbols = 0
    blue_mana_symbols = 0
    green_mana_symbols = 0
    black_mana_symbols = 0
    red_mana_symbols = 0
    colorless_mana_symbols = 0
    total_mana_symbols = 0 
    #need to change color list for non normal mana symbols
    #color_list = ['W', 'U', 'G'] iterating through something like this will probably be more efficent/ good looking

    for i in non_land_cards:
        mana_cost = i.manaCost
        mana_cost = (mana_cost[1:-1]).split('}{')
        #the mana_cost calculation might need to be changed a little 
        for j in mana_cost:
            if 'W' in j:
                white_mana_symbols += 1
                total_mana_symbols += 1
            if 'U' in j:
                blue_mana_symbols += 1
                total_mana_symbols += 1
            if 'G' in j:
                green_mana_symbols += 1
                total_mana_symbols += 1
            if 'B' in j:
                black_mana_symbols += 1
                total_mana_symbols += 1
            if 'R' in j:
                red_mana_symbols += 1
                total_mana_symbols += 1
            if 'C' in j:
                colorless_mana_symbols += 1
                total_mana_symbols += 1

    if not total_mana_symbols == 0:
        white_recomended = round(((white_mana_symbols / total_mana_symbols) * mana_needed), 1)
        blue_recomended  = round(((blue_mana_symbols / total_mana_symbols) * mana_needed), 1)
        green_recomended  = round(((green_mana_symbols / total_mana_symbols) * mana_needed), 1)
        black_recomended  = round(((black_mana_symbols / total_mana_symbols) * mana_needed), 1)
        red_recomended  = round(((red_mana_symbols / total_mana_symbols) * mana_needed), 1)
        colorless_recomended  = round(((colorless_mana_symbols / total_mana_symbols) * mana_needed), 1)
    else:
        white_recomended = 0
        blue_recomended  = 0
        green_recomended  = 0
        black_recomended  = 0
        red_recomended  = 0
        colorless_recomended  = 0

    mana_needed = round(mana_needed,1)
    average_mana_cost = total_cmc/len(non_land_cards)

    context = {'white_recomended': white_recomended, 'blue_recomended': blue_recomended, 'green_recomended': green_recomended,'black_recomended':black_recomended,'red_recomended':red_recomended, 'colorless_recomended': colorless_recomended, 'average_mana_cost': average_mana_cost, 'mana_needed': mana_needed, 'id':d_id }
    
    if request.user.is_active == True:
        return render(request, 'deck_search/user_deck_analysis.html', context)
    else:
        return render(request, 'deck_search/deck_analysis.html', context)