# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0013_answer_value_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='object_id',
        ),
    ]
