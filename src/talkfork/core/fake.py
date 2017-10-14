import requests
import json
from .tokens import tokens
from .utils import send_comment
from . import utils

default_thread = '138882'

users = []

for token in tokens:
    utils.oauth2_headers = {'Authorization': 'Bearer ' + token}
    send_comment(default_thread["id"], "Test", as_user=True)
    users.append(requests.get("/api/v2/users/getone").json()["id"])

messages = [
    (0, [1], "Hi, where are you?"),
    (4, [], "BIENE"),
    (1, [0], "I've been waiting at A6 for 3 hours!"),
    (5, [], "MORE BIENE"),
    (2, [], "Are there any breakfast leftovers?"),
    (3, [], "Dinner will be served soon"),
    (2, [], "Have I missed lunch too?!!")
    (1, [], "LOL, lunch was at 13")
]

