from django.urls import path
from . import views

urlpatterns = [
    path('p1/', views.p1, name='p1'),
    path('p2/', views.p2, name='p2'),
    path('about/', views.about, name='about2'),
    path('package/', views.package, name='package2'),
]