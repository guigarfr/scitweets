# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0015_answer_object_id'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='tweetyesnoanswer',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='tweetyesnoanswer',
            name='tweet',
        ),
        migrations.RemoveField(
            model_name='tweetyesnoanswer',
            name='user',
        ),
        migrations.AlterField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(related_query_name=b'answer', related_name='answers', to='tweets.Question'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='user',
            field=models.ForeignKey(related_query_name=b'answer', related_name='answers', to='accounts.UserProfile'),
        ),
        migrations.DeleteModel(
            name='TweetYesNoAnswer',
        ),
    ]
