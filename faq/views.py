from django.shortcuts import render
from data.utilities import update_context
from data.models import Company, Faq

# Create your views here.
def index(request):
    faq = Faq.objects.all()
    context ={'faq': faq}
    return render(request, "faq.html", update_context(context))