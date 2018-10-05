from django.shortcuts import render
from .models import *
# Create your views here.

def MainPage(request):
    nations = Nation.objects.all()
    return render(request, 'Main/MainPage.html', {
        'nations': nations,
    })

def CallcodeInput(request):
    import requests

    url = "https://restcountries.eu/rest/v2/all"
    req = requests.get(url=url)
    data = req.json()
    for d in data:
        Nation.objects.create(name=d['name'], flag=d['flag'], callcode=d['callingCodes'][0])
        print(d['name'])
        print(d['flag'])
        print(d['callingCodes'])

    return render(request, 'test.html', {})