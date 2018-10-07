from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.http import require_http_methods
from .models import *
from .views_api import getContext
import json, requests, time, datetime
# 아임포트 라이브러리
from iamport import Iamport

# Rest Framework
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
# 아임포트 API 키
iamport = Iamport(imp_key=settings.IAMPORT_API_KEY, imp_secret=settings.IAMPORT_API_SECRET)

# ------------------------------------------------------------------
# ClassName   : getToken
# Description : 인증토큰 발급
# ------------------------------------------------------------------
def getToken():
    url = "https://api.iamport.kr/users/getToken"
    data = {
        'imp_key': settings.IAMPORT_API_KEY,
        'imp_secret': settings.IAMPORT_API_SECRET
    }
    r = requests.post(url=url, data=data)
    return r.json()

# ------------------------------------------------------------------
# ClassName   : getReservation
# Description : 인증토큰 발급
# ------------------------------------------------------------------
def getReservation(unix_time):
    url = "https://api.iamport.kr/subscribe/payments/schedule"
    data = {
        'imp_key': settings.IAMPORT_API_KEY,
        'imp_secret': settings.IAMPORT_API_SECRET
    }
    r = requests.post(url=url, data=data)
    return r.json()

# ------------------------------------------------------------------
# ClassName   : PaymentAPI
# Description : 결제 API
# ------------------------------------------------------------------
@require_http_methods(["POST"])
def PaymentAPI(request):
    name = request.POST.get('name', None)
    url = request.POST.get('url', None)
    profile = UserProfile.objects.get(user=request.user)
    try:
        site = Site.objects.get(user=request.user, url=url, status='ready')
        site.name = name
        site.save()
    except:
        try:
            site = Site.objects.create(user=request.user, name=name, url=url)
        except:
            context = getContext("error", "이미 추가된 사이트 입니다.")
            return HttpResponse(json.dumps(context), content_type="application/json")
    # 결제 로직 구현
    today = datetime.date(datetime.datetime.today().year,datetime.datetime.today().month,datetime.datetime.today().day)
    unix_time = time.mktime(today.timetuple())
    # 토큰 발급
    token_result = getToken()
    try:
        access_token = token_result['response']['access_token']
    except:
        context = getContext("error", '토큰 발급 실패')
        return HttpResponse(json.dumps(context), content_type="application/json")
    # 결제 진행


    context = getContext("success", "아임포트 결제 진행.")

    return HttpResponse(json.dumps(context), content_type="application/json")

# ------------------------------------------------------------------
# ClassName   : CallbackAPI
# Description : 결제 후 CallbackAPI
# ------------------------------------------------------------------
@api_view(['POST'])
def CallbackAPI(request):
    try:
        imp_uid = request.body.json()["imp_uid"]
    except:
        imp_uid = None
    try:
        imp_uid2 = request.body["imp_uid"]
    except:
        imp_uid2 = None
    context = getContext("success", "성공", {'imp_uid':imp_uid, 'imp_uid2':imp_uid2,})
    # return HttpResponse(json.dumps(context), content_type="application/json")
    return Response(context, status=status.HTTP_201_CREATED)

# ------------------------------------------------------------------
# ClassName   : updateSiteAPI
# Description : 결제 상태 업데이트
# ------------------------------------------------------------------
@require_http_methods(["POST"])
def updateSiteAPI(request):
    merchant_uid = request.POST.get('merchant_uid', None)
    imp_uid = request.POST.get('imp_uid', None)
    status = request.POST.get('status', None)

    site = get_object_or_404(Site, user=request.user, merchant_uid=merchant_uid, status='ready')
    if site:
        site.status = status
        site.imp_uid = imp_uid
        site.save()
        context = getContext("success", "Update database.")
    else:
        context = getContext("error", "Cannot found site data.")
    return HttpResponse(json.dumps(context), content_type="application/json")

# ------------------------------------------------------------------
# ClassName   : getBillingAPI
# Description : 빌링키를 설정하는 API
# ------------------------------------------------------------------
def getBillingAPI(request):
    token_result = getToken()
    try:
        access_token = token_result['response']['access_token']
    except:
        context = getContext("error", '토큰 발급 실패')
        return HttpResponse(json.dumps(context), content_type="application/json")

    card_number = request.POST.get('card_number', None)
    expiry = request.POST.get('expiry', None)
    pwd_2digit = request.POST.get('pwd_2digit', None)
    birth = request.POST.get('birth', None)

    if card_number == '' or expiry == '' or pwd_2digit == '' or birth == '':
        context = getContext("error", "빈칸을 채워주세요.")
    # 빌링키 발급
    else:
        profile = UserProfile.objects.get(user=request.user)
        url = "https://api.iamport.kr/subscribe/customers/" + str(profile.customer_uid)
        headers = {"Authorization": access_token}
        data = {
            'card_number' : card_number,
            'expiry' : expiry,
            'pwd_2digit': pwd_2digit,
            'birth': birth
        }
        r = requests.post(url=url, headers=headers, data=data)
        if r.json()['code']==0:
            context = getContext("success", "빌링키 발급 성공")
            profile.billing = True
            profile.save()
        else:
            context = getContext("error", "빌링키 발급 실패")

    return HttpResponse(json.dumps(context), content_type="application/json")

# ------------------------------------------------------------------
# ClassName   : PaymentAPI
# Description : 빌링키를 설정하는 API
# ------------------------------------------------------------------
# def PaymentAPI(request):
