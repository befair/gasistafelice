# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='homepage',
            name='resource_ctype',
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='role',
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='user',
        ),
        migrations.DeleteModel(
            name='HomePage',
        ),
        migrations.RemoveField(
            model_name='page',
            name='resource_ctype',
        ),
        migrations.RemoveField(
            model_name='page',
            name='role',
        ),
        migrations.RemoveField(
            model_name='page',
            name='user',
        ),
        migrations.DeleteModel(
            name='Page',
        ),
    ]
