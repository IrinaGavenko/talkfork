from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import json
from .utils import watch_comments, get_usernames
from django.conf import settings

oauth2_headers = {'Authorization': 'Bearer ' + settings.TWIST_API_KEY}


def oauth2(request):

    code = request.GET.get('code')
    request.user.code = code
    return render(request, 'index.html')


def comments(request):

    return JsonResponse(watch_comments(), safe=False)


def usernames(request):

    return JsonResponse(get_usernames(), safe=False)


def index(request):
    watch_comments()
    return render(request, 'index.html')


def json_response(result, data):
    response = json.dumps({"result": result, "data": data})
    return HttpResponse(response, mimetype="application/json")
