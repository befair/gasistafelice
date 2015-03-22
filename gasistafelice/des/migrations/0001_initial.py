# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import gf.base.models
import gf.base.utils
from django.conf import settings

def create_default_site(apps, schema_editor):
    Site = apps.get_model("sites", "Site")
    Site.objects.create(
        domain=settings.INIT_OPTIONS["domain"], 
        name=settings.INIT_OPTIONS["sitename"]
    )

class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_default_site),
        migrations.CreateModel(
            name='DES',
            fields=[
                ('site_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='sites.Site')),
                ('cfg_time', models.PositiveIntegerField()),
                ('logo', models.ImageField(null=True, upload_to=gf.base.utils.get_resource_icon_path, blank=True)),
                ('info_people_set', models.ManyToManyField(to='base.Person', null=True, blank=True)),
            ],
            options={
                'verbose_name': 'site',
                'verbose_name_plural': 'sites',
            },
            bases=('sites.site', gf.base.models.PermissionResource),
        ),
        migrations.CreateModel(
            name='Siteattr',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=63, verbose_name='name', db_index=True)),
                ('value', models.TextField(verbose_name='value', blank=True)),
                ('atype', models.CharField(max_length=63, verbose_name='type')),
                ('descr', models.CharField(default=b'', max_length=255, blank=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'environment variable',
                'verbose_name_plural': 'environment variables',
            },
            bases=(models.Model,),
        ),
    ]
