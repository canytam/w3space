from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader
from django.urls import reverse
from data.models import Company, Package, Customer, PackageDetails, Space
from .forms import SpaceSearchForm
import datetime
from data.utilities import total_coupon, update_context

# Create your views here.
def space_search(request):
    if request.method == 'POST':
        form = SpaceSearchForm(request.POST)
        if form.is_valid():
            # Get the search criteria from the form
            location = form.cleaned_data.get('location')
            #amenities = form.cleaned_data.get('amenities')
            min_price = form.cleaned_data.get('min_price')
            max_price = form.cleaned_data.get('max_price')
            package_id = form.cleaned_data.get('purchased_package')
            
            # Build the query based on the search criteria
            spaces = Space.objects.filter(package_id=package_id)
            if location:
                spaces = spaces.filter(location__icontains=location)
            #if amenities:
                #for amenity in amenities:
                    #spaces = spaces.filter(amenities__icontains=amenity)
            if min_price:
                spaces = spaces.filter(price__gte=min_price)
            if max_price:
                spaces = spaces.filter(price__lte=max_price)
            
            # Render the search results to the user
            return render(request, 'space_search_results.html', {'spaces': spaces})
    else:
        form = SpaceSearchForm()
    context = {
        'form': form
    }
    return render(request, 'space_search.html', update_context(context))
