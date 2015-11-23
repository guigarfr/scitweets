# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0012_auto_20151123_1850'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='value_type',
            field=models.PositiveSmallIntegerField(default=1, choices=[(0, 'Integer'), (1, 'String'), (2, 'Boolean')]),
            preserve_default=False,
        ),
    ]
