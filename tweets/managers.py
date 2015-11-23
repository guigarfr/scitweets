from django.db import models


class TweetQuerySet(models.QuerySet):

    use_for_related_fields = True

    def unanswered(self):
        return self.filter(is_scientific=None)

    def answered(self):
        return self.exclude(is_scientific=None)

    def answered_by_user(self, user=None):
        if user is None:
            return self.none()
        return self.filter(answers__user=user)

    def unanswered_by_user(self, user=None):
        if user is None:
            return self.none()
        return self.exclude(answers__user=user)

    def next_unanswered_by_user(self, user=None):
        if user is None:
            return self.none()
        return self.unanswered_by_user(user).first()

    def next_unanswered_by_user2(self, user=None):
        if user is None:
            return self.none()
        return self.unanswered_by_user2(user).first()



class TweetManager(models.Manager):
    def get_queryset(self):
        return TweetQuerySet(self.model, using=self._db)