# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0003_auto_20151115_2149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweetyesnoanswer',
            name='user',
            field=models.ForeignKey(related_query_name=b'answer', related_name='answers', to='accounts.UserProfile'),
        ),
    ]
