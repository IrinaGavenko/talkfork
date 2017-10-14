from django.http import HttpResponse
from django.shortcuts import render
import requests
import json
from .utils import watch_comments

oauth2_headers = {'Authorization': 'Bearer oauth2:9b3d62d69d44fb52330e5018a0ea053382236915'}


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

    return render(request, 'index.html')


def json_response(result, data):
    response = json.dumps({"result": result, "data": data})
    return HttpResponse(response, mimetype="application/json")


def comments(request):

    request.POST.get('')
    watch_comments()
