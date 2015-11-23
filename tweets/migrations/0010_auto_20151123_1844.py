# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0009_remove_question_answer_values'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answervalue',
            name='value_type',
            field=models.PositiveSmallIntegerField(choices=[(int, b'Entero'), (str, b'String'), (bool, b'Booleano')]),
        ),
        migrations.AlterField(
            model_name='question',
            name='answer_value_type',
            field=models.PositiveSmallIntegerField(choices=[(int, b'Entero'), (str, b'String'), (bool, b'Booleano')]),
        ),
    ]
