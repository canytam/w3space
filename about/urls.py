from django.urls import path
from . import views

urlpatterns = [
    path('', views.about, name='about'),
    path('subscribe/', views.subscribe, name='subscribe'),
]

