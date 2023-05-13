from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegistrationForm, UserLoginForm
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
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView, PasswordChangeView, PasswordChangeDoneView
from data.models import Customer, Company
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY
unit_amount = 5000

def terms(request):
    context = {        
    }
    return render(request, "termsAndConditions.html", update_context(context))

def cookie(request):
    context = {        
    }
    return render(request, "cookiePreferences.html", update_context(context))

def privacy(request):
    context = {        
    }
    return render(request, "privacyPolicy.html", update_context(context))
    
# Create your views here.
def register(request):
    if request.user.is_authenticated:
        return redirect("/")
    
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, f"New account created: {user.username}")
            return redirect('/')
        else:
            for key, error in list(form.errors.items()):
                messages.error(request, f'{key}: {error}')
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
            session = event["data"]["object"]
            customer_id = session["metadata"]["customer_id"]
            customer = Customer.objects.get(id=customer_id)
            customer.balance += int(session["metadata"]["unit_amount"]) * int(session["metadata"]["quantity"])
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
            metadata = {"customer_id": customer.id, "unit_amount": unit_amount, "quantity": 1},
            line_items = [
                {
                    'price_data': {
                        'currency': 'hkd',
                        'unit_amount': unit_amount*100,
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

def custom_login(request):
    if request.user.is_authenticated:
        return redirect(reverse_lazy('info'))
    
    if request.method == "POST":
        form = UserLoginForm(request=request, data=request.POST)
        if form.is_valid():
            remember_me = form.cleaned_data.get('remember_me')
            if not remember_me:
                request.session.set_expiry(0)
                request.session.modified = True
                
            user = authenticate(
                username = form.cleaned_data['username'],
                password = form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect(reverse_lazy('info'))
        else:
            for key, error in list(form.errors.items()):
                if key == 'captcha' and error[0] == 'This field is required.':
                    messages.error(request, "You must pass the reCAPTCHA test")
                    continue
                messages.error(request, error)
    form = UserLoginForm()
    context = {
        'form': form
    }
    return render(request=request, template_name="registration/login.html", context = update_context(context))

class MyPasswordResetView(PasswordResetView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company = Company.objects.all()[0]
        context['company'] = company
        return context
    
class MyPasswordResetDoneView(PasswordResetDoneView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company = Company.objects.all()[0]
        context['company'] = company
        return context
    
class MyPasswordResetConfirmView(PasswordResetConfirmView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company = Company.objects.all()[0]
        context['company'] = company
        return context
    
class MyPasswordResetCompleteView(PasswordResetCompleteView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company = Company.objects.all()[0]
        context['company'] = company
        return context
    
class MyPasswordChangeView(PasswordChangeView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company = Company.objects.all()[0]
        context['company'] = company
        return context
    
class MyPasswordChangeDoneView(PasswordChangeDoneView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company = Company.objects.all()[0]
        context['company'] = company
        return context