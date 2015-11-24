# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^tweets/$', views.TweetListView.as_view(), name='tweet_list'),
    url(r'^tweets/voted/$', views.TweetAnswerListView.as_view(), name='tweets_voted'),

    url(r'^tts/$', views.TrendingTopicListView.as_view(), name='trendingtopic_list'),
    url(r'^tts/voted/$', views.TrendingTopicAnswerListView.as_view(), name='trendingtopics_voted'),

    url(r'^questions/$', views.QuestionListView.as_view(), name='tweet_question_list'),
    url(r'^answers/(?P<question_id>\d+)/new/$', views.CreateAnswerView.as_view(), name='tweet_answer_new')
]
