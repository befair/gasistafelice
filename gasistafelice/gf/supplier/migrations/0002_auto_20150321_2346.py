# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import gf.supplier.models


class Migration(migrations.Migration):

    dependencies = [
        ('supplier', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalproduct',
            name='category',
            field=models.IntegerField(default=gf.supplier.models.category_catchall, null=True, verbose_name='category', db_index=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='historicalproduct',
            name='mu',
            field=models.IntegerField(db_index=True, null=True, verbose_name='measure unit', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='historicalproduct',
            name='producer',
            field=models.IntegerField(db_index=True, null=True, verbose_name='producer', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='historicalproduct',
            name='pu',
            field=models.IntegerField(db_index=True, null=True, verbose_name='product unit', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='historicalsupplier',
            name='frontman',
            field=models.IntegerField(db_index=True, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='historicalsupplier',
            name='seat',
            field=models.IntegerField(db_index=True, null=True, verbose_name='seat', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='historicalsupplieragent',
            name='person',
            field=models.IntegerField(db_index=True, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='historicalsupplieragent',
            name='supplier',
            field=models.IntegerField(db_index=True, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='historicalsupplierstock',
            name='product',
            field=models.IntegerField(db_index=True, null=True, verbose_name='product', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='historicalsupplierstock',
            name='supplier',
            field=models.IntegerField(db_index=True, null=True, verbose_name='supplier', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='historicalsupplierstock',
            name='supplier_category',
            field=models.IntegerField(db_index=True, null=True, verbose_name='supplier category', blank=True),
            preserve_default=True,
        ),
    ]
