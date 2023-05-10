from django.shortcuts import render
from django.db.models import Count
from data.models import Space, Package, Customer, Booking
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
        'package': packages,
        'customers': customers,
        'city': city,
        'repeatedCustomers': repeatedCustomers,
    }
    return render (request, "about.html", update_context(context))

