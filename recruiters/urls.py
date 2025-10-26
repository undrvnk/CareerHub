from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='recruiters.index'),
    path('create/', views.create, name='recruiters.create'),
    path('candidates', views.candidates, name='recruiters.candidates'),
    path('recommendations/', views.recommendations, name='recruiters.recommendations'),
    path('<int:id>/edit/', views.edit, name='recruiters.edit'),
    path('<int:id>/delete/', views.delete, name='recruiters.delete'),
    path('<int:id>/detail/', views.detail, name='recruiters.detail'),
    path('move-application/', views.move_application, name='recruiters.move_application'),
    path('email-candidate/', views.email_candidate, name='recruiters.email_candidate'),
    path('save-search/', views.save_search, name='recruiters.save_search'),
    path('delete-search/<int:id>/', views.delete_search, name='recruiters.delete_search'),
]
