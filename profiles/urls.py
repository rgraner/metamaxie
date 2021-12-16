from django.urls import path
from . import views


app_name = 'profiles'

urlpatterns = [
    path('edit/', views.edit_profile, name='edit_profile'),
    path('my/', views.my_profile, name='my_profile'),
    path('rules/', views.rules, name='rules'),
]