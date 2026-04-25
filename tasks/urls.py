from django.urls import path
from . import views

urlpatterns = [
    path('', views.plan_list, name='plan_list'),
    path('create/', views.plan_create, name='plan_create'),
    path('<int:plan_id>/', views.plan_detail, name='plan_detail'),
    path('task/<int:task_id>/toggle/', views.task_toggle_status, name='task_toggle_status'),
]