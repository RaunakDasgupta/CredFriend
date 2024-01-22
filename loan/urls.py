from django.contrib import admin
from django.urls import path, include
from .views import my_function_view

urlpatterns = [
    path('ingest/', my_function_view),
]