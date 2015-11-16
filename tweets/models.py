# -*- coding: utf-8 -*-
import datetime

from django.db import models
from django.utils import timezone
from users.models import UserProfile
from .managers import TweetManager


class UpdatedCreatedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Tweet(UpdatedCreatedModel):
    id_twitter = models.IntegerField(blank=False, null=False)
    text = models.CharField(max_length=200)
    is_scientific = models.NullBooleanField(null=True, default=None)

    objects = TweetManager()
    
    def __str__(self):              # __unicode__ on Python 2
        return unicode(self).encode('utf-8')

    def __unicode__(self):              # __unicode__ on Python 2
        return unicode(self.text)
            
    # @property
#     def voted(self):
#     	n = 1
#     	votes = TweetAnswer.objects.filter(tweet=self).count()
#     	return votes >= n


class TweetYesNoAnswer(UpdatedCreatedModel):
    tweet = models.ForeignKey(Tweet, unique=False, related_name='answers', related_query_name='answer')
    user = models.ForeignKey(UserProfile, null=False, related_name='answers', related_query_name='answer')
    result = models.NullBooleanField(null=True)

    class Meta:
        unique_together = (('tweet', 'user'),)

    def __str__(self):
        return self.tweet.__str__() + ": " + str(self.result)

    def unicode(self):
        return self.__str__()


