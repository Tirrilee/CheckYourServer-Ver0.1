from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.http import require_http_methods
from .models import *
from .views_api import getContext
import json, requests, time, datetime
from dateutil.relativedelta import relativedelta
# 아임포트 라이브러리
from iamport import Iamport

# Rest Framework
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
# 아임포트 API 키
# iamport = Iamport(imp_key=settings.IAMPORT_API_KEY, imp_secret=settings.IAMPORT_API_SECRET)

amount = 1000
# ------------------------------------------------------------------
# ClassName   : getUnixTime
# Description : 당일날로부터 한달 뒤의 UnixTime 가져오기
# ------------------------------------------------------------------
def getUnixTime():
    # next_month = datetime.datetime.now() + relativedelta(months=1)
    next_month = datetime.datetime.now() + relativedelta(minutes=1)
    unix_time = time.mktime(next_month.timetuple())
    return unix_time

# ------------------------------------------------------------------
# ClassName   : getClientIP
# Description : 클라이언트 IP 가져오기
# ------------------------------------------------------------------
def getClientIP(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
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
# Description : 결제예약
# ------------------------------------------------------------------
def getReservation(site, user, unix_time, access_token):
    order = Order.objects.create(user=user, site=site, status='reservation')
    url = "https://api.iamport.kr/subscribe/payments/schedule"
    headers = {
        "Authorization": access_token,
        "Content-Type": "application/json"
    }
    schedules = [
        {
            'merchant_uid': str(order.merchant_uid),
            'schedule_at': unix_time,
            'amount': amount,
            'name': 'CheckYourSite 월간 사용료 정기결제',
            'buyer_email': str(order.user),
            'buyer_tel': str(order.user.userprofile.phone)
        }
    ]
    data = {
        'customer_uid': str(user.userprofile.customer_uid),
        'schedules': schedules
    }
    print(data)
    r = requests.post(url=url, headers=headers, data=json.dumps(data))
    return r.json()

# ------------------------------------------------------------------
# ClassName   : getPayment
# Description : 결제
# ------------------------------------------------------------------
def getPayment(order, customer_uid, access_token):
    url = "https://api.iamport.kr/subscribe/payments/again"
    headers = {"Authorization": access_token}
    data = {
        'customer_uid': str(customer_uid),
        'merchant_uid': str(order.merchant_uid),
        'amount': amount,
        'name': 'CheckYourSite 월간 사용료 정기결제',
        'buyer_email': str(order.user),
        'buyer_tel': str(order.user.userprofile.phone)
    }
    print(type(data))
    r = requests.post(url=url, headers=headers, data=data)
    return r.json()

# ------------------------------------------------------------------
# ClassName   : getPaymentData
# Description : 결제정보 가져오기
# ------------------------------------------------------------------
def getPaymentData(imp_uid, access_token):
    url = "https://api.iamport.kr/payments/"+imp_uid
    headers = {"Authorization": access_token}
    r = requests.get(url=url, headers=headers)
    return r.json()

# ------------------------------------------------------------------
# ClassName   : PaymentAPI
# Description : 결제 API
# ------------------------------------------------------------------
@require_http_methods(["POST"])
def PaymentAPI(request):
    name = request.POST.get('name', None)
    url = request.POST.get('url', None)
    user = request.user

    # 사이트가 이미 등록되어 있을 경우
    # 결제 상태 확인 후 결제가 안되어 있을 경우 결제 및 예약 진행 or 이미 결제 된 상품 request
    try:
        site = Site.objects.get(user=user, url=url)
        site.name = name
        site.save()
    # 사이트가 등록이 안되어 있을 경우 생성
    except:
        try:
            site = Site.objects.create(user=user, name=name, url=url)
        except:
            context = getContext("error", "이미 추가된 사이트 입니다.")
            return HttpResponse(json.dumps(context), content_type="application/json")
    # 토큰 발급
    access_token = getToken()['response']['access_token']
    # 결제 진행
    # 마지막 결제 상태가 "예약상태"가 아닐 경우 해당 결제를 가져와서 결제 진행
    last_order = Order.objects.filter(user=user, site=site).last()
    if last_order!=None:
        print("주문 정보가 있습니다.")
        # 결제 예약 상태 일 경우 에러 return
        if last_order.status=='reservation':
            context = getContext('error', "이미 결제예약이 등록된 주문입니다.")
            return HttpResponse(json.dumps(context), content_type="application/json")
        # 결제 상태일 경우..?
        elif last_order.status=='paid':
            print("이미 결제된 상품입니다. 새로운 주문을 생성합니다.")
            order = Order.objects.create(user=user, site=site)
        # 그 외...
        else:
            print("미결제 주문이 있습니다.")
            order = last_order
    else:
        print("주문 정보가 없습니다. 새로운 주문을 생성합니다.")
        order = Order.objects.create(user=user, site=site)


    result = getPayment(order, user.userprofile.customer_uid, access_token)
    if result["code"]==0:
        print(result["response"])
        order.imp_uid = result["response"]["imp_uid"]
        order.status = result["response"]["status"]
        order.save()
        ########################################################################
        # 예약 진행
        # site, customer_uid, unix_time, access_token
        # 예약 객체 생성
        result = getReservation(site, user, int(getUnixTime()), access_token)
        print(result)
        context = getContext("success", "아임포트 결제 및 예약 진행.", {"result": result})
    else:
        context = getContext("error", "아임포트 결제 실패.", {"result": result})
    return HttpResponse(json.dumps(context), content_type="application/json")

# ------------------------------------------------------------------
# ClassName   : updateSiteAPI
# Description : 결제 상태 업데이트
# ------------------------------------------------------------------
@require_http_methods(["POST"])
def updateSiteAPI(request):
    merchant_uid = request.POST.get('merchant_uid', None)
    imp_uid = request.POST.get('imp_uid', None)
    status = request.POST.get('status', None)

    order = get_object_or_404(Order, user=request.user, merchant_uid=merchant_uid, status='ready')
    if order:
        order.status = status
        order.imp_uid = imp_uid
        order.save()
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
# ClassName   : CallbackAPI
# Description : 결제 후 CallbackAPI
# ------------------------------------------------------------------
@api_view(['POST'])
def CallbackAPI(request):
    print("콜백 URL 접근")
    # 아임포트 IP만 접속가능하도록
    client_ip = getClientIP(request)
    print(client_ip)
    if not (client_ip != "52.78.100.19" or client_ip != "52.78.48.223"):
        context = getContext("error", "잘못된 접근입니다.", {"ip":client_ip})
        return Response(context)

    imp_uid = json.loads(request.body)["imp_uid"]
    merchant_uid = json.loads(request.body)["merchant_uid"]
    status = json.loads(request.body)["status"]
    # 상태 업데이트
    try:
        order = Order.objects.get(merchant_uid=merchant_uid)
        order.status=status
        order.save()
    except:
        context = getContext("error", "주문정보가 없습니다.")
        return Response(context)
    # 결제정보 가져오기
    access_token = getToken()['response']['access_token']
    payment_data = getPaymentData(imp_uid, access_token)
    # 예약하기
    if str(payment_data['response']['status'])=="paid":
        # 결제 확인 후 데이터 생성..
        print(str(payment_data['response']))
        # 새로운 예약 결제
        result = getReservation(order.site, order.user, int(getUnixTime()), access_token)
        context = getContext("success", "아임포트 결제 및 예약 진행.", {"result": result})
    # 해당 정보로 결제 재시도
    else:
        context = getContext("error", "예약 결제 실패.")
    return Response(context)