from django import forms
#from data.models import Package

class SpaceSearchForm(forms.Form):
    
    location = forms.CharField(max_length=100, required=False)
    #amenities = forms.MultipleChoiceField(choices=AMENITIES_CHOICES, required=False)
    min_price = forms.DecimalField(decimal_places=2, max_digits=10, required=False)
    max_price = forms.DecimalField(decimal_places=2, max_digits=10, required=False)
    #purchased_package = forms.ChoiceField(choices=choice)
    


