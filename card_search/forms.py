from django import forms
from home.models import cards


#this whole file deals with user input in the card search page and retuens a list of cards that fit that spesfic criterial 

COLOR_CHOICES = [
    ('R', 'Red'),
    ('U', 'Blue'),
    ('G', 'Green'),
    ('B', 'Black'),
    ('W', 'White'),
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
    ('modern', 'Modern'),
    ('pauper', 'Pauper'),
    ('legacy', 'Legacy'),
    ('penny', 'Penny'),
    ('vintage', 'Vintage'),
    ('commander', 'Commander'),
    ('dule', 'Dule'),
    ('future', 'Future'),
    ('frontier', 'Frontier')
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
    power = forms.DecimalField(required= False,  widget=forms.TextInput(attrs={'class': 'form-control'}))
    power_op = forms.ChoiceField(required= False, widget=forms.RadioSelect, choices=NUMS)
    toughness = forms.DecimalField(required= False,  widget=forms.TextInput(attrs={'class': 'form-control'}))
    toughness_op = forms.ChoiceField(required= False, widget=forms.RadioSelect, choices=NUMS)
    legal = forms.ChoiceField(required= False, widget=forms.Select, choices=LEGAL)
    price = forms.DecimalField(required= False,  widget=forms.TextInput(attrs={'class': 'form-control'}))
    price_op = forms.ChoiceField(required= False, widget=forms.RadioSelect, choices=NUMS)
    keyword = forms.ChoiceField(required= False, widget=forms.Select, choices=LEGAL)



def search_function(send_list):
    cost = send_list[3]
    name = send_list[5]
    cmc = send_list[0]
    cmc_op = send_list[1]
    color = send_list[2]
    #color_op = form.cleaned_data.get('color_op')
    card_type = send_list[14]
    sub_type = send_list[10]
    super_type = send_list[11]
    rules_text = send_list[9]
    power = send_list[6]
    power_op = send_list[7]
    toughness = send_list[12]
    toughness_op = send_list[13]
    legal1 = send_list[4]
    price = send_list[8]
    #price_op = form.cleaned_data.get('price_op')



    card_list = cards.objects.all()

    if not name == "":
        card_list = card_list.filter(name__icontains=name) 
    #name

    if not cost == "":
        card_list = card_list.filter(manaCost__iexact=cost) 
    #cost 

    if not cmc == "":
        op = card_list
        if cmc_op == "=":
            op = card_list.filter(convertedManaCost__exact=cmc)
        elif cmc_op == ">":
            op = card_list.filter(convertedManaCost__gt=cmc)
        elif cmc_op == "<":
            op = card_list.filter(convertedManaCost__lt=cmc)

        card_list = op
    #cmc


    if not card_type == "":
        card_list = card_list.filter(type1__iexact=card_type)
    #type 

    if not sub_type == "":
        card_list = card_list.filter(subtypes__iexact=sub_type)
    #sub type

    if not super_type == "":
        card_list = card_list.filter(supertypes__iexact=super_type)
    #super type

    if not rules_text == "":
        card_list = card_list.filter(rulesText__icontains=rules_text)
    #rules text

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


    if legal1 == 'standard':
        card_list = card_list.filter(legal_standard='Legal')
    elif legal1 == 'brawl':
        card_list = card_list.filter(legal_brawl='Legal')
    elif legal1 == 'pioneer':
        card_list = card_list.filter(legal_pioneer='Legal')
    elif legal1 == 'modern':
        card_list = card_list.filter(legal_modern='Legal')
    elif legal1 == 'pauper':
        card_list = card_list.filter(legal_pauper='Legal')
    elif legal1 == 'legacy':
        card_list = card_list.filter(legal_legacy='Legal')
    elif legal1 == 'penny':
        card_list = card_list.filter(legal_penny='Legal')
    elif legal1 == 'vintage':
        card_list = card_list.filter(legal_vintage='Legal')
    elif legal1 == 'commander':
        card_list = card_list.filter(legal_commander='Legal')
    elif legal1 == 'dule':
        card_list = card_list.filter(legal_dule='Legal')
    elif legal1 == 'future':
        card_list = card_list.filter(legal_future='Legal')
    elif legal1 == 'frontier':
        card_list = card_list.filter(legal_frontier='Legal')


    #legal

    if not color == '':
        for i in color:
            card_list = card_list.filter(colors__in=i)

    #color needs work!!!!!!!! only searches for cards that have all colors searched

    return(card_list)
