from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>/', views.spaceDetail, name='space_detail'),
    path('info/', views.info, name='info'),
]