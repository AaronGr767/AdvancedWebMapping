from django.urls import path
from . import views, templates
from django.views.generic.base import TemplateView

app_name = "main"


urlpatterns = [
    path('login', views.login_request, name="login"),
    path('registration', views.register_request, name="registration"),
    path('map', TemplateView.as_view(template_name="userMap.html"), name="map"),
    path('', TemplateView.as_view(template_name="home.html"), name="home"),
    path('logout', views.logout_request, name="logout"),
    path('updatedb/', views.update_database, name='update_db')
]