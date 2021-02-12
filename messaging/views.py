from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import HttpResponseServerError
from django.http import JsonResponse
from json import loads
from .models import CustomUser

@csrf_exempt
def login(request):
    if request.method == 'POST':
       mJson = loads(request.body.decode("utf-8"))
       username = mJson.get('username')
       password = mJson.get('password')
       print(username)
       print (password)
       return JsonResponse({
           "response" : "post successful"
       })
    else:
        return HttpResponseBadRequest("Missing username or password")

@csrf_exempt 
def register(request):
    if request.method == 'POST':
       mJson = loads(request.body.decode("utf-8"))
       username = mJson.get('username')
       conflicts = CustomUser.objects.filter(username=username)
       if(len(conflicts) > 0):
           return HttpResponseServerError("Username already taken")
       password = mJson.get('password')
       new_user = CustomUser(username=username, password=password)
       new_user.save()
       return HttpResponse("User Created")

    else:
        return HttpResponseBadRequest("Missing username or password")
