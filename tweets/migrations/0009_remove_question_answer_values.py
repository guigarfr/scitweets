# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0008_question_answer_value_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='answer_values',
        ),
    ]
