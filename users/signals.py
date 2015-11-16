from django.db import models
from django.db.models import signals
from django.contrib.auth.models import User
from .models import UserProfile


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

signals.post_save.connect(create_user_profile, sender=User)
