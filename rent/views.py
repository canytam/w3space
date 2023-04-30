from django.shortcuts import render, redirect
from data.models import Space, Booking, User, Customer, PackageDetails
from data.utilities import update_context, total_coupon
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest
from django.urls import reverse
import json
import datetime

# Create your views here.
@login_required
def spaceDetail(request, pk):
    space = Space.objects.get(pk=int(pk))
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == "POST":
            data = json.load(request)
            selectedDate = data.get('selectedDate')
            customer = Customer.objects.get(user=request.user)
            for date in selectedDate:
                booking = Booking(space=space, customer=customer, date=date)
                booking.save()
            #bookings = Booking.objects.filter(space=space)
            #return JsonResponse({'bookings': bookings}, status=200)
            print(reverse('info'))
            response_data = {
                "redirect_url": reverse("info")
            }
            print(response_data)
            return JsonResponse({}, status=200)
        return JsonResponse({}, status=400)
    bookings = Booking.objects.filter(space=space)
    context = {
        'space': space,
        'today': datetime.date.today(),
        'endday': datetime.date.today()+datetime.timedelta(days=90),
        'bookings': bookings,
    }
    return render(request, "space_detail.html", update_context(context))

@login_required
def info(request):
    customer = Customer.objects.get(user=request.user)
    packageDetails = PackageDetails.objects.filter(customer=customer, coupon__gt=0)
    bookings = Booking.objects.filter(customer=customer)
    context = {
        'customer': customer,
        'packageDetails': packageDetails,
        'bookings': bookings,
        'coupon': total_coupon(customer),
    }
    return render(request, "info.html", update_context(context))
