from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),  # maps "/" to the home view
]
