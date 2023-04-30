from django.shortcuts import render
from data.models import Space, Company
from data.utilities import update_context

# Create your views here.
def index(request):
    spaces = Space.objects.all()
    context = {
        'space': spaces,
    }
    return render (request, "home.html", update_context(context))



