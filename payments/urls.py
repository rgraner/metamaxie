from django.urls import path
from . import views


app_name = 'payments'

urlpatterns = [
    path('', views.payment_view, name='payments'),
    path('scholar-table/', views.scholar_table, name='scholar_table'),
]