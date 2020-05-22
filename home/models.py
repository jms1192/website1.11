from django.db import models
from django.contrib.auth.models import User

class cards(models.Model):
    name = models.CharField(max_length=100)
    cost = models.CharField(max_length=100)
    cmc = models.DecimalField(max_digits=5, decimal_places=1)
    color =models.CharField(max_length=100)
    type1 = models.CharField(max_length=100)
    sub_type = models.CharField(max_length=100) 
    supper_type = models.CharField(max_length=100)
    sets = models.CharField(max_length=200)
    rulestext = models.CharField(max_length=500)
    flavor_text =models.CharField(max_length=500)
    power = models.DecimalField(max_digits=5, decimal_places=1)
    toughness = models.DecimalField(max_digits=5, decimal_places=1)
    loyality = models.DecimalField(max_digits=5, decimal_places=1)
    costusd = models.DecimalField(max_digits=5, decimal_places=1)
    user_tag = models.CharField(max_length=200)


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

class follow_modle(models.Model):
    follower =  models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='follower')
    followed = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='followed')


