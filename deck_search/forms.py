from django import forms

class add_deck(forms.Form):
    deck_name = forms.CharField(widget=forms.TextInput())



class publish_deck(forms.Form):
    deck_discription = forms.CharField(widget=forms.Textarea())
    hash_tags = forms.CharField(widget=forms.TextInput())

class deck_searchform(forms.Form):
    hash_tags = forms.CharField(widget=forms.TextInput)