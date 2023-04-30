from django.urls import path
from . import views

urlpatterns = [
    path('', views.purchase_package, name='purchase_package'),
]