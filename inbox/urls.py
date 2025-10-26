from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='inbox.index'),
    path('compose/<int:id>', views.compose, name='inbox.compose')
]