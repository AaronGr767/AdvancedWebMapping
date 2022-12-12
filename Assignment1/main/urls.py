from django.urls import path
from . import views, templates
from django.views.generic.base import TemplateView

# from .views import UserDetailAPI, RegisterUserAPIView

app_name = "main"


urlpatterns = [
    path('login', views.login_request, name="login"),
    path('registration', views.register_request, name="registration"),
    # path("get-details",UserDetailAPI.as_view()),
    # path('register',RegisterUserAPIView.as_view()),
    path('map', TemplateView.as_view(template_name="userMap.html"), name="map"),
    path('home', TemplateView.as_view(template_name="home.html"), name="home"),
    path('logout', views.logout_request, name="logout"),
    path('updatedb/', views.update_database, name='update_db'),
    path('nearbyattract/', views.nearby_attractions, name="nearby_attractions"),
    path('savedmap', TemplateView.as_view(template_name="savedMap.html"), name="savedmap"),
    path('savedview/', views.view_saved, name="view_saved")
]