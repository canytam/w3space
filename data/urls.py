from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('create-checkout-session/<int:pk>/', views.CreateStripeCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('success/', views.successView, name='success'),
    path('cancel/', views.cancelView, name='cancel'),
]