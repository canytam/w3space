from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from data.models import Customer
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox

class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
       
    username = forms.CharField(max_length=100, required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control form-control-lg', 'placeholder': 'Username'}
        ),
        label="Username"
    )
    
    password = forms.CharField(max_length=50, required=True,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control form-control-lg', 'placeholder': 'Password', 'data-toggle': 'password', 'id': 'password', 'name': 'password'}
        ),
        label='password'
    )
    
    remember_me = forms.BooleanField(required=False,
        widget=forms.CheckboxInput(
            attrs={'class': 'form-check-input', 'checked': "True"}
        )                
    )
    
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox(), required=True)
    
    
class UserRegistrationForm(UserCreationForm):
    terms = forms.BooleanField(required=True,
        widget=forms.CheckboxInput(
            attrs={'taxindex': '9'}
        )
    )
    gender = forms.ChoiceField(choices=Customer.GENDER_CHOICES,
        widget=forms.Select(
            attrs={'tabindex': '8'}
        )
    )
    telephone = forms.CharField(max_length=16,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'tabindex': '6', 'placeholder': 'Telephone Number'}
        )
    )
    username = forms.CharField(required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'tabindex': '1', 'placeholder': 'Username'}
        )
    )
    first_name = forms.CharField(required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'tabindex': '2', 'placeholder': 'First Name'}
        )
    )
    last_name = forms.CharField(required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'tabindex': '3', 'placeholder': 'Last Name'}
        )
    )
    email = forms.EmailField(required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'tabindex': '7', 'placeholder': 'Email Address'}
        )
    )
    password1 = forms.CharField(required=True,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'tabindex': '4', 'placeholder': 'Password'}
        )
    )
    password2 = forms.CharField(required=True,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'tabindex': '5', 'placeholder': 'Password Again'}
        )
    )

    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox(), required=True)
   
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