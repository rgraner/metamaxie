from django.urls import path
from . import views


app_name = 'tasks'

urlpatterns = [
    path('', views.tasks, name='tasks'),
    path('add-task1a/', views.add_task1a, name='add_task1a'),
    path('add-task1b/', views.add_task1b, name='add_task1b'),
    path('add-task12a/', views.add_task12a, name='add_task12a'),
    path('add-task12b/', views.add_task12b, name='add_task12b'),
    path('add-task123a/', views.add_task123a, name='add_task123a'),
    path('add-task123b/', views.add_task123b, name='add_task123b'),
    path('add-task1234a/', views.add_task1234a, name='add_task1234a'),
    path('edit/<int:name_id>/', views.edit_task, name='edit_task'),
    path('remove/<int:task_id>/', views.remove_task, name='remove_task'),
]