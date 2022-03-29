from django.urls import path
from .views import scholarship_list, scholarship


app_name = 'api'

urlpatterns = [
    path('scholarships/', scholarship_list),
    path('<int:ronin_id>/', scholarship),
]