from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('stripe/', views.stripeView.as_view(), name='stripe'),
    #path('config/', views.stripe_config),
    #path('create-checkout-session/', views.create_checkout_session),
]