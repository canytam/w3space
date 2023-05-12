from django.urls import path, reverse_lazy
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('create-checkout-session/<int:pk>/', views.CreateStripeCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('success/', views.successView, name='success'),
    path('cancel/', views.cancelView, name='cancel'),
    path('userlogin/', views.custom_login, name='userlogin'),
    path('userlogin/', views.custom_login, name='login'),
    path('password-reset', views.MyPasswordResetView.as_view(), name="password-reset"),
    path('password-reset/done/', views.MyPasswordResetDoneView.as_view(), name="password_reset_done"),
    path('password-reset-confirm/<uidb64>/<token>/', views.MyPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset-complete/', views.MyPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('password-change/', views.MyPasswordChangeView.as_view(template_name="registration/password_change.html", success_url='/rent/info/'), name='password-change'),
    path('password_change/done/', views.MyPasswordChangeDoneView.as_view(), name='password_change_done'),
]