from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from data.models import Customer

class UserRegistrationForm(UserCreationForm):
    gender = forms.ChoiceField(choices=Customer.GENDER_CHOICES)
    telephone = forms.CharField(max_length=16)
    
    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        
    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=True)
        customer = Customer(
            user=user,
            gender=self.cleaned_data['gender'],
            telephone=self.cleaned_data['telephone'],
            balance=0
        )
        customer.save()
        return user