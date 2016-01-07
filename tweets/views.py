# -*- coding: utf-8 -*-
# from django.contrib import messages
import json
from django.views.generic import CreateView, ListView, FormView, UpdateView
from braces.views import LoginRequiredMixin
from django.utils.translation import ugettext_lazy
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import redirect

from django.contrib.contenttypes.models import ContentType

from . import models
from . import forms
from accounts.views import ScitweetsContextMixin
from lib.views import send_manually_exception_email


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
        self.queryset = self.model.objects.filter(content_type=tweet_type, user=self.request.user.profile)
        return self.queryset

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
        self.queryset = self.model.objects.filter(content_type=trendingtopic_type, user=self.request.user.profile)
        return self.queryset

    def get_context_data(self, **kwargs):
        context = {
            'trendingtopic': True
        }
        context.update(kwargs)
        return super(TrendingTopicAnswerListView, self).get_context_data(**context)


class QuestionListView(LoginRequiredMixin, ScitweetsContextMixin, ListView):
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
        context['unanswered_count'] = self.about_object_class.objects.exclude(
            answers__user=self.request.user.profile).count()
        context['answered_count'] = self.about_object_class.objects.filter(
            answers__user=self.request.user.profile).count()
        assert(self.about_object_class.objects.all().count() ==
               (context['unanswered_count'] + context['answered_count']))
        return context


class UpdateAnswerView(LoginRequiredMixin, ScitweetsContextMixin, UpdateView):
    model = models.Answer
    template_name = 'tweets/vote.html'
    form_class = forms.CreateAnswerForm
    redirect_unauthenticated_users = True
    question = None
    about_object = None
    about_object_class = None
    object = None
    pk_url_kwarg = 'answer_id'

    def get_initial(self):
        initials = dict()
        if self.about_object:
            initials.update({
                "object_id": self.object.pk,
                "question": self.object.question.pk,
            })

            initials.update(super(UpdateAnswerView, self).get_initial())

        return initials

    def get_context_data(self, *args, **kwargs):
        context = super(UpdateAnswerView, self).get_context_data(*args, **kwargs)
        context['question'] = self.object.question
        about_class = self.object.content_type.model_class()
        context['unanswered_count'] = about_class.objects.exclude(
            answers__user=self.request.user.profile).count()
        context['answered_count'] = about_class.objects.filter(
            answers__user=self.request.user.profile).count()
        assert(about_class.objects.all().count() ==
               (context['unanswered_count'] + context['answered_count']))
        return context


class TweetImportFormView(LoginRequiredMixin, ScitweetsContextMixin, FormView):
    template_name = 'tweets/import_tweets.html'
    form_class = forms.UploadFileForm

    def get_success_url(self):
        return reverse('tweets:tweet_list')

    def parse_json_text(self, text):
        try:
            return json.loads(text)
        except ValueError as e:
            print('invalid json: %s' % e)
            return None # or: raise

    def parse_json_file(self, json_file):
        raw_data = json_file.read()

        # Check if file is a correct json
        json_data = self.parse_json_text(raw_data)

        # File might be json data for each row
        if not json_data:
            raw_data = raw_data.split('\n')

            json_data = list()
            for row_data in raw_data:
                if row_data:
                    parsed_row_data = self.parse_json_text(row_data)
                    if not parsed_row_data:
                        return None
                    json_data.append(parsed_row_data)

        return json_data

    def parse_tweet_data_from_json_data_array(self, json_data_array):

        tweet_imported = tweet_found = tweet_failure_format = tweet_failure_other = 0
        for json_tweet in json_data_array:
            tweet_text = json_tweet.get('text', None)
            tweet_id = json_tweet.get('id', None)

            # Check for needed fields
            if tweet_text is None or tweet_id is None:
                tweet_failure_format += 1
                continue

            # Check for existing tweet or create new one
            try:
                _ = models.Tweet.objects.get(id_twitter=int(json_tweet['id']))
                tweet_found += 1
            except models.Tweet.DoesNotExist:
                try:
                    new_tweet = models.Tweet(id_twitter=int(tweet_id), text=unicode(tweet_text))
                    new_tweet.save()
                    tweet_imported += 1
                except Exception, e:
                    send_manually_exception_email(self.request, e)
                    tweet_failure_other += 1

        imported_tweets = {
            'imported': tweet_imported,
            'existing': tweet_found,
            'failure_format': tweet_failure_format,
            'failure_other': tweet_failure_other
        }

        failure_text = []
        warning_text = u''
        if tweet_imported:
            if not tweet_found:
                success_text = u"%(imported)d tweets were imported from file" % imported_tweets
            else:
                success_text = u'%(imported)d tweets were imported from file and ' \
                               u'%(existing)d already existed in the database' % imported_tweets
            messages.success(self.request, ugettext_lazy(success_text))
        else:
            warning_text = u'No new tweets were created.'

        if tweet_failure_format:
            failure_text.append(u'There were %(failure_format)d tweets had format errors' % imported_tweets)
        if tweet_failure_other:
            failure_text.append(u'%(failure_other)s tweets led to unexpected errors' % imported_tweets)

        if failure_text:
            messages.error(self.request, ugettext_lazy(' and '.join(failure_text).capitalize()))
        elif warning_text:
            messages.warning(self.request, ugettext_lazy(warning_text))

        return tweet_imported

    def form_valid(self, form):

        form_file = form.cleaned_data.get('file', None)

        if form_file is None:
            messages.error(self.request, ugettext_lazy("File field is required"))

        json_data = self.parse_json_file(form_file)

        if json_data is None:
            failure_text = ugettext_lazy(u'There was no data we could process in this file')
            messages.error(self.request, failure_text)
            return super(TweetImportFormView, self).form_invalid(form)

        imported_tweets = self.parse_tweet_data_from_json_data_array(json_data)

        if not imported_tweets:
            return super(TweetImportFormView, self).form_invalid(form)

        return super(TweetImportFormView, self).form_valid(form)

    def get_context_data(self, **kwargs):

        context = dict()
        context['page_title'] = ugettext_lazy(u"Import tweets")
        context.update(kwargs)

        print "HI, context", context

        return super(TweetImportFormView, self).get_context_data(**context)


