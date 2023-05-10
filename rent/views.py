from django.shortcuts import render, redirect
from data.models import Space, Booking, Customer, PackageDetails
from data.utilities import update_context, total_credits
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest
from django.urls import reverse
from django.contrib import messages
from social_django.models import UserSocialAuth
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
    try:
        google_login = customer.user.social_auth.get(provider='google-oauth2')
    except UserSocialAuth.DoesNotExist:
        google_login = None
    try:
        github_login = customer.user.social_auth.get(provider='github')
    except UserSocialAuth.DoesNotExist:
        github_login = None
    context = {
        'customer': customer,
        'packageDetails': packageDetails,
        'bookings': bookings,
        'credits': total_credits(customer),
        'google_login': google_login,
        'github_login': github_login,
    }
    return render(request, "info.html", update_context(context))

def searchSpace(request):
    if request.method == "GET":
        name = request.GET['search_space']
        try:
            space = Space.objects.get(name=name)
            return redirect(reverse('space_detail', kwargs={'pk': space.id}))
        except Space.DoesNotExist:
            messages.error(request, 'No matched space.')
    return redirect(reverse('home'))