from django.urls import path
from . import views

urlpatterns = [
    path('', views.plan_list, name='plan_list'),
    path('create/', views.plan_create, name='plan_create'),
    path('<int:plan_id>/', views.plan_detail, name='plan_detail'),
    path(
        'task/<int:task_id>/toggle/',
        views.task_toggle_status,
        name='task_toggle_status',
    ),
    path('flashcards/', views.collection_list, name='collection_list'),
    path('flashcards/create/', views.collection_create, name='collection_create'),
    path(
        'flashcards/<int:collection_id>/',
        views.collection_detail,
        name='collection_detail',
    ),
]
