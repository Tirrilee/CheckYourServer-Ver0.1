# from __future__ import absolute_import
#
# import os
# from celery import Celery
# from datetime import timedelta
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CheckYourServer.settings')
#
# from django.conf import settings
#
# app = Celery('CheckYourServer',  # 첫번째 값은 현재 프로젝트의 이름을 설정하고
#              broker='django://')  # broker: 브로커에 접속할 수 있는 URL을 설정.
# # Django 데이터베이스 백엔드를 사용하려면 'django://'로 설정한다.
#
# app.config_from_object('django.conf:settings')
# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
# app.conf.update(
#     BROKER_URL='django://',
#     CELERY_TASK_SERIALIZER='json',
#     CELERY_ACCEPT_CONTENT=['json'],  # Ignore other content
#     CELERY_RESULT_SERIALIZER='json',
#     CELERY_TIMEZONE='Asia/Seoul',
#     CELERY_ENABLE_UTC=False,
#     CELERYBEAT_SCHEDULE = {
#         'say_hello-every-seconds': {
#             'task': 'App.task.CheckTest',
#             'schedule': timedelta(seconds=10),
#             'args': ()
#         },
#     }
# )

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from datetime import timedelta
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CheckYourServer.settings')

app = Celery('CheckYourServer', broker='amqp://guest:guest@localhost:5672//')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.

app.config_from_object('django.conf:settings')
# app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
# app.autodiscover_tasks()
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.update(
    # BROKER_URL='django://',
    CELERY_TASK_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json'],  # Ignore other content
    CELERY_RESULT_SERIALIZER='json',
    CELERY_TIMEZONE='Asia/Seoul',
    CELERY_ENABLE_UTC=False,
    CELERYBEAT_SCHEDULE = {
        'say_hello-every-seconds': {
            "task": "App.tasks.CheckSite",
            'schedule': timedelta(seconds=60),
            'args': ()
        },
    }
)

# @app.task(bind=True)
# def debug_task(self):
#     print('Request: {0!r}'.format(self.request))