# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('tweets', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tweet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id_twitter', models.IntegerField()),
                ('text', models.CharField(max_length=200)),
                ('is_scientific', models.NullBooleanField(default=None)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TweetYesNoAnswer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('result', models.NullBooleanField()),
                ('tweet', models.ForeignKey(to='tweets.Tweet')),
                ('user', models.ForeignKey(to='users.UserProfile')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='tweetanswer',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='tweetanswer',
            name='tweet',
        ),
        migrations.RemoveField(
            model_name='tweetanswer',
            name='user',
        ),
        migrations.DeleteModel(
            name='Question',
        ),
        migrations.DeleteModel(
            name='TweetAnswer',
        ),
        migrations.AlterUniqueTogether(
            name='tweetyesnoanswer',
            unique_together=set([('tweet', 'user')]),
        ),
    ]
