from django.shortcuts import render, redirect
from data.models import Space, Booking, User, Customer, PackageDetails
from data.utilities import update_context, total_credits
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest
from django.urls import reverse
import json
import datetime

# Create your views here.
# @login_required
def spaceDetail(request, pk):
    space = Space.objects.get(pk=int(pk))
    packages = []
    if request.user.is_authenticated:
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        customer = Customer.objects.get(user=request.user)
        packages = PackageDetails.objects.filter(customer=customer, credits__gt=0)
        if is_ajax:
            if request.method == "POST":
                data = json.load(request)
                selectedDate = data.get('selectedDate')
                for date in selectedDate:
                    booking = Booking(space=space, customer=customer, date=date)
                    booking.save()
                credit = len(selectedDate) * space.credits
                for package in packages:
                    if (credit > package.credits):
                        credit -= package.credits
                        package.credits = 0
                        package.save()
                    else:
                        package.credits -= credit
                        package.save()
                        break
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
        'packages': packages,
    }
    return render(request, "space_detail.html", update_context(context))

@login_required
def info(request):
    customer = Customer.objects.get(user=request.user)
    packageDetails = PackageDetails.objects.filter(customer=customer, credits__gt=0)
    bookings = Booking.objects.filter(customer=customer)
    context = {
        'customer': customer,
        'packageDetails': packageDetails,
        'bookings': bookings,
        'credits': total_credits(customer),
    }
    return render(request, "info.html", update_context(context))
