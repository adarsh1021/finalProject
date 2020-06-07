from django.urls import path
from stubapi import views


app_name = "stubapi"


urlpatterns = [
    path("sm1/", views.sm1),
    path("sm2/", views.sm2),
    path("facebook/", views.facebook),
    path("facebook/api/", views.facebook_api.as_view()),
]
