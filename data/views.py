from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegistrationForm
from data.utilities import update_context
from django.contrib import messages
from django.views.generic.base import TemplateView
from django.conf import settings
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import stripe

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
  
class stripeView(TemplateView):
    template_name = 'stripe.html'
'''    
@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)
    
@csrf_exempt
def create_checkout_session(request):
    if request.method == 'GET':
        domain_url = 'http://localhost:8000/accounts/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            checkout_session = stripe.checkout.Session.create(
                success_url = domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url = domain_url + 'cancelled/',
                payment_method_types = ['card'],
                mode = 'payment',
                line_items = [
                    {
                        'price_data': {
                            'currency': 'hkd',
                            'unit_amount': 1000,
                            'product_data': {
                                'name': 'Deposit',                                
                            },
                        },
                        'quantity': 1,
                    },
                ],
            ),
            return JsonResponse({'id': checkout_session.id})
        except Exception as e:
            return JsonResponse({'error': str(e)})
            '''