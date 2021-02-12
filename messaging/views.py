from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import HttpResponseServerError
from django.http import JsonResponse
from json import loads
from .models import CustomUser
from django.contrib.auth import hashers

@csrf_exempt
def login(request):
    if request.method == 'POST':
       mJson = loads(request.body.decode("utf-8"))
       username = mJson.get('username')
       existing_uname_list = CustomUser.objects.filter(username=username)
       if len(existing_uname_list) < 1:
           return HttpResponseBadRequest("No such user exists")
       password = mJson.get('password')
       if not hashers.check_password(password, existing_uname_list[0].password):
           return HttpResponseBadRequest("incorrect password")
       else:
            return HttpResponse("Logged you in")

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
       hashed_password = hashers.make_password(password)
       new_user = CustomUser(username=username, password=hashed_password)
       new_user.save()
       return HttpResponse("User Created")

    else:
        return HttpResponseBadRequest("Missing username or password")
