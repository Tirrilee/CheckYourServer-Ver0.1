from django.urls import path
from .views_api import SMSValidate, getNation

app_name = "API"
urlpatterns = [
    path('', SMSValidate, name="home"),
    path('nations/', getNation, name="nation")
]