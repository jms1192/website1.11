from django import forms

#this is where the user types in a deck name to create a new deck 
class add_deck(forms.Form):
    deck_name = forms.CharField(widget=forms.TextInput())


# this is where users put in extra information into there deck so it can be published 
class publish_deck(forms.Form):
    deck_discription = forms.CharField(widget=forms.Textarea())
    hash_tags = forms.CharField(widget=forms.TextInput())

#this is how users search decks baced on hashtags 
class deck_searchform(forms.Form):
    hash_tags = forms.CharField(widget=forms.TextInput)

#this where users input card name an quaitty to add cards to their decks 
class add_card_to_deck(forms.Form):
    card_name = forms.CharField()
    quantity = forms.IntegerField()