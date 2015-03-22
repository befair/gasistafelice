# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import gf.gas.models.base


class Migration(migrations.Migration):

    dependencies = [
        ('gas', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicaldelivery',
            name='place',
            field=models.IntegerField(help_text='where the order will be delivered by supplier', null=True, verbose_name='place', db_index=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='historicalgas',
            name='des',
            field=models.IntegerField(db_index=True, null=True, verbose_name='des', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='historicalgas',
            name='headquarter',
            field=models.IntegerField(help_text='main address', null=True, verbose_name='headquarter', db_index=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='historicalgas',
            name='orders_email_contact',
            field=models.IntegerField(db_index=True, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='historicalgasactivist',
            name='gas',
            field=models.IntegerField(db_index=True, null=True, verbose_name='gas', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='historicalgasactivist',
            name='person',
            field=models.IntegerField(db_index=True, null=True, verbose_name='person', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='historicalgasconfig',
            name='default_delivery_place',
            field=models.IntegerField(help_text='to specify if different from withdrawal place', null=True, verbose_name='default delivery place', db_index=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='historicalgasconfig',
            name='default_withdrawal_place',
            field=models.IntegerField(help_text='to specify if different from headquarter', null=True, verbose_name='default withdrawal place', db_index=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='historicalgasconfig',
            name='default_workflow_gasmember_order',
            field=models.IntegerField(default=gf.gas.models.base.get_gasmember_order_default, null=True, editable=False, db_index=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='historicalgasconfig',
            name='default_workflow_gassupplier_order',
            field=models.IntegerField(default=gf.gas.models.base.get_supplier_order_default, null=True, editable=False, db_index=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='historicalgasconfig',
            name='gas',
            field=models.IntegerField(db_index=True, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='historicalgasmember',
            name='gas',
            field=models.IntegerField(db_index=True, null=True, verbose_name='gas', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='historicalgasmember',
            name='person',
            field=models.IntegerField(db_index=True, null=True, verbose_name='person', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='historicalgasmemberorder',
            name='ordered_product',
            field=models.IntegerField(db_index=True, null=True, verbose_name='order product', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='historicalgasmemberorder',
            name='purchaser',
            field=models.IntegerField(db_index=True, null=True, verbose_name='purchaser', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='historicalgassupplierorder',
            name='delivery',
            field=models.IntegerField(db_index=True, null=True, verbose_name='Delivery', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='historicalgassupplierorder',
            name='delivery_referrer_person',
            field=models.IntegerField(db_index=True, null=True, verbose_name='delivery referrer', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='historicalgassupplierorder',
            name='pact',
            field=models.IntegerField(db_index=True, null=True, verbose_name='pact', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='historicalgassupplierorder',
            name='referrer_person',
            field=models.IntegerField(db_index=True, null=True, verbose_name='order referrer', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='historicalgassupplierorder',
            name='root_plan',
            field=models.IntegerField(default=None, blank=True, help_text='Order was generated by another order', null=True, verbose_name='planned order', db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='historicalgassupplierorder',
            name='withdrawal',
            field=models.IntegerField(db_index=True, null=True, verbose_name='Withdrawal', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='historicalgassupplierorder',
            name='withdrawal_referrer_person',
            field=models.IntegerField(db_index=True, null=True, verbose_name='withdrawal referrer', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='historicalgassupplierorderproduct',
            name='gasstock',
            field=models.IntegerField(db_index=True, null=True, verbose_name='gas stock', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='historicalgassupplierorderproduct',
            name='order',
            field=models.IntegerField(db_index=True, null=True, verbose_name='order', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='historicalgassuppliersolidalpact',
            name='default_delivery_place',
            field=models.IntegerField(db_index=True, null=True, verbose_name='Default delivery place', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='historicalgassuppliersolidalpact',
            name='gas',
            field=models.IntegerField(db_index=True, null=True, verbose_name='GAS', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='historicalgassuppliersolidalpact',
            name='supplier',
            field=models.IntegerField(db_index=True, null=True, verbose_name='Supplier', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='historicalgassupplierstock',
            name='pact',
            field=models.IntegerField(db_index=True, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='historicalgassupplierstock',
            name='stock',
            field=models.IntegerField(db_index=True, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='historicalwithdrawal',
            name='place',
            field=models.IntegerField(help_text='where the order will be withdrawn by GAS members', null=True, db_index=True, blank=True),
            preserve_default=True,
        ),
    ]
