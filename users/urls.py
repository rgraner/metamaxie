from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

from . import views


app_name = 'users'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('change-password/', views.change_password, name='change_password'),
    path('password-reset/', auth_views.PasswordResetView.as_view(
        success_url=reverse_lazy('users:password_reset_done'),
        template_name='users/password_reset.html'
        ), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='users/password_reset_sent.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        success_url=reverse_lazy('users:password_reset_complete'),
        template_name='users/password_reset_form.html'
        ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html'
    ), name='password_reset_complete'),
]

