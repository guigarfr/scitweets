from django.db import models


class TweetQuerySet(models.QuerySet):

    use_for_related_fields = True

    def unanswered(self):
        return self.filter(is_scientific=None)

    def answered(self):
        return self.exclude(is_scientific=None)

    def answered_by_user(self, user=None):
        if user is None:
            return self
        return self.filter(answer__user=user)

    def unanswered_by_user(self, user=None):
        if user is None:
            return self
        return self.exclude(answer__user=user)


class TweetManager(models.Manager):
    def get_queryset(self):
        return TweetQuerySet(self.model, using=self._db)