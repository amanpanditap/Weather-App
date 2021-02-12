from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.index),  #the path for our index view
    path('delete/<city_id>', views.delete, name = 'delete'),
]