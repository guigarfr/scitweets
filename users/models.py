from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    # This field is required.
    user = models.OneToOneField(User, related_name='profile')

    class Meta:
        app_label = 'users'

    # Other fields here
    def __unicode__(self):
        return self.user.username.encode('utf8')

