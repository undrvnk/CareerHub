from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='jobs.index'),
    path('create/', views.create, name='jobs.create'),
    path('applications/', views.applications, name='jobs.applications'),
    path('recommendations/', views.recommendations, name='jobs.recommendations'),
    path('<int:job_id>/', views.detail, name='jobs.detail'),
    path('<int:job_id>/edit/', views.edit, name='jobs.edit'),
    path('<int:job_id>/delete/', views.delete, name='jobs.delete'),
]