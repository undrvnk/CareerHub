# profiles/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('view/', views.view_profile, name='profiles.view'),
    path('edit/', views.edit_profile, name='profiles.edit'),
]