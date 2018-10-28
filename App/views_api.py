from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from .models import *
import json, re, random
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# SMS 전송 라이브러리
from sdk.api.message import Message
from sdk.exceptions import CoolsmsException


# Create your views here.

# Json Context 출력
def getContext(status, msg, data=None):
    result = {}
    result['status'] = status
    result['message'] = msg
    result['data'] = data
    return result

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

@require_http_methods(["POST"])
def SMSValidate(request):
    # 전화번호 가져오기
    number = request.POST.get('number', None)
    country = request.POST.get('country', None)
    code = random.randint(100000,999999)
    # APK Key
    api_key = "NCSHOF1IQLXBBNA0"
    api_secret = "CDTEK50OCSZ1AOHDFFSL3BQX5NB5CUXA"

    params = dict()
    params['type'] = 'sms'  # Message type ( sms, lms, mms, ata )
    params['to'] = number  # Recipients Number '01000000000,01000000001'
    params['country'] = country
    params['from'] = '01024932906'  # Sender number
    params['text'] = 'Your CheckYourSite verification code is '+str(code)  # Message

    Validate.objects.create(number=number, code=code)
    cool = Message(api_key, api_secret)

    try:
        response = cool.send(params)
        print("Success Count : %s" % response['success_count'])
        print("Error Count : %s" % response['error_count'])
        print("Group ID : %s" % response['group_id'])
        context = getContext("success", "Message Send!")
        if "error_list" in response:
            context = getContext("error", response['error_list'])
            print("Error List : %s" % response['error_list'])

    except CoolsmsException as e:
        print("Error Code : %s" % e.code)
        print("Error Message : %s" % e.msg)
        context = getContext("error", e.msg)

    return HttpResponse(json.dumps(context), content_type="application/json")

# ------------------------------------------------------------------
# ClassName   : LoginAPI
# Description : 로그인을 위한 API
# ------------------------------------------------------------------
@require_http_methods(["POST"])
def SigninAPI(request):
    email = request.POST.get('email', None)
    password = request.POST.get('password', None)

    if email=="" or password=="":
        context = getContext("error", "Fields are required.")
    else:
        try:
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                context = getContext("success", "Success to Sign in.")
            else:
                context = getContext("error", "Check your email and password.")
        except:
            context = getContext("error", "Fail to Sign in.")
    return HttpResponse(json.dumps(context), content_type="application/json")

# ------------------------------------------------------------------
# ClassName   : SignupAPI
# Description : 로그인을 위한 API
# ------------------------------------------------------------------
@require_http_methods(["POST"])
def SignupAPI(request):
    email = request.POST.get('email', None)
    password = request.POST.get('password', None)
    password2 = request.POST.get('password2', None)
    birth = request.POST.get('birth', None)
    number = request.POST.get('number', None)
    code = request.POST.get('code', None)

    print("email : " + email)
    print("password : " + password)
    print("password2: " + password2)
    print("birth: " + birth)
    email_reg = re.compile("([a-z0-9_\.-]+)@([\da-z\.-]+)\.([a-z\.]{2,6})")
    email_match = email_reg.match(email)
    password_reg = re.compile("(?=.*[a-zA-Z])(?=.*[!@#$%^*+=-])(?=.*[0-9]).{6,16}")
    password_match = password_reg.match(password)
    validate = Validate.objects.all().filter(number=number, code=0 if code == '' else int(code))


    if email == "" or password == "" or password2 == "" or code == "" or birth=="":
        context = getContext("error", "Fields are required.")
    # 이메일 정규식
    elif not email_match:
        context = getContext("error", "This email is not in email format.")
    # 비밀번호 정규식
    elif password != password2:
        context = getContext("error", "The two password fields didn't match.")
    elif not password_match:
        context = getContext("error", "This password is too common.")
    elif not validate:
        context = getContext("error", "Check your valification code.")
    else:
        try:
            user = User.objects.create_user(email, email, password)
            login_user = authenticate(request, username=email, password=password)
            user_profile = UserProfile.objects.create(user=login_user, birth=str(birth), phone=str(number))
            login(request, login_user)
            user.save()
            user_profile.save()
            context = getContext("success", "Success to Sign up.")
        except:
            context = getContext("error", "This email already exists.")
    return HttpResponse(json.dumps(context), content_type="application/json")

