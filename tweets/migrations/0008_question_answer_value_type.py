# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0007_answervalue_value_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='answer_value_type',
            field=models.PositiveSmallIntegerField(default=3, choices=[(1, int), (2, str), (3, bool)]),
            preserve_default=False,
        ),
    ]
