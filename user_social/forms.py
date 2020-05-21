from django import forms


class follow_form(forms.Form):
    follow = forms.CharField(widget=forms.TextInput)