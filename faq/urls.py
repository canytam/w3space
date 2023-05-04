from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='faq'),
    path('contact/', views.contact, name='contact')
]