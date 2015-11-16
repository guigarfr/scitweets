"""scitweets URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from django.conf import settings

from accounts.views import DashboardView

from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', DashboardView.as_view()),
    url(r'^dashboard/', DashboardView.as_view(), name="dashboard"),
    url(r'^tweets/', include('tweets.urls', namespace="tweets")),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('accounts.urls', namespace="accounts")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

