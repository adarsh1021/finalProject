from django.urls import path
from stubapi import views


app_name = "backend"


urlpatterns = [path("facebook/", views.facebook)]