class TrendingTopicImportFormView(LoginRequiredMixin, ScitweetsContextMixin, FormView):
    template_name = 'tweets/import_tweets.html'
    form_class = forms.UploadFileForm

    def get_success_url(self):
        return reverse('tweets:tweet_list')

    def parse_json_file(self, json_file):
        raw_data = json_file.read()

        return raw_data

    def parse_trending_topic_data_from_text_array(self, text_array):

        tt_imported = tt_found = tt_failure_format = tt_failure_other = 0
        for text_tt in text_array:
            print "Trending topic line:", text_tt
            # tweet_text = json_tweet.get('text', None)
            # tweet_id = json_tweet.get('id', None)
            #
            # # Check for needed fields
            # if tweet_text is None or tweet_id is None:
            #     tweet_failure_format += 1
            #     continue
            #
            # # Check for existing tweet or create new one
            # try:
            #     _ = models.Tweet.objects.get(id_twitter=int(json_tweet['id']))
            #     tweet_found += 1
            # except models.Tweet.DoesNotExist:
            #     try:
            #         new_tweet = models.Tweet(id_twitter=int(tweet_id), text=unicode(tweet_text))
            #         new_tweet.save()
            #         tweet_imported += 1
            #     except Exception, e:
            #         send_manually_exception_email(self.request, e)
            #         tweet_failure_other += 1

        imported_tts = {
            'imported': tt_imported,
            'existing': tt_found,
            'failure_format': tt_failure_format,
            'failure_other': tt_failure_other
        }

        failure_text = []
        warning_text = u''
        if tt_imported:
            if not tt_found:
                success_text = u"%(imported)d tweets were imported from file" % imported_tts
            else:
                success_text = u'%(imported)d tweets were imported from file and ' \
                               u'%(existing)d already existed in the database' % imported_tts
            messages.success(self.request, ugettext_lazy(success_text))
        else:
            warning_text = u'No new tweets were created.'

        if tt_failure_format:
            failure_text.append(u'There were %(failure_format)d tweets had format errors' % imported_tts)
        if tt_failure_other:
            failure_text.append(u'%(failure_other)s tweets led to unexpected errors' % imported_tts)

        if failure_text:
            messages.error(self.request, ugettext_lazy(' and '.join(failure_text).capitalize()))
        elif warning_text:
            messages.warning(self.request, ugettext_lazy(warning_text))

        return tt_imported

    def form_valid(self, form):

        form_file = form.cleaned_data.get('file', None)

        if form_file is None:
            messages.error(self.request, ugettext_lazy("File field is required"))

        json_data = self.parse_json_file(form_file)

        if json_data is None:
            failure_text = ugettext_lazy(u'There was no data we could process in this file')
            messages.error(self.request, failure_text)
            return super(TweetImportFormView, self).form_invalid(form)

        imported_tweets = self.parse_trending_topic_data_from_text_array(json_data)

        if not imported_tweets:
            return super(TweetImportFormView, self).form_invalid(form)

        return super(TweetImportFormView, self).form_valid(form)

    def get_context_data(self, **kwargs):

        context = dict()
        context['page_title'] = ugettext_lazy(u"Import trending topics")
        context.update(kwargs)

        print "HI, context", context

        return super(TrendingTopicImportFormView, self).get_context_data(**context)
