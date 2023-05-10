from django.shortcuts import render,HttpResponse
from data.utilities import update_context
from data.models import Company, Faq, Contact
from .forms import ContactForm


# Create your views here.
def index(request):
    faq = Faq.objects.all()
    context ={'faq': faq}
    return render(request, "faq.html", update_context(context))

def contact(request): 
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid(): 
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            contact = Contact(
                name=name,
                email=email,
                subject=subject,
                message=message
            )
            contact.save()
            context = { }
            return render(request, 'success.html', update_context(context)) 
    form = ContactForm()
    context = {'form': form}
    return render(request, 'contact.html', update_context(context))