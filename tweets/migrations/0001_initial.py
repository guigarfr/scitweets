# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('accounts', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('object_id', models.PositiveIntegerField()),
                ('value_type', models.PositiveSmallIntegerField(choices=[(0, 'Entero'), (1, 'Cadena de caracteres'), (2, 'Booleano')])),
                ('value_int', models.IntegerField(null=True, blank=True)),
                ('value_str', models.CharField(max_length=100, null=True, blank=True)),
                ('value_bool', models.NullBooleanField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('question', models.CharField(max_length=200)),
                ('answer_value_type', models.PositiveSmallIntegerField(choices=[(0, 'Entero'), (1, 'Cadena de caracteres'), (2, 'Booleano')])),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TrendingTopic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('text', models.CharField(max_length=200)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Tweet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('id_twitter', models.BigIntegerField()),
                ('text', models.CharField(max_length=200)),
                ('is_scientific', models.NullBooleanField(default=None)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(related_query_name=b'answer', related_name='answers', to='tweets.Question'),
        ),
        migrations.AddField(
            model_name='answer',
            name='user',
            field=models.ForeignKey(related_query_name=b'answer', related_name='answers', to='accounts.UserProfile'),
        ),
        migrations.AlterUniqueTogether(
            name='answer',
            unique_together=set([('user', 'question', 'content_type', 'object_id')]),
        ),
    ]
