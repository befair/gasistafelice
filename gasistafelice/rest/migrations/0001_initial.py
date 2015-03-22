# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
        ('flexi_auth', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlockConfiguration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('blocktype', models.CharField(db_index=True, max_length=255, verbose_name='Rest block name', blank=True)),
                ('resource_type', models.CharField(max_length=255, verbose_name='Resource type', db_index=True)),
                ('resource_id', models.CharField(max_length=255, verbose_name='Resource key', db_index=True)),
                ('page', models.SmallIntegerField(default=1, verbose_name='user page')),
                ('position', models.SmallIntegerField(default=0, verbose_name='page position')),
                ('confdata', models.TextField(default=b'', null=True, verbose_name='Configuration data')),
                ('user', models.ForeignKey(verbose_name='User', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'blockconfiguration',
                'verbose_name': 'Block configuration data',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HomePage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('resource_id', models.PositiveIntegerField()),
                ('resource_ctype', models.ForeignKey(to='contenttypes.ContentType')),
                ('role', models.ForeignKey(to='flexi_auth.ParamRole')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('resource_id', models.PositiveIntegerField(null=True, blank=True)),
                ('confdata', models.TextField(default=b'', null=True, verbose_name='Configuration data')),
                ('resource_ctype', models.ForeignKey(to='contenttypes.ContentType')),
                ('role', models.ForeignKey(to='flexi_auth.ParamRole')),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
