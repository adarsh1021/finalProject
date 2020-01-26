from django.urls import path
from backend import views
from backend import api_views


app_name="backend"


urlpatterns = [
    # Static pages
    path('test/',views.hello),
    path('login/', views.login),

    # API endpoints
    path('api/sign_up', api_views.sign_up),
    path('api/sign_in', api_views.sign_in),
]
