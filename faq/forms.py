from django import forms
from data.models import Contact



class ContactForm(forms.ModelForm):
    #name = forms.CharField(required=False)
    #subject = forms.CharField(required=False, widget=forms.Select(choices=select_question_categories))
    #message = forms.CharField(max_length=3000)

    class Meta:
        model = Contact
        fields = '__all__'