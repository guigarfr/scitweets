from django.contrib import admin
from . import models
from django.contrib.contenttypes.admin import GenericTabularInline

@admin.register(models.Tweet)
class TweetAdmin(admin.ModelAdmin):
    pass


@admin.register(models.TrendingTopic)
class TrendingTopicAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Answer)
class AnswerAdmin(admin.ModelAdmin):
    pass


# class AnswersInline(GenericTabularInline):
#     model = models.Answer
#
#
# @admin.register(models.Question)
# class QuestionAdmin2(admin.ModelAdmin):
#     inlines = (AnswersInline, )