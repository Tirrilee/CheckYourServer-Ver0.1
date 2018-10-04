from django.urls import path
from .views import MainPage

app_name = "App"
urlpatterns = [
    path('', MainPage, name="home"),
]