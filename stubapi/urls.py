from django.urls import path
from stubapi import views


app_name = "backend"


urlpatterns = [path("sm1/", views.sm1), path("sm2/", views.sm2)]
