from django.shortcuts import render, redirect
from django.db.models import Count
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.contrib.auth import get_user_model
from data.models import Space, Package, Customer, Booking, SubscribedUsers
from data.utilities import update_context

#Create your views here.

def about(request):
    spaces = Space.objects.all().values()
    packages = Package.objects.all().values()
    customers = Customer.objects.all()
    city = Space.objects.all().values('city').distinct().count()
    repeatedCustomers = Booking.objects.values('customer').annotate(bookingCount=Count('customer')).filter(bookingCount__gt=1)
    context = {
        'spaces': spaces,
        'packages': packages,
        'customers': customers,
        'city': city,
        'repeatedCustomers': repeatedCustomers,
    }
    return render (request, "about.html", update_context(context))

def subscribe(request):
    if request.method == 'POST':
        #name = request.POST.get('name', None)
        email = request.POST.get('email', None)
        
        #if not name or not email:
        if not email:
            messages.error(request, "You must type legit name and email to subscribe to a Newsletter.")
            return redirect("/")
        
        if get_user_model().objects.filter(email=email).first():
            messages.error(request, f"Found registered user with associated {email} email.")
            return redirect(request.META.get("HTTP_REFERER", "/"))
        subscribe_user = SubscribedUsers.objects.filter(email=email).first()
        if subscribe_user:
            messages.error(request, f"{email} email address is already subscriber.")
            return redirect(request.META.get("HTTP_REFERER", "/"))
        
        try:
            validate_email(email)
        except ValidationError as e:
            messages.error(request, e.messages[0])
            return redirect("/")
        
        subscribe_model_instance = SubscribedUsers()
        #subscribe_model_instance.name = name
        subscribe_model_instance.email = email
        subscribe_model_instance.save()
        messages.success(request, f'{email} email was successfully subscribed to our newsletter!')
        return redirect(request.META.get("HTTP_REFERER", "/"))
        