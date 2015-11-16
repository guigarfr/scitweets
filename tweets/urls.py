# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.CreateAnswerView.as_view(), name='vote'),
]
