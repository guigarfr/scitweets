# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0002_auto_20151115_2143'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tweet',
            old_name='created_at',
            new_name='created',
        ),
        migrations.RenameField(
            model_name='tweet',
            old_name='updated_at',
            new_name='updated',
        ),
        migrations.RenameField(
            model_name='tweetyesnoanswer',
            old_name='created_at',
            new_name='created',
        ),
        migrations.RenameField(
            model_name='tweetyesnoanswer',
            old_name='updated_at',
            new_name='updated',
        ),
    ]
