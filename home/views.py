from django.shortcuts import render
from data.models import Space, Company, Booking
from data.utilities import update_context
import datetime as dt

# Create your views here.
def index(request):
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
                wkDyStr =  str(wkDy - int(wkDy/100)*100) + "/" + str(int(wkDy/100))
                avDy.append(wkDyStr)
                                   
        #bkDyLs[i+1]=avDy
        bkDyLs[spaces[i].id]=avDy
        
    print(bkDyLs)   
    context = {
        'space': spaces,
        'bookLs' : bkDyLs,
    }
    return render (request, "home.html", update_context(context))



