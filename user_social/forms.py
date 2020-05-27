from django import forms

#tye in another users name here to follow
class follow_form(forms.Form):
    follow = forms.CharField(widget=forms.TextInput)