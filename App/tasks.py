from __future__ import absolute_import

from CheckYourServer.celery import app
from .models import Site, CheckLog
import requests
# SMS 전송 라이브러리
from sdk.api.message import Message
from sdk.exceptions import CoolsmsException
def SendSMS(number, msg):
    # APK Key
    api_key = "NCSHOF1IQLXBBNA0"
    api_secret = "CDTEK50OCSZ1AOHDFFSL3BQX5NB5CUXA"

    params = dict()
    params['type'] = 'sms'  # Message type ( sms, lms, mms, ata )
    params['to'] = number  # Recipients Number '01000000000,01000000001'
    params['country'] = '82'
    params['from'] = '01024932906'  # Sender number
    params['text'] = msg

    cool = Message(api_key, api_secret)

    try:
        response = cool.send(params)
        print("Success Count : %s" % response['success_count'])
        print("Error Count : %s" % response['error_count'])
        print("Group ID : %s" % response['group_id'])
        if "error_list" in response:
            print("Error List : %s" % response['error_list'])

    except CoolsmsException as e:
        print("Error Code : %s" % e.code)
        print("Error Message : %s" % e.msg)

@app.task
def CheckSite():
    # 실제 백그라운드에서 작업할 내용을 task로 정의한다.
    sites = Site.objects.filter(status="paid")
    for site in sites:
        # 1. 사이트 중 에러가 안난 사이트를 가져와서 확인한다.
        # 2. 이중 에러가 날 경우 상태를 바꾸고, 문자를 전송한다.
        # 3. 사이트 중 에러가 이미 난 사이트를 파싱해 확인한다.
        result = CheckLog.objects.filter(site=site).order_by('created_at').last()
        print(result)

        # 파싱한 값의 에러가 True의 경우 문자 전송 안하고 새로운 데이터 생성
        if result.error_flag:
            print("이전 파싱 때 에러")
            try:
                req = requests.get(str(site.url))
                CheckLog.objects.create(
                    site=site,
                    status_code=str(req.status_code),
                    error_flag=False if str(req.status_code) == "200" else True,
                    error_msg=str(req.reason),
                    headers=str(req.headers),
                    response_tiem=float(req.elapsed.total_seconds())
                )
            except:
                CheckLog.objects.create(
                    site=site,
                    status_code="900",
                    error_flag=True,
                    error_msg="알 수 없는 에러입니다.",
                )
        else:
            print("이전 파싱 때 정상")
            try:
                req = requests.get(str(site.url))
                if not str(req.status_code) == "200":
                    print("에러발생")
                    print(str(site) + " : 문자전송")
                CheckLog.objects.create(
                    site=site,
                    status_code=str(req.status_code),
                    error_flag=False if str(req.status_code) == "200" else True,
                    error_msg=str(req.reason),
                    headers=str(req.headers),
                    response_tiem=float(req.elapsed.total_seconds())
                )
            except:
                print("에러발생")
                print(str(site) + " : 문자전송")
                CheckLog.objects.create(
                    site=site,
                    status_code="900",
                    error_flag=True,
                    error_msg="알 수 없는 에러입니다.",
                )