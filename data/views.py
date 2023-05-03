from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegistrationForm
from data.utilities import update_context
from django.contrib import messages


# Create your views here.
def register(request):
    if request.user.is_authenticated:
        return redirect("/")
    
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"New account created: {user.username}")
            return redirect('/')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    else:
        form = UserRegistrationForm()
      
    context = {
        "form": form
    }  
    return render(request, "register.html", update_context(context))            
                