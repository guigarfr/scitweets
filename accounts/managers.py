from django.db import models


class UserQuerySet(models.QuerySet):
    def unanswered(self):
        return self.filter(is_scientific=None)

    def answered_tweets(self):
        return self.answers.exclude(is_scientific=None)


class UserManager(models.Manager):
    def get_queryset(self):
        return UserQuerySet(self.model, using=self._db)