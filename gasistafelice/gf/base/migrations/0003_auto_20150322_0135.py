# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_auto_20150321_2346'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicaldefaulttransition',
            name='history_user',
        ),
        migrations.DeleteModel(
            name='HistoricalDefaultTransition',
        ),
    ]
