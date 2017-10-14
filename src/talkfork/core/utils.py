import requests
import json
from django.conf import settings
from .ml import ML

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


GROUPS = []
IGNORE_MESSAGES = []

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
    messages, users = (get_comment_data(comments_parsed), default_thread['participants'])
    ml = ML(users)
    clusters, graph = ml.get_clusters_and_graph(messages)
    if clusters:
        send_comment(default_thread, "Hi {}! Seems like your TALK deserves being FORKED. Just type /yes and I'll take care of the rest."
                     .format([get_name(user) for user in clusters]))
        GROUPS.append(clusters)
    return graph

def on_yes(comment_id, user):
    if comment_id in IGNORE_MESSAGES:
        return
    IGNORE_MESSAGES.append(comment_id)
    for group in GROUPS:
        if user in group:
            cut_group(user)
            GROUPS.remove(group)


