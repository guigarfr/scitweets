from django.contrib import admin
from . import models


@admin.register(models.Tweet)
class TweetAdmin(admin.ModelAdmin):
    pass


@admin.register(models.TweetYesNoAnswer)
class TweetAdmin(admin.ModelAdmin):
    pass
