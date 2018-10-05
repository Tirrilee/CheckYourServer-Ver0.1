from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from .models import *
import json, sys
# SMS 전송 라이브러리
from sdk.api.message import Message
from sdk.exceptions import CoolsmsException

# Create your views here.

@require_http_methods(["POST"])
def SMSValidate(request):
    # 전화번호 가져오기
    number = request.POST.get('number', None)
    lng = request.POST.get('lng', None)
    # APK Key
    api_key = "NCSHOF1IQLXBBNA0"
    api_secret = "CDTEK50OCSZ1AOHDFFSL3BQX5NB5CUXA"

    params = dict()
    params['type'] = 'sms'  # Message type ( sms, lms, mms, ata )
    params['to'] = '01000000000'  # Recipients Number '01000000000,01000000001'
    params['from'] = '01024932906'  # Sender number
    params['text'] = 'Test Message'  # Message

    context = {}
    return HttpResponse(json.dumps(context), content_type="application/json")

@require_http_methods(["GET"])
def getNation(request):
    nations = Nation.objects.all()
    result = []
    for n in nations:
        dict = {}
        dict['id'] = n.id
        dict['name'] = n.name
        dict['flag'] = n.flag
        dict['callcode'] = n.callcode
        result.append(dict)
    context = {}
    context['results'] = result
    return HttpResponse(json.dumps(context), content_type="application/json")