from __future__ import absolute_import
from celery.utils.log import get_task_logger

from CheckYourServer.celery import app
from .models import Site, CheckLog
import requests, logging


@app.task
def say_hello():
    req = requests.get("http://127.0.0.1:8000/")
    print("hellow world!")

@app.task
def CheckTest():
    site = Site.objects.get(pk=6)
    CheckLog.objects.create(site=site)
@app.task
def CheckSite():
    # 실제 백그라운드에서 작업할 내용을 task로 정의한다.
    sites = Site.objects.filter(status="paid")
    for site in sites:
        # 1. 사이트 중 에러가 안난 사이트를 가져와서 확인한다.
        # 2. 이중 에러가 날 경우 상태를 바꾸고, 문자를 전송한다.
        # 3. 사이트 중 에러가 이미 난 사이트를 파싱해 확인한다.
        result = CheckLog.objects.filter(site=site).order_by('created_at')[0]
        if not result:
            result = CheckLog.objects.create(site=site)
        try:
            req = requests.get(str(site.url))

            if not result.error_flag:
                print("문자전송")

            result.status_code = str(req.status_code)
            result.error_flag = False if str(req.status_code) == "200" else True
            result.error_msg = str(req.reason)
            result.headers = str(req.headers)
            result.response_tiem = float(req.elapsed.total_seconds())
            result.save()
            print("저장완료")

        except:
            result.status_code = "900"
            result.error_flag = True
            result.error_msg = "알 수 없는 에러입니다."
            result.save()
            print("저장완료")


