from django import forms
from data.models import Space

#class SpaceSearchForm(forms.Form):
    
    #location = forms.CharField(max_length=100, required=False)
    #amenities = forms.MultipleChoiceField(choices=AMENITIES_CHOICES, required=False)
    #min_price = forms.DecimalField(decimal_places=2, max_digits=10, required=False)
    #max_price = forms.DecimalField(decimal_places=2, max_digits=10, required=False)
    #purchased_package = forms.ChoiceField(choices=choice)

#class SpaceSearchForm(forms.Form):
    #location = Space.objects.all()
    #choice = []
    #a_address = " "
    #for i in location:
        #print('i', i.address)
        #if a_address != i.address:
            #print('hi')
            #choice.append((i.id, i.address))
            #a_address = i.address 
    #print(choice)
    #location = forms.ChoiceField(choices=choice)
 

