# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicaldefaulttransition',
            name='state',
            field=models.IntegerField(db_index=True, null=True, verbose_name='state', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='historicaldefaulttransition',
            name='transition',
            field=models.IntegerField(db_index=True, null=True, verbose_name='transition', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='historicaldefaulttransition',
            name='workflow',
            field=models.IntegerField(db_index=True, null=True, verbose_name='workflow', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='historicalperson',
            name='address',
            field=models.IntegerField(db_index=True, null=True, verbose_name='main address', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='historicalperson',
            name='user',
            field=models.IntegerField(help_text='bind to a user if you want to give this person an access to the platform', null=True, verbose_name='User', db_index=True, blank=True),
            preserve_default=True,
        ),
    ]
