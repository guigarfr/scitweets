# -*- coding: utf-8 -*-
# from django.contrib import messages
from django.views.generic import CreateView, ListView
from braces.views import LoginRequiredMixin
from django.utils.translation import ugettext_lazy
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import redirect

from . import models
from . import forms
from accounts.views import MenuContextMixin


class TweetListView(ListView):
    model = models.Tweet
    template_name = 'tweets/list.html'


class CreateAnswerView(LoginRequiredMixin, MenuContextMixin, CreateView):
    model = models.TweetYesNoAnswer
    template_name = 'tweets/vote.html'
    form_class = forms.TweetQuestionForm
    redirect_unauthenticated_users = True
    tweet = None

    def get_initial(self):
        # Get first unanswered tweet
        initials = dict()
        first_unanswered_tweet = models.Tweet.objects.all().unanswered_by_user(self.request.user.profile).first()
        self.tweet = first_unanswered_tweet
        print "Tweet:", first_unanswered_tweet
        initials = {
            "tweet": first_unanswered_tweet,
            "result": None,
        }
        return initials

    def get_success_url(self):
        return reverse('tweets:vote')

    def form_valid(self, form):
        tweet_answer = form.save(commit=False)
        tweet_answer.user = self.request.user.profile
        tweet_answer.save()
        return redirect(self.get_success_url())

    def get_context_data(self, *args, **kwargs):
        context = super(CreateAnswerView, self).get_context_data(*args, **kwargs)
        context['tweet'] = self.tweet
        context['unanswered_count'] = models.Tweet.objects.all().unanswered_by_user(self.request.user.profile).count()
        context['answered_count'] = models.Tweet.objects.all().answered_by_user(self.request.user.profile).count()
        assert(models.Tweet.objects.all().count() == (context['unanswered_count'] + context['answered_count']))
        return context
