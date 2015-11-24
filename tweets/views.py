# -*- coding: utf-8 -*-
# from django.contrib import messages
from django.views.generic import CreateView, ListView
from braces.views import LoginRequiredMixin
from django.utils.translation import ugettext_lazy
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import redirect

from django.contrib.contenttypes.models import ContentType

from . import models
from . import forms
from accounts.views import ScitweetsContextMixin


class TweetListView(LoginRequiredMixin, ListView, ScitweetsContextMixin):
    model = models.Tweet
    template_name = 'tweets/list.html'

    # TODO: Agrupar por question, y poner cada una en una caja? o poner columna question


class TrendingTopicListView(LoginRequiredMixin, ListView, ScitweetsContextMixin):
    model = models.TrendingTopic
    template_name = 'tweets/list_trendingtopic.html'

    # TODO: Agrupar por question, y poner cada una en una caja? o poner columna question


class TweetAnswerListView(LoginRequiredMixin, ScitweetsContextMixin, ListView):
    model = models.Answer
    template_name = 'tweets/answer_list.html'

    def get_queryset(self):
        tweet_type = ContentType.objects.get_for_model(models.Tweet)
        return self.model.objects.filter(content_type=tweet_type, user=self.request.user.profile)

    def get_context_data(self, **kwargs):
        context = {
            'tweet': True
        }
        context.update(kwargs)
        return super(TweetAnswerListView, self).get_context_data(**context)


class TrendingTopicAnswerListView(LoginRequiredMixin, ScitweetsContextMixin, ListView):
    model = models.Answer
    template_name = 'tweets/answer_list.html'

    def get_queryset(self):
        trendingtopic_type = ContentType.objects.get_for_model(models.TrendingTopic)
        return self.model.objects.filter(content_type=trendingtopic_type, user=self.request.user.profile)

    def get_context_data(self, **kwargs):
        context = {
            'trendingtopic': True
        }
        context.update(kwargs)
        return super(TrendingTopicAnswerListView, self).get_context_data(**context)



class QuestionListView(ListView):
    model = models.Question
    template_name = 'tweets/question-list.html'


class CreateAnswerView(LoginRequiredMixin, ScitweetsContextMixin, CreateView):
    model = models.Answer
    template_name = 'tweets/vote.html'
    form_class = forms.CreateAnswerForm
    redirect_unauthenticated_users = True
    question = None
    about_object = None
    about_object_class = None
    object = None

    def dispatch(self, request, *args, **kwargs):
        # Get question to answer to
        question_id = self.kwargs.get("question_id")
        try:
            self.question = models.Question.objects.get(id=question_id)
        except:
            raise ValueError("There is no question with id " + str(question_id))

        # Get first unanswered tweet or trendingtopic
        self.about_object_class = self.question.content_type.model_class()
        self.about_object = self.about_object_class.objects.exclude(answers__user=request.user.profile).first()

        return super(CreateAnswerView, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        print "Object about:", self.about_object
        initials = dict()
        if self.about_object:
            initials.update({
                "object_id": self.about_object.pk,
                "question": self.question,
            })

            initials.update(super(CreateAnswerView, self).get_initial())

        return initials

    def get_success_url(self):
        return reverse('tweets:tweet_answer_new', kwargs={
            'question_id': self.question.pk
        })

    def form_valid(self, form):
        tweet_answer = form.save(commit=False)
        tweet_answer.user = self.request.user.profile
        # tweet_answer.question = self.question
        # tweet_answer.object_id = self.about_object.pk
        tweet_answer.value_type = self.question.answer_value_type
        tweet_answer.content_type = self.question.content_type
        tweet_answer.save()
        return redirect(self.get_success_url())

    def get_context_data(self, *args, **kwargs):
        context = super(CreateAnswerView, self).get_context_data(*args, **kwargs)
        context['question'] = self.question
        context['object'] = self.about_object
        context['unanswered_count'] = self.about_object_class.objects.exclude(answers__user=self.request.user.profile).count()
        context['answered_count'] = self.about_object_class.objects.filter(answers__user=self.request.user.profile).count()
        assert(self.about_object_class.objects.all().count() == (context['unanswered_count'] + context['answered_count']))
        return context

