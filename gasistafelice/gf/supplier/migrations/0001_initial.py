# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.management import call_command
from django.db import models, migrations
import lib.fields.models
import gf.base.utils
import gf.supplier.models
import gf.base.models
import current_user.models
from django.conf import settings

import datetime, os
from decimal import Decimal

def create_default_category(apps, schema_editor):
    ProductCategory = apps.get_model('supplier', "ProductCategory")
    ProductCategory.objects.create(name=settings.DEFAULT_CATEGORY_CATCHALL)

def load_supplier_initial_data(apps, schema_editor):
    """
    Test if models have been initialized correctly and 
    load initial json data for suppliers.
    """

    ProductCategory = apps.get_model('supplier', "ProductCategory")
    ProductMU = apps.get_model('supplier', "ProductMU")
    ProductPU = apps.get_model('supplier', "ProductPU")

    call_command("loaddata", os.path.join(os.path.dirname(__file__), "initial_data.json"))

class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Certification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=128, verbose_name='name')),
                ('symbol', models.CharField(unique=True, max_length=5, verbose_name='symbol')),
                ('description', models.TextField(verbose_name='description', blank=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'certification',
                'verbose_name_plural': 'certifications',
            },
            bases=(models.Model, gf.base.models.PermissionResource),
        ),
        migrations.CreateModel(
            name='HistoricalCertification',
            fields=[
                ('id', models.IntegerField(db_index=True, verbose_name='ID', serialize=False, auto_created=True, blank=True)),
                ('name', models.CharField(max_length=128, verbose_name='name', db_index=True)),
                ('symbol', models.CharField(max_length=5, verbose_name='symbol', db_index=True)),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField(default=datetime.datetime.now)),
                ('history_type', models.CharField(max_length=1, choices=[(b'+', b'Created'), (b'~', b'Changed'), (b'-', b'Deleted')])),
                ('history_user', current_user.models.CurrentUserField(related_name='_certification_history', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-history_date',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HistoricalProduct',
            fields=[
                ('id', models.IntegerField(db_index=True, verbose_name='ID', serialize=False, auto_created=True, blank=True)),
                ('code', models.CharField(max_length=128, blank=True, help_text='Identification provided by the producer', null=True, verbose_name='code', db_index=True)),
                ('muppu', lib.fields.models.PrettyDecimalField(decimal_places=2, default=Decimal('1.00'), max_digits=6, help_text='How many measure units fit in your product unit?', null=True, verbose_name='measure unit per product unit')),
                ('muppu_is_variable', models.BooleanField(default=False, help_text='Check this if measure units per product unit is not exact', verbose_name='variable volume')),
                ('vat_percent', models.DecimalField(default=Decimal('0.21'), verbose_name='vat percent', max_digits=3, decimal_places=2)),
                ('name', models.CharField(max_length=128, verbose_name='name')),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('deleted', models.BooleanField(default=False, verbose_name='deleted')),
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
            name='HistoricalProductCategory',
            fields=[
                ('id', models.IntegerField(db_index=True, verbose_name='ID', serialize=False, auto_created=True, blank=True)),
                ('name', models.CharField(max_length=128, verbose_name='name', db_index=True)),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('image', models.ImageField(upload_to=gf.base.utils.get_resource_icon_path, null=True, verbose_name='image', blank=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField(default=datetime.datetime.now)),
                ('history_type', models.CharField(max_length=1, choices=[(b'+', b'Created'), (b'~', b'Changed'), (b'-', b'Deleted')])),
                ('history_user', current_user.models.CurrentUserField(related_name='_productcategory_history', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-history_date',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HistoricalProductMU',
            fields=[
                ('id', models.IntegerField(db_index=True, verbose_name='ID', serialize=False, auto_created=True, blank=True)),
                ('name', models.CharField(max_length=32, db_index=True)),
                ('symbol', models.CharField(max_length=5, db_index=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField(default=datetime.datetime.now)),
                ('history_type', models.CharField(max_length=1, choices=[(b'+', b'Created'), (b'~', b'Changed'), (b'-', b'Deleted')])),
                ('history_user', current_user.models.CurrentUserField(related_name='_productmu_history', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-history_date',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HistoricalProductPU',
            fields=[
                ('id', models.IntegerField(db_index=True, verbose_name='ID', serialize=False, auto_created=True, blank=True)),
                ('name', models.CharField(max_length=32, db_index=True)),
                ('symbol', models.CharField(max_length=5, db_index=True)),
                ('description', models.TextField(blank=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField(default=datetime.datetime.now)),
                ('history_type', models.CharField(max_length=1, choices=[(b'+', b'Created'), (b'~', b'Changed'), (b'-', b'Deleted')])),
                ('history_user', current_user.models.CurrentUserField(related_name='_productpu_history', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-history_date',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HistoricalSupplier',
            fields=[
                ('id', models.IntegerField(db_index=True, verbose_name='ID', serialize=False, auto_created=True, blank=True)),
                ('name', models.CharField(max_length=128, verbose_name='name')),
                ('vat_number', models.CharField(db_index=True, max_length=128, null=True, verbose_name='VAT number', blank=True)),
                ('ssn', models.CharField(db_index=True, max_length=128, null=True, verbose_name='Social Security Number', blank=True)),
                ('website', models.URLField(verbose_name='web site', blank=True)),
                ('flavour', models.CharField(default=b'COMPANY', max_length=128, verbose_name='flavour', choices=[(b'COMPANY', 'Company'), (b'COOPERATING', 'Cooperating'), (b'FREELANCE', 'Freelance')])),
                ('n_employers', models.PositiveIntegerField(default=None, null=True, verbose_name='amount of employers', blank=True)),
                ('logo', models.ImageField(upload_to=gf.base.utils.get_resource_icon_path, null=True, verbose_name='logo', blank=True)),
                ('iban', models.CharField(max_length=64, verbose_name='IBAN', blank=True)),
                ('description', models.TextField(default=b'', verbose_name='description', blank=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField(default=datetime.datetime.now)),
                ('history_type', models.CharField(max_length=1, choices=[(b'+', b'Created'), (b'~', b'Changed'), (b'-', b'Deleted')])),
                ('frontman', models.ForeignKey(related_name='historicalsupplier_frontman_set', to='base.Person', null=True)),
                ('history_user', current_user.models.CurrentUserField(related_name='_supplier_history', to=settings.AUTH_USER_MODEL, null=True)),
                ('seat', models.ForeignKey(verbose_name='seat', blank=True, to='base.Place', null=True)),
            ],
            options={
                'ordering': ('-history_date',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HistoricalSupplierAgent',
            fields=[
                ('id', models.IntegerField(db_index=True, verbose_name='ID', serialize=False, auto_created=True, blank=True)),
                ('job_title', models.CharField(max_length=256, blank=True)),
                ('job_description', models.TextField(blank=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField(default=datetime.datetime.now)),
                ('history_type', models.CharField(max_length=1, choices=[(b'+', b'Created'), (b'~', b'Changed'), (b'-', b'Deleted')])),
                ('history_user', current_user.models.CurrentUserField(related_name='_supplieragent_history', to=settings.AUTH_USER_MODEL, null=True)),
                ('person', models.ForeignKey(to='base.Person')),
            ],
            options={
                'ordering': ('-history_date',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HistoricalSupplierStock',
            fields=[
                ('id', models.IntegerField(db_index=True, verbose_name='ID', serialize=False, auto_created=True, blank=True)),
                ('image', models.ImageField(upload_to=gf.base.utils.get_resource_icon_path, null=True, verbose_name='image', blank=True)),
                ('price', lib.fields.models.CurrencyField(verbose_name='price', max_digits=10, decimal_places=4)),
                ('code', models.CharField(help_text='Product supplier identifier', max_length=128, null=True, verbose_name='code', blank=True)),
                ('amount_available', models.PositiveIntegerField(default=1000000000, verbose_name='availability')),
                ('units_minimum_amount', models.PositiveIntegerField(default=1, verbose_name='units minimum amount')),
                ('units_per_box', lib.fields.models.PrettyDecimalField(default=1, verbose_name='units per box', max_digits=5, decimal_places=2)),
                ('detail_minimum_amount', lib.fields.models.PrettyDecimalField(decimal_places=2, default=1, max_digits=5, blank=True, null=True, verbose_name='detail minimum amount')),
                ('detail_step', lib.fields.models.PrettyDecimalField(decimal_places=2, default=1, max_digits=5, blank=True, null=True, verbose_name='detail step')),
                ('delivery_notes', models.TextField(default=b'', verbose_name='delivery notes', blank=True)),
                ('deleted', models.BooleanField(default=False, verbose_name='deleted')),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField(default=datetime.datetime.now)),
                ('history_type', models.CharField(max_length=1, choices=[(b'+', b'Created'), (b'~', b'Changed'), (b'-', b'Deleted')])),
                ('history_user', current_user.models.CurrentUserField(related_name='_supplierstock_history', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-history_date',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(null=True, max_length=128, blank=True, help_text='Identification provided by the producer', unique=True, verbose_name='code')),
                ('muppu', lib.fields.models.PrettyDecimalField(decimal_places=2, default=Decimal('1.00'), max_digits=6, help_text='How many measure units fit in your product unit?', null=True, verbose_name='measure unit per product unit')),
                ('muppu_is_variable', models.BooleanField(default=False, help_text='Check this if measure units per product unit is not exact', verbose_name='variable volume')),
                ('vat_percent', models.DecimalField(default=Decimal('0.21'), verbose_name='vat percent', max_digits=3, decimal_places=2)),
                ('name', models.CharField(max_length=128, verbose_name='name')),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('deleted', models.BooleanField(default=False, verbose_name='deleted')),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'product',
                'verbose_name_plural': 'products',
            },
            bases=(models.Model, gf.base.models.PermissionResource),
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=128, verbose_name='name')),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('image', models.ImageField(upload_to=gf.base.utils.get_resource_icon_path, null=True, verbose_name='image', blank=True)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'Product category',
                'verbose_name_plural': 'Product categories',
            },
            bases=(models.Model, gf.base.models.PermissionResource),
        ),
        migrations.CreateModel(
            name='ProductMU',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=32)),
                ('symbol', models.CharField(unique=True, max_length=5)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'measure unit',
                'verbose_name_plural': 'measure units',
            },
            bases=(models.Model, gf.base.models.PermissionResource),
        ),
        migrations.CreateModel(
            name='ProductPU',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=32)),
                ('symbol', models.CharField(unique=True, max_length=5)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'product unit',
                'verbose_name_plural': 'product units',
            },
            bases=(models.Model, gf.base.models.PermissionResource),
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128, verbose_name='name')),
                ('vat_number', models.CharField(max_length=128, unique=True, null=True, verbose_name='VAT number', blank=True)),
                ('ssn', models.CharField(max_length=128, unique=True, null=True, verbose_name='Social Security Number', blank=True)),
                ('website', models.URLField(verbose_name='web site', blank=True)),
                ('flavour', models.CharField(default=b'COMPANY', max_length=128, verbose_name='flavour', choices=[(b'COMPANY', 'Company'), (b'COOPERATING', 'Cooperating'), (b'FREELANCE', 'Freelance')])),
                ('n_employers', models.PositiveIntegerField(default=None, null=True, verbose_name='amount of employers', blank=True)),
                ('logo', models.ImageField(upload_to=gf.base.utils.get_resource_icon_path, null=True, verbose_name='logo', blank=True)),
                ('iban', models.CharField(max_length=64, verbose_name='IBAN', blank=True)),
                ('description', models.TextField(default=b'', verbose_name='description', blank=True)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'supplier',
                'verbose_name_plural': 'suppliers',
            },
            bases=(models.Model, gf.base.models.PermissionResource),
        ),
        migrations.CreateModel(
            name='SupplierAgent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('job_title', models.CharField(max_length=256, blank=True)),
                ('job_description', models.TextField(blank=True)),
                ('person', models.ForeignKey(to='base.Person')),
                ('supplier', models.ForeignKey(to='supplier.Supplier')),
            ],
            options={
                'verbose_name': 'supplier agent',
                'verbose_name_plural': 'supplier agents',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SupplierConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('receive_order_via_email_on_finalize', models.BooleanField(default=True, help_text='Check this option if you want to let the GAS be able to send order via mail on finalize', verbose_name='receive order via email on finalize')),
                ('use_custom_categories', models.BooleanField(default=False, help_text='Check this option if you use your own categories', verbose_name='use custom categories')),
                ('products_made_by_set', models.ManyToManyField(help_text='Select here producers of products you sell. YOU will be always enabled in this list', to='supplier.Supplier', verbose_name='products made by')),
                ('supplier', models.OneToOneField(related_name='config', to='supplier.Supplier')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SupplierProductCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128, verbose_name='name')),
                ('sorting', models.PositiveIntegerField(null=True, blank=True)),
                ('supplier', models.ForeignKey(to='supplier.Supplier')),
            ],
            options={
                'ordering': ('supplier', 'sorting'),
                'verbose_name': 'supplier product category',
                'verbose_name_plural': 'supplier product categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SupplierStock',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(upload_to=gf.base.utils.get_resource_icon_path, null=True, verbose_name='image', blank=True)),
                ('price', lib.fields.models.CurrencyField(verbose_name='price', max_digits=10, decimal_places=4)),
                ('code', models.CharField(help_text='Product supplier identifier', max_length=128, null=True, verbose_name='code', blank=True)),
                ('amount_available', models.PositiveIntegerField(default=1000000000, verbose_name='availability')),
                ('units_minimum_amount', models.PositiveIntegerField(default=1, verbose_name='units minimum amount')),
                ('units_per_box', lib.fields.models.PrettyDecimalField(default=1, verbose_name='units per box', max_digits=5, decimal_places=2)),
                ('detail_minimum_amount', lib.fields.models.PrettyDecimalField(decimal_places=2, default=1, max_digits=5, blank=True, null=True, verbose_name='detail minimum amount')),
                ('detail_step', lib.fields.models.PrettyDecimalField(decimal_places=2, default=1, max_digits=5, blank=True, null=True, verbose_name='detail step')),
                ('delivery_notes', models.TextField(default=b'', verbose_name='delivery notes', blank=True)),
                ('deleted', models.BooleanField(default=False, verbose_name='deleted')),
                ('product', models.ForeignKey(related_name='stock_set', verbose_name='product', to='supplier.Product')),
                ('supplier', models.ForeignKey(related_name='stock_set', verbose_name='supplier', to='supplier.Supplier')),
                ('supplier_category', models.ForeignKey(verbose_name='supplier category', blank=True, to='supplier.SupplierProductCategory', null=True)),
            ],
            options={
                'ordering': ('supplier_category__sorting', 'product__category'),
                'verbose_name': 'supplier stock',
                'verbose_name_plural': 'supplier stocks',
            },
            bases=(models.Model, gf.base.models.PermissionResource),
        ),
        migrations.CreateModel(
            name='UnitsConversion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', lib.fields.models.PrettyDecimalField(default=1, verbose_name='amount', max_digits=10, decimal_places=4)),
                ('dst', models.ForeignKey(related_name='dst_conversion_set', verbose_name='destination', to='supplier.ProductMU')),
                ('src', models.ForeignKey(related_name='src_conversion_set', verbose_name='source', to='supplier.ProductMU')),
            ],
            options={
                'ordering': ('src', 'dst', 'amount'),
                'verbose_name': 'units conversion',
                'verbose_name_plural': 'units conversions',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='unitsconversion',
            unique_together=set([('src', 'dst')]),
        ),
        migrations.RunPython(load_supplier_initial_data),
        migrations.AddField(
            model_name='supplier',
            name='agent_set',
            field=models.ManyToManyField(to='base.Person', through='supplier.SupplierAgent'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='supplier',
            name='certifications',
            field=models.ManyToManyField(to='supplier.Certification', null=True, verbose_name='certifications', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='supplier',
            name='contact_set',
            field=models.ManyToManyField(to='base.Contact', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='supplier',
            name='frontman',
            field=models.ForeignKey(related_name='supplier_frontman_set', to='base.Person', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='supplier',
            name='seat',
            field=models.ForeignKey(verbose_name='seat', blank=True, to='base.Place', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(related_name='product_set', default=gf.supplier.models.category_catchall, verbose_name='category', blank=True, to='supplier.ProductCategory'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='mu',
            field=models.ForeignKey(verbose_name='measure unit', blank=True, to='supplier.ProductMU', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='producer',
            field=models.ForeignKey(related_name='produced_product_set', verbose_name='producer', to='supplier.Supplier'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='pu',
            field=models.ForeignKey(verbose_name='product unit', to='supplier.ProductPU'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='historicalsupplierstock',
            name='product',
            field=models.ForeignKey(related_name='historicalstock_set', verbose_name='product', to='supplier.Product'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='historicalsupplierstock',
            name='supplier',
            field=models.ForeignKey(related_name='historicalstock_set', verbose_name='supplier', to='supplier.Supplier'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='historicalsupplierstock',
            name='supplier_category',
            field=models.ForeignKey(verbose_name='supplier category', blank=True, to='supplier.SupplierProductCategory', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='historicalsupplieragent',
            name='supplier',
            field=models.ForeignKey(to='supplier.Supplier'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='historicalproduct',
            name='category',
            field=models.ForeignKey(related_name='historicalproduct_set', default=gf.supplier.models.category_catchall, verbose_name='category', blank=True, to='supplier.ProductCategory'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='historicalproduct',
            name='history_user',
            field=current_user.models.CurrentUserField(related_name='_product_history', to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='historicalproduct',
            name='mu',
            field=models.ForeignKey(verbose_name='measure unit', blank=True, to='supplier.ProductMU', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='historicalproduct',
            name='producer',
            field=models.ForeignKey(related_name='historicalproduced_product_set', verbose_name='producer', to='supplier.Supplier'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='historicalproduct',
            name='pu',
            field=models.ForeignKey(verbose_name='product unit', to='supplier.ProductPU'),
            preserve_default=True,
        ),
    ]
