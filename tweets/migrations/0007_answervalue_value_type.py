# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0006_answervalue_hashtag_question'),
    ]

    operations = [
        migrations.AddField(
            model_name='answervalue',
            name='value_type',
            field=models.PositiveSmallIntegerField(default=3, choices=[(1, int), (2, str), (3, bool)]),
            preserve_default=False,
        ),
    ]
