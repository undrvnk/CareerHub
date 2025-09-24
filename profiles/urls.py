from django.urls import path
from . import views

urlpatterns = [
    path('view/', views.view, name='profiles.view'),
    path('edit/', views.edit, name='profiles.edit'),
]