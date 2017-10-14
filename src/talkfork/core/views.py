from django.http import HttpResponse
from django.shortcuts import render
import requests
import json
from .utils import watch_comments, move_users_comments
from django.conf import settings

oauth2_headers = {'Authorization': 'Bearer ' + settings.TWIST_API_KEY}


def oauth2(request):

    code = request.GET.get('code')
    request.user.code = code
    return render(request, 'index.html')


def webhook(request):

    response = requests.get('https://api.twistapp.com/api/v2/users/getone',
                            headers=oauth2_headers)
    print(response)
    return render(request, 'index.html')


def index(request):

    watch_comments()
    return render(request, 'index.html')


def json_response(result, data):
    response = json.dumps({"result": result, "data": data})
    return HttpResponse(response, mimetype="application/json")


def comments(request):

    request.POST.get('')
    watch_comments()
