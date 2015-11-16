# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.TweetListView.as_view(), name='list'),
    url(r'^vote/$', views.CreateAnswerView.as_view(), name='vote'),
]
