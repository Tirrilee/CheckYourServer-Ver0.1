from django.urls import path
from .views_api import (
    SMSValidate,
    getNation,
    SignupAPI, SigninAPI
)
from .views_payment_api import getMerchantUid, updateSiteAPI

app_name = "API"
urlpatterns = [
    path('', SMSValidate, name="sms-validation"),
    path('merchant-uid', getMerchantUid, name="merchant_uid"),
    path('site-update', updateSiteAPI, name="site_update"),

    path('nations/', getNation, name="nation"),

    path('signin/', SigninAPI, name="signin"),
    path('signup/', SignupAPI, name="signup"),
]