from django.urls import path
from . import views, templates

app_name = "main"


urlpatterns = [
    path('', views.login_request, name="login"),
    path('register', views.register_request, name="register"),
    path('map', views.userMap, name="map")
]