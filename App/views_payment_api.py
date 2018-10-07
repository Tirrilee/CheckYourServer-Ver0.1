from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.http import require_http_methods
from .models import *
from .views_api import getContext
import json
# 아임포트 라이브러리
from iamport import Iamport

# 아임포트 API 키
iamport = Iamport(imp_key=settings.IAMPORT_API_KEY, imp_secret=settings.IAMPORT_API_SECRET)

# ------------------------------------------------------------------
# ClassName   : getMerchantUid
# Description : 결제를 위한 파라미터 전달 API
# ------------------------------------------------------------------
@require_http_methods(["POST"])
def getMerchantUid(request):
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
            context = getContext("error", "This site is already added.")
            return HttpResponse(json.dumps(context), content_type="application/json")
    data = {
        'pay_method': 'card',
        'merchant_uid': str(site.merchant_uid),
        'customer_uid': str(site.customer_uid),
        'name': str(site.name),
        'amount': 1004,
        'buyer_email': request.user.username,
        'buyer_name': request.user.username,
        'buyer_tel': profile.phone
    }
    context = getContext("success", "Get Merchant Uid.", data)

    return HttpResponse(json.dumps(context), content_type="application/json")

# ------------------------------------------------------------------
# ClassName   : getMerchantUid
# Description : 결제를 위한 파라미터 전달 API
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



def PaymentAPI(request):
    # 테스트용 값
    payload = {
        'customer_uid': '{고객 아이디}',
        'schedules': [
            {
                'merchant_uid': 'test_merchant_01',
                # UNIX timestamp
                'schedule_at': 1478150985,
                'amount': 1004
            },
            {
                'merhcant_uid': 'test_merchant_02',
                # UNIX timestamp
                'schedule_at': 1478150985,
                'amount': 5000,
            },
        ]
    }
    try:
        response = iamport.pay_schedule(**payload)
        print(response)
    except KeyError:
        # 필수 값이 없을때 에러 처리
        print(KeyError)
        pass
    except Iamport.ResponseError as e:
        # 응답 에러 처리
        print(e.code)
        print(e.message)
    except Iamport.HttpError as http_error:
        # HTTP not 200 응답 에러 처리
        print(http_error.code)
        print(http_error.reason)
    context = {}
    return HttpResponse(json.dumps(context), content_type="application/json")