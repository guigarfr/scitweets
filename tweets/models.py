# -*- coding: utf-8 -*-
import datetime
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

from django.db import models
from django.utils import timezone
from accounts.models import UserProfile
from .managers import TweetManager
from django.utils.translation import ugettext as _


class UpdatedCreatedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Tweet(UpdatedCreatedModel):
    id_twitter = models.BigIntegerField(blank=False, null=False)
    text = models.CharField(max_length=200)
    is_scientific = models.NullBooleanField(null=True, default=None)
    answers = GenericRelation('Answer')

    objects = TweetManager()
    
    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return unicode(self.text)


class TrendingTopic(UpdatedCreatedModel):
    text = models.CharField(max_length=200, null=False, blank=False)
    answers = GenericRelation('Answer')

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return unicode(self.text)


class Question(UpdatedCreatedModel):
    ANSWER_VALUE_TYPES = [
        (0, _(u"Integer")),
        (1, _(u"String")),
        (2, _(u"Boolean"))
    ]

    HELP_TEXTS = [
        (0, None),
        (1, None),
        (2, _(u"Give your oppinion about this question. "
              u"Answer YES or NO, or click the UNKNOWN button in case you cannot decrypt the content "
              u"or you don't understand it. If you do, but are greatly unsure, you can also click UNKNOWN "
              u"but it's preferable if you go for an option."))
    ]

    question = models.CharField(max_length=200, null=False, blank=False)
    tweet_or_tt = models.Q(app_label='tweets', model='tweet') | models.Q(app_label='tweets', model='trendingtopic')
    content_type = models.ForeignKey(ContentType, limit_choices_to=tweet_or_tt)
    answer_value_type = models.PositiveSmallIntegerField(null=False, blank=False, choices=ANSWER_VALUE_TYPES)

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return unicode(self.question)

    @property
    def is_tweet(self):
        return self.content_type.model == 'tweet'

    @property
    def is_trendingtopic(self):
        return self.content_type.model == 'trendingtopic'

    def answered_by_user(self, user):
        user_answers = Answer.objects.filter(question=self, user=user).count()
        return user_answers

    def to_answer_by_user(self, user):
        user_answers = Answer.objects.filter(question=self, user=user).count()
        total_objects = self.content_type.model_class().objects.all().count()
        return total_objects - user_answers

    def help_text(self):
        return self.HELP_TEXTS[self.answer_value_type][1]


class Answer(UpdatedCreatedModel):
    user = models.ForeignKey(UserProfile, null=False, related_name='answers', related_query_name='answer')
    question = models.ForeignKey(Question, related_name='answers', related_query_name='answer')

    tweet_or_tt = models.Q(app_label='tweets', model='tweet') | models.Q(app_label='tweets', model='trendingtopic')
    content_type = models.ForeignKey(ContentType, limit_choices_to=tweet_or_tt)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    value_type = models.PositiveSmallIntegerField(blank=False, null=False, choices=Question.ANSWER_VALUE_TYPES)
    value_int = models.IntegerField(null=True, blank=True)
    value_str = models.CharField(max_length=100, null=True, blank=True)
    value_bool = models.NullBooleanField()

    class Meta:
        unique_together = ('user', 'question', 'content_type', 'object_id')

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