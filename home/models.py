from django.db import models
from django.contrib.auth.models import User
from django_mysql.models import ListCharField
from django.db.models import CharField, DecimalField, BooleanField


#this file holds all of the tables in the databace

class cards(models.Model):

    colorIdentity = ListCharField(base_field=CharField(max_length=250), size=7, max_length=20000)
    colorIndicator = ListCharField(base_field=CharField(max_length=250), size=7, max_length=20000)
    colors = CharField(max_length=200)
    convertedManaCost = DecimalField(decimal_places=1, max_digits=4)
    faceConvertedManaCost = DecimalField(decimal_places=1, max_digits=4)   
    hasNoDeckLimit = BooleanField()
    isReserved = BooleanField()    
    layout = CharField(max_length=100)

    #legalities
    legal_brawl = CharField(max_length=200)
    legal_commander = CharField(max_length=200)
    legal_duel = CharField(max_length=200) 
    legal_future = CharField(max_length=200)
    legal_frontier = CharField(max_length=200)
    legal_legacy = CharField(max_length=200)
    legal_modern = CharField(max_length=200)
    legal_pauper = CharField(max_length=200)
    legal_penny = CharField(max_length=200)
    legal_pioneer = CharField(max_length=200)
    legal_standard = CharField(max_length=200)
    legal_vintage = CharField(max_length=200)

    loyalty = CharField(max_length=10)
    manaCost = CharField(max_length=10)
    name = CharField(max_length=200)
    names = ListCharField(base_field=CharField(max_length=250), size=10, max_length=20000)
    power = CharField(max_length=10)
    #printings = ListCharField(base_field=CharField(max_length=200), size=50, max_length=20000)
    side = CharField(max_length=100)
    subtypes = ListCharField(base_field=CharField(max_length=250), size=10, max_length=20000)
    supertypes = ListCharField(base_field=CharField(max_length=200), size=20, max_length=20000)
    rulesText =  CharField(max_length=500)
    toughness = CharField(max_length=10)
    type1 = CharField(max_length=100)
    #Type of the card. Includes any supertypes and subtypes.
    types = ListCharField(base_field=CharField(max_length=200), size=50, max_length=20000)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class decks(models.Model):

    deck_creator = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    deck_name = models.CharField(max_length=100)
    hash_tags = models.CharField(max_length = 250)
    deck_discription = models.CharField(max_length=500)
    #deck_image = models.ImageField( height_field=None, width_field=None, max_length=100) fix this
    deck_views = models.PositiveIntegerField()
    deck_copies = models.PositiveIntegerField()
    deck_publish = models.BooleanField(default=False)
    deck_type = models.CharField(max_length=20, default='nome')
    date_publish = models.DateTimeField(auto_now=True)



class cards_in_deck(models.Model):
    deck = models.ForeignKey(decks, on_delete=models.CASCADE)
    card = models.ForeignKey(cards, on_delete=models.CASCADE)
    is_commander = models.BooleanField(default=False)
    is_sideboard = models.BooleanField(default=False)

class follow_modle(models.Model):
    follower =  models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='follower')
    followed = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='followed')


class card_set_model(models.Model):
    card_set = models.CharField(max_length=10)
    date_releced = models.DateField()
    #set image

class cards_in_set(models.Model):
    card = models.ForeignKey(cards, on_delete=models.CASCADE)
    card_set = models.ForeignKey(card_set_model, on_delete=models.CASCADE)
    #card image
