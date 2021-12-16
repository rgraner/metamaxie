from django.contrib import admin
from django.urls import path
from scholarships import views


app_name = 'scholarships'

urlpatterns = [
    path('scholarships-table/', views.scholarships_table, name='scholarships_table'),
    path('', views.scholarships, name='scholarships_cards'),
    path('add/', views.add_scholarship, name='add_scholarship'),
    path('edit/<int:scholarship_id>/', views.edit_scholarship, name='edit_scholarship'),
    path('remove/<int:scholarship_id>/', views.remove_scholarship, name='remove_scholarship'),
    path('scholars/', views.scholars, name='scholars'),
    path('disconnect-scholar/<int:scholar_id>/', views.disconnect_scholar, name='disconnect_scholar'),
    path('refresh/', views.refresh, name='refresh'),
]