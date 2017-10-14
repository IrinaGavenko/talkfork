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
    for comment in comments:
        if comment["content"] != "/yes":
            continue
        if comment["id"] in IGNORE_MESSAGES:
            continue
        IGNORE_MESSAGES.append(comment["id"])
        for group in GROUPS:
            if comment["creator"] in group:
                cut_group(comment["creator"])
                GROUPS.remove(group)
    messages, users = (get_comment_data(comments_parsed), default_thread['participants'])
    ml = ML(users)
    clusters, graph = ml.get_clusters_and_graph(messages)

    # user = requests.get('https://api.twistapp.com/api/v2/users/getone',
    #                     headers=oauth2_headers)
    #
    # move_users_comments(default_channel_id, default_thread['id'], [], [json.loads(user.text)['id']])

    if clusters:
        send_comment(default_thread, "Hi {}! Seems like your TALK deserves being FORKED. Just type /yes and I'll take care of the rest."
                     .format([get_name(user) for user in clusters]))
        GROUPS.append(clusters)
    return graph

def send_comment(thread_id, message):

    requests.post('https://api.twistapp.com/api/v2/comments/add',
                  data={'thread_id': thread_id, 'content': message},
                  headers=oauth2_headers)


def move_users_comments(channel_id, thread_id, comments, users_to_move):

    comments = requests.get('https://api.twistapp.com/api/v2/comments/get',
                            headers=oauth2_headers, params={'thread_id': thread_id})
    comments = json.loads(comments.text)

    comments_to_move = []

    # Detect comments to delete
    for comment in comments:
        if comment['creator'] in users_to_move:
            comments_to_move.append(comment['id'])

    # Create new thread and move comments to it
    new_thread = requests.post('https://api.twistapp.com/api/v2/threads/add',
                               data={'channel_id': channel_id,
                                     'title': '',
                                     'content': 'Forked thread of ',
                                     'recipients': users_to_move},
                               headers=oauth2_headers)

    new_thread = json.loads(new_thread.text)
    print(new_thread)
    #
    # for comment in comments_to_move:
    #     requests.post('https://api.twistapp.com/api/v2/comments/add',
    #                   data={'thread_id': new_thread['id'], 'content': comment['content']},
    #                   headers=oauth2_headers)
    #
    # # Remove comments
    # for comment in comments_to_move:
    #     requests.post('https://api.twistapp.com/api/v2/comments/remove',
    #                   data={'id': comment['id']},
    #                   headers=oauth2_headers)
    #
    # return new_thread['id']
