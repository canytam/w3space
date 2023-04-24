from django.shortcuts import render
from data.models import Space, Booking, User, Customer
from data.utilities import update_context
from django.contrib import messages
import datetime

# Create your views here.
def spaceDetail(request, pk):
    space = Space.objects.get(pk=int(pk))
    bookings = Booking.objects.filter(space=space)
    for booking in bookings:
        messages.info(request, booking.date)
    context = {
        'space': space,
        'today': datetime.date.today(),
        'endday': datetime.date.today()+datetime.timedelta(days=90),
        'bookings': bookings,
    }
    return render(request, "space_detail.html", update_context(context))
