from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegistrationForm
from data.utilities import update_context
from django.contrib import messages
from django.views.generic.base import TemplateView
from django.conf import settings
from django.http.response import JsonResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.urls import reverse_lazy
from django.contrib import messages
from data.models import Customer
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.
def register(request):
    if request.user.is_authenticated:
        return redirect("/")
    
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"New account created: {user.username}")
            return redirect('/')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    else:
        form = UserRegistrationForm()
      
    context = {
        "form": form
    }  
    return render(request, "register.html", update_context(context))            
  
@method_decorator(csrf_exempt, name="dispatch")
class StripeWebhookView(View):
    def post(self, request, format=None):
        payload = request.body
        endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
        sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
        event = None
        
        try:
            event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
        except ValueError as e:
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError as e:
            return HttpResponse(status=400)
        
        if event["type"] == "checkout.session.completed":
            print("Payment successful")
            session = event["data"]["object"]
            customer_id = session["metadata"]["customer_id"]
            customer = Customer.objects.get(id=customer_id)
            customer.balance += 1000
            customer.save()
        
        return HttpResponse(status=200)
    
class CreateStripeCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        customer = Customer.objects.get(id=self.kwargs["pk"])
        checkout_session = stripe.checkout.Session.create(
            success_url = settings.PAYMENT_SUCCESS_URL,
            cancel_url = settings.PAYMENT_CANCEL_URL,
            payment_method_types = ['card'],
            mode = 'payment',
            metadata = {"customer_id": customer.id},
            line_items = [
                {
                    'price_data': {
                        'currency': 'hkd',
                        'unit_amount': 100000,
                        'product_data': {
                            'name': 'Deposit',                                
                        },
                    },
                    'quantity': 1,
                },
            ],
        ),
        return redirect(checkout_session[0].url)

def successView(request):
    messages.info(request, 'Transcation completed.')
    return redirect(reverse_lazy('info'))
        
def cancelView(request):
    messages.error(request, 'Transcation cancelled.')
    return redirect(reverse_lazy('info'))