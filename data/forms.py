from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from data.models import Customer
#from captcha.fields import ReCaptchaField
#from captcha.widgets import ReCaptchaV2Checkbox

class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Username or Email'}
        ),
        label="Username or Email*"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Password'}
        )
    )
    #captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())
    
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