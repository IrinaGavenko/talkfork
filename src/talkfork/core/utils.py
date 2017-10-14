import requests
import json
from django.conf import settings

oauth2_headers = {'Authorization': 'Bearer ' + settings.TWIST_API_KEY}


def get_comment_data(comments_parsed, max_messages_count=100):

    data = []
    for comment in comments_parsed[:max_messages_count]:
        comment_data = dict()
        comment_data['user_id'] = comment['creator']

        if comment['recipients'] == 'EVERYONE' or comment['recipients'] == 'EVERYONE_IN_THREAD':
            comment_data['recipients'] = []
        else:
            comment_data['recipients'] = comment['recipients']

        comment_data['time'] = comment['posted_ts']
        comment_data['message'] = comment['content']
        data.append(comment_data)

    return data


def watch_comments():

    channels = requests.get('https://api.twistapp.com/api/v2/workspaces/get',
                            headers=oauth2_headers)
    default_channel_id = json.loads(channels.text)[0]['default_channel']

    threads = requests.get('https://api.twistapp.com/api/v2/threads/get',
                           headers=oauth2_headers, params={'channel_id': default_channel_id})
    default_thread = json.loads(threads.text)[0]

    comments = requests.get('https://api.twistapp.com/api/v2/comments/get',
                            headers=oauth2_headers, params={'thread_id': default_thread['id']})
    comments_parsed = json.loads(comments.text)
    data = (get_comment_data(comments_parsed), default_thread['participants'])

    # call ML

    return []
