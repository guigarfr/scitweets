# -*- coding: utf-8 -*-
import datetime
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

from django.db import models
from django.utils import timezone
from accounts.models import UserProfile
from .managers import TweetManager
from django.utils.translation import ugettext as _

ANSWER_VALUE_TYPES = [
        (0, _(u"Integer")),
        (1, _(u"String")),
        (2, _(u"Boolean"))
    ]


class UpdatedCreatedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Tweet(UpdatedCreatedModel):
    id_twitter = models.IntegerField(blank=False, null=False)
    text = models.CharField(max_length=200)
    is_scientific = models.NullBooleanField(null=True, default=None)
    answers = GenericRelation('Answer')

    objects = TweetManager()
    
    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return unicode(self.text)


class Hashtag(UpdatedCreatedModel):
    text = models.CharField(max_length=200, null=False, blank=False)
    answers = GenericRelation('Answer')

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return u'#' + unicode(self.text)


class Question(UpdatedCreatedModel):
    question = models.CharField(max_length=200, null=False, blank=False)
    tweet_or_hashtag = models.Q(app_label='tweets', model='tweet') | models.Q(app_label='tweets', model='hashtag')
    content_type = models.ForeignKey(ContentType, limit_choices_to=tweet_or_hashtag)
    answer_value_type = models.PositiveSmallIntegerField(null=False, blank=False, choices=ANSWER_VALUE_TYPES)

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return unicode(self.question)

    @property
    def is_tweet(self):
        return self.content_type.model == 'tweet'

    @property
    def is_hashtag(self):
        return self.content_type.model == 'hashtag'


class Answer(UpdatedCreatedModel):
    user = models.ForeignKey(UserProfile, null=False, related_name='answers', related_query_name='answer')
    question = models.ForeignKey(Question, related_name='answers', related_query_name='answer')

    tweet_or_hashtag = models.Q(app_label='tweets', model='tweet') | models.Q(app_label='tweets', model='hashtag')
    content_type = models.ForeignKey(ContentType, limit_choices_to=tweet_or_hashtag)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    value_type = models.PositiveSmallIntegerField(blank=False, null=False, choices=ANSWER_VALUE_TYPES)
    value_int = models.IntegerField(null=True, blank=True)
    value_str = models.CharField(max_length=100, null=True, blank=True)
    value_bool = models.NullBooleanField()

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        value = self.value
        if value is None:
            return _(u"Unanswered")
        if isinstance(value, bool):
            if value:
                return _(u"Yes")
            else:
                return _(u"No")
        return unicode(self.value)

    @property
    def value(self):
        if self.value_type == 0:
            return self.value_int
        elif self.value_type == 1:
            return self.value_str
        if self.value_type == 2:
            return self.value_bool

    @value.setter
    def value(self, value):
        if self.value_type == 0:
            self.value_int = value
        elif self.value_type == 1:
            self.value_str = value
        if self.value_type == 2:
            self.value_bool = value