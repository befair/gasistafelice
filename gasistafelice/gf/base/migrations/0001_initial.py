# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import gf.base.models
import gf.base.utils
import current_user.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('workflows', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('flavour', models.CharField(default=b'EMAIL', max_length=32, verbose_name='flavour', choices=[(b'PHONE', 'PHONE'), (b'EMAIL', 'EMAIL'), (b'FAX', 'FAX')])),
                ('value', models.CharField(max_length=256, verbose_name='value')),
                ('is_preferred', models.BooleanField(default=False, verbose_name='preferred')),
                ('description', models.CharField(default=b'', max_length=128, verbose_name='description', blank=True)),
            ],
            options={
                'db_table': 'base_contact',
                'verbose_name': 'contact',
                'verbose_name_plural': 'contacts',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DefaultTransition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('state', models.ForeignKey(verbose_name='state', to='workflows.State')),
                ('transition', models.ForeignKey(verbose_name='transition', to='workflows.Transition')),
                ('workflow', models.ForeignKey(related_name='default_transition_set', verbose_name='workflow', to='workflows.Workflow')),
            ],
            options={
                'db_table': 'base_defaulttransition',
                'verbose_name': 'default transition',
                'verbose_name_plural': 'default transitions',
            },
            bases=(models.Model, gf.base.models.PermissionResource),
        ),
        migrations.CreateModel(
            name='HistoricalContact',
            fields=[
                ('id', models.IntegerField(db_index=True, verbose_name='ID', serialize=False, auto_created=True, blank=True)),
                ('flavour', models.CharField(default=b'EMAIL', max_length=32, verbose_name='flavour', choices=[(b'PHONE', 'PHONE'), (b'EMAIL', 'EMAIL'), (b'FAX', 'FAX')])),
                ('value', models.CharField(max_length=256, verbose_name='value')),
                ('is_preferred', models.BooleanField(default=False, verbose_name='preferred')),
                ('description', models.CharField(default=b'', max_length=128, verbose_name='description', blank=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField(default=datetime.datetime.now)),
                ('history_type', models.CharField(max_length=1, choices=[(b'+', b'Created'), (b'~', b'Changed'), (b'-', b'Deleted')])),
                ('history_user', current_user.models.CurrentUserField(related_name='_contact_history', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-history_date',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HistoricalDefaultTransition',
            fields=[
                ('id', models.IntegerField(db_index=True, verbose_name='ID', serialize=False, auto_created=True, blank=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField(default=datetime.datetime.now)),
                ('history_type', models.CharField(max_length=1, choices=[(b'+', b'Created'), (b'~', b'Changed'), (b'-', b'Deleted')])),
                ('history_user', current_user.models.CurrentUserField(related_name='_defaulttransition_history', to=settings.AUTH_USER_MODEL, null=True)),
                ('state', models.ForeignKey(verbose_name='state', to='workflows.State')),
                ('transition', models.ForeignKey(verbose_name='transition', to='workflows.Transition')),
                ('workflow', models.ForeignKey(related_name='historicaldefault_transition_set', verbose_name='workflow', to='workflows.Workflow')),
            ],
            options={
                'ordering': ('-history_date',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HistoricalPerson',
            fields=[
                ('id', models.IntegerField(db_index=True, verbose_name='ID', serialize=False, auto_created=True, blank=True)),
                ('name', models.CharField(max_length=128, verbose_name='name')),
                ('surname', models.CharField(max_length=128, verbose_name='surname')),
                ('display_name', models.CharField(max_length=128, verbose_name='display name', blank=True)),
                ('ssn', models.CharField(editable=False, max_length=128, blank=True, help_text='Write your social security number here', null=True, verbose_name='Social Security Number', db_index=True)),
                ('avatar', models.ImageField(upload_to=gf.base.utils.get_resource_icon_path, null=True, verbose_name='avatar', blank=True)),
                ('website', models.URLField(verbose_name='web site', blank=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField(default=datetime.datetime.now)),
                ('history_type', models.CharField(max_length=1, choices=[(b'+', b'Created'), (b'~', b'Changed'), (b'-', b'Deleted')])),
            ],
            options={
                'ordering': ('-history_date',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HistoricalPlace',
            fields=[
                ('id', models.IntegerField(db_index=True, verbose_name='ID', serialize=False, auto_created=True, blank=True)),
                ('name', models.CharField(help_text='You can avoid to specify a name if you specify an address', max_length=128, verbose_name='name', blank=True)),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('address', models.CharField(max_length=128, verbose_name='address', blank=True)),
                ('zipcode', models.CharField(max_length=128, verbose_name='Zip code', blank=True)),
                ('city', models.CharField(max_length=128, verbose_name='city')),
                ('province', models.CharField(help_text='Insert the province code here (max 2 char)', max_length=2, verbose_name='province')),
                ('lon', models.FloatField(null=True, verbose_name='lon', blank=True)),
                ('lat', models.FloatField(null=True, verbose_name='lat', blank=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField(default=datetime.datetime.now)),
                ('history_type', models.CharField(max_length=1, choices=[(b'+', b'Created'), (b'~', b'Changed'), (b'-', b'Deleted')])),
                ('history_user', current_user.models.CurrentUserField(related_name='_place_history', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-history_date',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128, verbose_name='name')),
                ('surname', models.CharField(max_length=128, verbose_name='surname')),
                ('display_name', models.CharField(max_length=128, verbose_name='display name', blank=True)),
                ('ssn', models.CharField(null=True, editable=False, max_length=128, blank=True, help_text='Write your social security number here', unique=True, verbose_name='Social Security Number')),
                ('avatar', models.ImageField(upload_to=gf.base.utils.get_resource_icon_path, null=True, verbose_name='avatar', blank=True)),
                ('website', models.URLField(verbose_name='web site', blank=True)),
            ],
            options={
                'ordering': ('display_name',),
                'db_table': 'base_person',
                'verbose_name': 'person',
                'verbose_name_plural': 'people',
            },
            bases=(models.Model, gf.base.models.PermissionResource),
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='You can avoid to specify a name if you specify an address', max_length=128, verbose_name='name', blank=True)),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('address', models.CharField(max_length=128, verbose_name='address', blank=True)),
                ('zipcode', models.CharField(max_length=128, verbose_name='Zip code', blank=True)),
                ('city', models.CharField(max_length=128, verbose_name='city')),
                ('province', models.CharField(help_text='Insert the province code here (max 2 char)', max_length=2, verbose_name='province')),
                ('lon', models.FloatField(null=True, verbose_name='lon', blank=True)),
                ('lat', models.FloatField(null=True, verbose_name='lat', blank=True)),
            ],
            options={
                'ordering': ('name', 'address', 'city'),
                'db_table': 'base_place',
                'verbose_name': 'place',
                'verbose_name_plural': 'places',
            },
            bases=(models.Model, gf.base.models.PermissionResource),
        ),
        migrations.AddField(
            model_name='person',
            name='address',
            field=models.ForeignKey(verbose_name='main address', blank=True, to='base.Place', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='person',
            name='contact_set',
            field=models.ManyToManyField(to='base.Contact', null=True, verbose_name='contacts', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='person',
            name='user',
            field=models.OneToOneField(null=True, to=settings.AUTH_USER_MODEL, blank=True, help_text='bind to a user if you want to give this person an access to the platform', verbose_name='User'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='historicalperson',
            name='address',
            field=models.ForeignKey(verbose_name='main address', blank=True, to='base.Place', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='historicalperson',
            name='history_user',
            field=current_user.models.CurrentUserField(related_name='_person_history', to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='historicalperson',
            name='user',
            field=models.OneToOneField(null=True, to=settings.AUTH_USER_MODEL, blank=True, help_text='bind to a user if you want to give this person an access to the platform', verbose_name='User'),
            preserve_default=True,
        ),
    ]
