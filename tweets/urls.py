# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^tweets/$', views.TweetListView.as_view(), name='tweet_list'),
    url(r'^tweets/voted/$', views.TweetAnswerListView.as_view(), name='tweets_voted'),

    url(r'^hashtags/$', views.HashtagListView.as_view(), name='hashtag_list'),
    url(r'^hashtags/voted/$', views.HashtagAnswerListView.as_view(), name='hashtags_voted'),

    url(r'^questions/$', views.QuestionListView.as_view(), name='tweet_question_list'),
    url(r'^answers/(?P<question_id>\d+)/new/$', views.CreateAnswerView.as_view(), name='tweet_answer_new')
]
