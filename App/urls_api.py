from django.urls import path
from .views_api import (
    SMSValidate,
    getNation,
    SignupAPI, SigninAPI
)
from .views_payment_api import PaymentAPI, updateSiteAPI, getBillingAPI, CallbackAPI

app_name = "API"
urlpatterns = [
    path('', SMSValidate, name="sms-validation"),
    path('pay', PaymentAPI, name="pay"),
    path('site-update', updateSiteAPI, name="site_update"),
    path('billing', getBillingAPI, name="billing"),

    path('nations/', getNation, name="nation"),

    path('signin/', SigninAPI, name="signin"),
    path('signup/', SignupAPI, name="signup"),

    path('iamport-callback/schedule', CallbackAPI, name="callback"),
]