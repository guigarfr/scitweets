# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0010_auto_20151123_1844'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answervalue',
            name='value_type',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Integer'), (1, 'String'), (2, 'Boolean')]),
        ),
        migrations.AlterField(
            model_name='question',
            name='answer_value_type',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Integer'), (1, 'String'), (2, 'Boolean')]),
        ),
    ]
