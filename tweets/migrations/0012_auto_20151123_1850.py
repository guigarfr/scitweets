# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('accounts', '0001_initial'),
        ('tweets', '0011_auto_20151123_1846'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('object_id', models.PositiveIntegerField()),
                ('value_int', models.IntegerField(null=True, blank=True)),
                ('value_str', models.CharField(max_length=100, null=True, blank=True)),
                ('value_bool', models.NullBooleanField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('question', models.ForeignKey(to='tweets.Question')),
                ('user', models.ForeignKey(related_query_name=b'answer2', related_name='answers', to='accounts.UserProfile')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.DeleteModel(
            name='AnswerValue',
        ),
    ]
