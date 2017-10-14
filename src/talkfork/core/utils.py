import requests
import json

oauth2_headers = {'Authorization': 'Bearer oauth2:9b3d62d69d44fb52330e5018a0ea053382236915'}


def get_comment_data(comments_parsed, max_messages_count=100):

    data = []
    for comment in comments_parsed[:max_messages_count]:
        comment_data = dict()
        comment_data['user'] = comment['creator']

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
    default_thread_id = json.loads(threads.text)[0]['id']

    comments = requests.get('https://api.twistapp.com/api/v2/comments/get',
                            headers=oauth2_headers, params={'thread_id': default_thread_id})
    comments_parsed = json.loads(comments.text)
    get_comment_data(comments_parsed)

    # call ML

    return []
