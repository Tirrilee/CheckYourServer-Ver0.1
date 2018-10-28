from django.urls import path
from .views import MainPage, CallcodeInput

app_name = "App"

urlpatterns = [
    path('', MainPage, name="home"),
    path('create-call-codes/', CallcodeInput, name="call"),

]