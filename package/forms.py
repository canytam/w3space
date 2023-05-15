from django import forms
from data.models import Package

class PurchasePackageForm(forms.Form):
    packages = Package.objects.all()
    choice = []
    for package in packages:
        choice.append((package.id, package.name))   
    purchased_package = forms.ChoiceField(choices=choice, label="Package")
    