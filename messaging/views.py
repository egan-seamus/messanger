from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import HttpResponseServerError
from django.http import JsonResponse
from django.middleware.csrf import get_token
from json import loads
from .models import CustomUser
from .models import Message
from django.contrib.auth import hashers
from django.db.models import Q
from django.core import serializers


@csrf_exempt
def login(request):
    if request.method == 'POST':
       request.session.set_test_cookie()
       print(request.session.test_cookie_worked())
       mJson = loads(request.body.decode("utf-8"))
       username = mJson.get('username')
       existing_uname_list = CustomUser.objects.filter(username=username)
       if len(existing_uname_list) < 1:
           return HttpResponseBadRequest("No such user exists")
       password = mJson.get('password')
       if not hashers.check_password(password, existing_uname_list[0].password):
           return HttpResponseBadRequest("incorrect password")
       else:
            request.session['username'] = username
            # use the list we already queried for
            request.session['id'] = existing_uname_list[0].id
            request.session.modified = True
            return HttpResponse("Logged you in")

    else:
        return HttpResponseBadRequest("Missing username or password")

# check if a user is alredy logged in


@csrf_exempt
def authenticate(request):
    if request.session.has_key('username'):
        reply_message = request.session.get('username')
        return HttpResponse(reply_message)
    else:
        return HttpResponseBadRequest()


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

# get this user's most recent message with all other users


@csrf_exempt
def getMessagePreviews(request):
    messages = Message.objects.filter(Q(sender__id=request.session['id']) | Q(recipient__id=request.session['id']))
    #allSent = Message.objects.filter(sender__id=request.session.['id']).order_by('timestamp')
    uniqueMessages = [messages[0]]
    for unfilteredEntry in messages:
            unique = True
            for filteredEntry in uniqueMessages:
                if(unfilteredEntry.isFromSameConversation(filteredEntry)):
                    unique = False
            if unique:
                uniqueMessages.append(unfilteredEntry)
    # append the usernames on to the messages
    parentList = []
    for uniqueMessage in uniqueMessages:
        username = Message.sender.id if request.session['id'] != Message.sender.id else Message.recipient.id
        parentList.append {
            "username" : username,
            "message" : uniqueMessage
        }

    jason = serializers.serialize("json", parentList);
    wrapper = {"MessageJSON", jason}
    return JsonResponse(wrapper)

    # allAccepted = Message.objects.filter(recipient__id=request.session.['id']).order_by('timestamp')

# get the messages between the given user and the logged in user
@csrf_exempt
def getMessagesBetween(request):
    if(request.method == 'POST'):
        try:
            mJson = loads(request.body.decode("utf-8"))
            recipient_id = mJson.get('recipient_id')
            sender = CustomUser.objects.get(id=request.session['id'])
            recipeint = CustomUser.objects.get(id=recipient_id)
            messages = Message.objects.filter(
                (Q(sender__id=request.session['id']) & Q(recipient__id=recipient_id)) 
                | (Q(sender__id=recipient_id) & Q(recipient__id=request.session['id'])))
            jason = serializers.serialize("json", messages);
            wrapper = {"MessageJSON", jason}
            return JsonResponse(wrapper)
        except:
            return HttpResponseBadRequest()





# add this message to the database
# request must have a json in the body that has
# sender_id, an int
# recipient_id, an int
# text, a string
@csrf_exempt
def sendMessage(request):
    if(request.method == 'POST'):
       mJson = loads(request.body.decode("utf-8"))
       sender_id = mJson.get('sender_id')
       recipient_id = mJson.get('recipient_id')
       text = mJson.get('text')
       sender = CustomUser.objects.get(id=sender_id)
       recipeint = CustomUser.objects.get(id=recipient_id)
       newMessage = Message.objects.create(
           sender = sender, recipient = recipient, text = text)
       newMessage.save()


@csrf_exempt 
def searchForUser(request):
    if(request.method == 'POST'):
       mJson = loads(request.body.decode("utf-8"))
       query = mJson.get('query')
       results = CustomUser.objects.filter(username__startswith=query)
       jason = serializers.serialize("json", results)
       wrapper = {"results", jason}
       return JsonResponse(wrapper)

# views for messages by use case
# let THIS = logged in user
# let THAT = another user

# HTTP Handleable Cases

# on login, display a home screen with recent messages
# sent to and by THIS user sorted by time of latest message
# also, open a websocket the handle new messages
# handle logins using
# https://docs.djangoproject.com/en/3.1/topics/http/sessions/

# on selection of a conversation
# getMessages between THIS user and THAT user sorted by
# date sent


# web socket cases
# see
# https://channels.readthedocs.io/en/stable/tutorial/part_2.html
# to send a message
# user should see new message when they send it
# server new message over web socket
# save message to DB
# if recipient is logged in, notify recipient's client


def csrf(request):
    return JsonResponse({'csrfToken': get_token(request)})

def ping(request):
    return JsonResponse({'result': 'OK'})
