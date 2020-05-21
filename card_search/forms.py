from django import forms
from home.models import cards




COLOR_CHOICES = [
    ('Red', 'Red'),
    ('Blue', 'Blue'),
    ('Green', 'Green'),
    ('Black', 'Black'),
    ('White', 'White'),
    ('Colorless', 'Colorless')
]

NUMS = [
    ('<', '<'),
    ('>', '>'),
    ('=', '=')
]

LEGAL = [
    ('all', "All"),
    ('standard', 'Standard'),
    ('brawl', 'Brawl'),
    ('pioneer', 'Pioneer'),
    ('historic', 'Historic'),
    ('modern', 'Modern'),
    ('pauper', 'Paupe'),
    ('legacy', 'Legacy'),
    ('penny', 'Penny'),
    ('vintage', 'Vintage'),
    ('commander', 'Commander'),
]

ANDOR = [
    ('and', 'And'),
    ('or', 'Or')
]


class card_searchform(forms.Form):
    name = forms.CharField(required= False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    cost = forms.CharField(required= False,  widget=forms.TextInput(attrs={'class': 'form-control'}))
    cmc =  forms.DecimalField(required= False,  widget=forms.TextInput(attrs={'class': 'form-control'}))
    cmc_op = forms.ChoiceField(required= False, widget=forms.RadioSelect, choices=NUMS)
    color = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=COLOR_CHOICES,
    )
    color_op = forms.ChoiceField(required=False, widget=forms.RadioSelect, choices=ANDOR )
    card_type =  forms.CharField(required= False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    sub_type =  forms.CharField(required= False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    super_type =  forms.CharField(required= False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    rules_text =  forms.CharField(required= False, widget=forms.Textarea(attrs={'class': 'form-control'}))
    flavor_text = forms.CharField(required= False, widget=forms.Textarea(attrs={'class': 'form-control'}))
    power = forms.DecimalField(required= False,  widget=forms.TextInput(attrs={'class': 'form-control'}))
    power_op = forms.ChoiceField(required= False, widget=forms.RadioSelect, choices=NUMS)
    toughness = forms.DecimalField(required= False,  widget=forms.TextInput(attrs={'class': 'form-control'}))
    toughness_op = forms.ChoiceField(required= False, widget=forms.RadioSelect, choices=NUMS)
    leagl = forms.ChoiceField(required= False, widget=forms.Select, choices=LEGAL)
    price = forms.DecimalField(required= False,  widget=forms.TextInput(attrs={'class': 'form-control'}))
    price_op = forms.ChoiceField(required= False, widget=forms.RadioSelect, choices=NUMS)
    keyword = forms.ChoiceField(required= False, widget=forms.Select, choices=LEGAL)

def search_function(form):
    name = form.cleaned_data.get('name')
    cost = form.cleaned_data.get('cost')
    cmc = form.cleaned_data.get('cmc')
    cmc_op = form.cleaned_data.get('cmc_op')
    color = form.cleaned_data.get('color')
    color_op = form.cleaned_data.get('color_op')
    card_type = form.cleaned_data.get('card_type')
    sub_type = form.cleaned_data.get('sub_type')
    super_type = form.cleaned_data.get('super_type')
    rules_text = form.cleaned_data.get('rules_text')
    flavor_text = form.cleaned_data.get('flavor_text')
    power = form.cleaned_data.get('power')
    power_op = form.cleaned_data.get('power_op')
    toughness = form.cleaned_data.get('toughness')
    toughness_op = form.cleaned_data.get('toughness_op')
    #legal = form.cleaned_data.get('legal')
    price = form.cleaned_data.get('price')
    price_op = form.cleaned_data.get('price_op')


    card_list = cards.objects.all()

    if not name == "":
        card_list = card_list.filter(name__icontains=name) 
    #name

    if not cost == "":
        card_list = card_list.filter(cost__iexact=cost) 
    #cost 

    if not cmc == "":
        op = card_list
        if cmc_op == "=":
            op = card_list.filter(cmc__exact=cmc)
        elif cmc_op == ">":
            op = card_list.filter(cmc__gt=cmc)
        elif cmc_op == "<":
            op = card_list.filter(cmc__lt=cmc)

        card_list = op
    #cmc

    if 'Blue' in color or 'Red' in color or 'Green' in color or 'Black' in color or 'White' in color or 'Colorless' in color:

        if color_op == 'and':
            card_list = card_list.filter(color__exact=color) 
    # needs work color        
    
    if not card_type == "":
        card_list = card_list.filter(type1__iexact=card_type)
    #type 

    if not sub_type == "":
        card_list = card_list.filter(sub_type__iexact=sub_type)
    #sub type

    if not super_type == "":
        card_list = card_list.filter(super_type__iexact=super_type)
    #super type

    if not rules_text == "":
        card_list = card_list.filter(rules_text__icontains=rules_text)
    #rules text

    if not flavor_text == "":
        card_list = card_list.filter(flavor_text__icontains=flavor_text)
    #flavor text

    if not power == "":
        op = card_list
        if power_op == "=":
            op = card_list.filter(power__exact=power)
        elif power_op == ">":
            op = card_list.filter(power__gt=power)
        elif power_op == "<":
            op = card_list.filter(power__lt=power)
        card_list = op
    #power

    if not toughness == "":
        op = card_list
        if toughness_op == "=":
            op = card_list.filter(toughness__exact=toughness)
        elif toughness_op == ">":
            op = card_list.filter(toughness__gt=toughness)
        elif toughness_op == "<":
            op = card_list.filter(toughness__lt=toughness)

        card_list = op
    #toughness
    
    #if not legal == 'all':
        #card_list = card_list.filter(leagl__exact=legal)
    #legal need to have a legality function

    if not price == "":
        op = card_list
        if price_op == "=":
            op = card_list.filter(price__exact=price)
        elif price_op == ">":
            op = card_list.filter(price__gt=price)
        elif price_op == "<":
            op = card_list.filter(price__lt=price)
    #price

    card_list2 = []
    for i in range(len(card_list)):
        card_list2.append(card_list[i].name)
    

    return(card_list)
