from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^api/comments/$', views.comments, name='comments'),
    url(r'^api/usernames/$', views.usernames, name='usernames'),
]
