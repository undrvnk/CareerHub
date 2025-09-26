from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='recruiters.index'),
    path('create/', views.create, name='recruiters.create'),
    #path('applications/', views.applications, name='posts.applications'),
    path('candidates', views.candidates, name='recruiters.candidates'),
    path('<int:id>/post_id/', views.detail, name='recruiters.detail'),
    path('<int:id>/post_id/edit/', views.edit, name='recruiters.edit'),
    path('<int:id>/post_id/delete/', views.delete, name='recruiters.delete'),
    #path("index/", views.index, name="recruiters.index_redirect"),
]