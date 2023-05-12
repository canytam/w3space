from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader
from django.urls import reverse
from data.models import Company, Package, Customer, PackageDetails, Space, Booking
from data.utilities import update_context
from django.db.models import Q
from django.shortcuts import render
from django.contrib import messages
import datetime as dt

# Create your views here.
def space_search(request):
    sizes = Space.objects.all().values('size').distinct().order_by('size')
    areas = Space.objects.all().values('area').distinct().order_by('area')
    if request.method == 'POST':
        wkLs = []
        dateRef  = dt.datetime.today()
        for a in range(1,8):
            aday = dateRef + dt.timedelta(days= a)
            y = aday.month*100 +aday.day
            wkLs.append(y)
    
        bkDyLs = {}
        spaces = Space.objects.all()
        for i in range(len(spaces)):
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
                                   
            bkDyLs[spaces[i].id]=avDy
        
        sp_cat =  request.POST['sp_cat']
        address = request.POST['address']
        size = request.POST['size']
        with_cof = request.POST['with_cof']
        with_nb = request.POST['with_nb']
        ##with_nbk = request.POST['with_nbk']
        #spaces = Space.objects.filter(Q(name__icontains=sp_cat) &Q(address__icontains=address) 
        #                              &Q(size__icontains=size) &Q(has_coffeemaker=with_cof))
        spaces = Space.objects.all()
        print("Coffee ", with_cof)
        print(spaces.values())
        if (size != ""):
            spaces = spaces.filter(size=size)
        if (address != ""):
            spaces = spaces.filter(area=address)
        if (with_cof != ""):
            spaces = spaces.filter(has_coffeemaker=with_cof)
        if (with_nb != ""):
            spaces = spaces.filter(has_notebook=with_nb)
        if (sp_cat != ""):
            if (sp_cat == 'Desk'):
                spaces = spaces.filter(is_space=False)
            else:
                spaces = spaces.filter(is_space=True)
        if (len(spaces) == 0):
            messages.error(request, "No matched spaces.")
            
        context = {
            'spaces': spaces,
            'bookLs' : bkDyLs,
            'sizes': sizes,
            'areas': areas,
            }

        return render(request, 'space_search.html', update_context(context))
    else:
        context = {
            'sizes': sizes,
            'areas': areas,
        }
        return render(request, 'space_search.html', update_context(context))


