# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^list/$', views.TweetListView.as_view(), name='list'),
    url(r'^voted/$', views.TweetAnswerListView.as_view(), name='voted'),
    url(r'^vote/$', views.CreateAnswerView.as_view(), name='vote'),
]
