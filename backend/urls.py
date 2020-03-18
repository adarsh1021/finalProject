from django.urls import path
from backend import views
from backend import api_views


app_name = "backend"


urlpatterns = [
    # Static pages
    path("test/", views.hello),
    path("sign_in/", views.sign_in, name="sign_in"),
    path("sign_out/", views.sign_out, name="sign_out"),
    path("sign_up/", views.sign_up, name="sign_up"),
    path("index/", views.index, name="index"),
    path("table_display/", views.table_disp, name="table_display"),
    path("dataCollection/", views.dataCollection, name="dataCollection"),
    path(
        "createCustomTable/", views.createCustomTable, name="createCustomTable"
    ),
    path("analytics/", views.analytics, name="analytics"),
    path("analytics/<int:customTableId>", views.analytics, name="analytics"),
    # API endpoints
    path("api/sign_up", api_views.sign_up),
    path("api/sign_in", api_views.sign_in),
    path("api/create_campaign", api_views.create_campaign),
    path("api/create_custom_table", api_views.create_custom_table),
    path("api/analytics", api_views.analytics),
]
