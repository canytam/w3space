from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader
from django.urls import reverse
from data.models import Company, Package, Customer, PackageDetails, Space, Booking
from data.utilities import update_context
from django.db.models import Q
from django.shortcuts import render
import datetime as dt

# Create your views here.
def space_search(request):
    if request.method == 'POST':
        wkLs = []
        dateRef  = dt.datetime.today()
        for a in range(1,11):
            aday = dateRef + dt.timedelta(days= a)
            y = aday.month*100 +aday.day
            wkLs.append(y)
    
        bkDyLs = {}
        spaces = Space.objects.all()
        for i in range(9):
            avDy =[]
            rmLs = spaces[i].booking_set.all()
        
            rmDyLs =[]
            for rmDy in rmLs:
                z = rmDy.date.month*100 + rmDy.date.day
                rmDyLs.append(z)
    
            for wkDy in wkLs:
                if wkDy not in rmDyLs:
                    wkDyStr = str(wkDy - int(wkDy/100)*100) + "/" + str(int(wkDy/100))
                    avDy.append(wkDyStr)
                                   
            bkDyLs[i+1]=avDy
        
        sp_cat =  request.POST['sp_cat']
        address = request.POST['address']
        size = request.POST['size']
        with_cof = request.POST['with_cof']
        #with_nbk = request.POST['with_nbk']
        spaces = Space.objects.filter(Q(name__icontains=sp_cat) &Q(address__icontains=address) 
                                      &Q(size__icontains=size) &Q(has_coffeemaker=with_cof))

        context = {
            'space': spaces,
            'bookLs' : bkDyLs,
            }

        return render(request, 'space_search_result.html', update_context(context))
    else:
        context = {
        }
        return render(request, 'space_search.html', update_context(context))


