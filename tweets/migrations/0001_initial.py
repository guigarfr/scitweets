# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question_id', models.IntegerField()),
                ('question_text', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='TweetAnswer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('result', models.NullBooleanField()),
                ('tweet', models.ForeignKey(to='tweets.Question')),
                ('user', models.ForeignKey(to='accounts.UserProfile')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='tweetanswer',
            unique_together=set([('tweet', 'user')]),
        ),
    ]
