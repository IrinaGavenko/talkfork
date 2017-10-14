import requests
import json
from .tokens import tokens
from .utils import send_comment
from . import utils

for token in tokens:
    utils.oauth2_headers = {'Authorization': 'Bearer ' + tokens[-1]}
    channels = requests.get('https://api.twistapp.com/api/v2/workspaces/get',
                            headers=utils.oauth2_headers)
    default_channel_id = json.loads(channels.text)[0]['default_channel']

    threads = requests.get('https://api.twistapp.com/api/v2/threads/get',
                           headers=utils.oauth2_headers, params={'channel_id': default_channel_id})
    default_thread = json.loads(threads.text)[0]
    utils.oauth2_headers = {'Authorization': 'Bearer ' + token}
    send_comment(default_thread["id"], "Test", as_user=True)

