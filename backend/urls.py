from django.urls import path
from backend import views
from backend import api_views


app_name = "backend"


urlpatterns = [
    # Static pages
    path("test/", views.hello),
    path("sign_in/", views.sign_in, name="sign_in"),
    path("index/", views.index, name="index"),
    path("sign_out/", views.sign_out, name="sign_out"),
    path("sign_up/", views.sign_up, name="sign_up"),
    # API endpoints
    path("api/sign_up", api_views.sign_up),
    path("api/sign_in", api_views.sign_in),
]
