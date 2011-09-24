# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'HistoricalGAS'
        db.create_table('gas_historicalgas', (
            ('id', self.gf('django.db.models.fields.IntegerField')(db_index=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('id_in_des', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('logo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='historicalgas_set', null=True, to=orm['bank.Account'])),
            ('liquidity', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='historicalgas_set2', null=True, to=orm['bank.Account'])),
            ('birthday', self.gf('django.db.models.fields.DateField')()),
            ('vat', self.gf('django.db.models.fields.CharField')(max_length=11, null=True, blank=True)),
            ('ssn', self.gf('django.db.models.fields.CharField')(max_length=16, null=True)),
            ('email_gas', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('email_referrer', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('association_act', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('intent_act', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('note', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('history_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('history_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('history_user', self.gf('current_user.models.CurrentUserField')(related_name='_gas_history', null=True, to=orm['auth.User'])),
            ('history_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('gas', ['HistoricalGAS'])

        # Adding model 'GAS'
        db.create_table('gas_gas', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('id_in_des', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('logo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='gas_set', null=True, to=orm['bank.Account'])),
            ('liquidity', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='gas_set2', null=True, to=orm['bank.Account'])),
            ('birthday', self.gf('django.db.models.fields.DateField')()),
            ('vat', self.gf('django.db.models.fields.CharField')(max_length=11, null=True, blank=True)),
            ('ssn', self.gf('django.db.models.fields.CharField')(max_length=16, null=True)),
            ('email_gas', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('email_referrer', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('association_act', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('intent_act', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('note', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('gas', ['GAS'])

        # Adding model 'HistoricalGASMember'
        db.create_table('gas_historicalgasmember', (
            ('id', self.gf('django.db.models.fields.IntegerField')(db_index=True, blank=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.Person'])),
            ('gas', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gas.GAS'])),
            ('id_in_gas', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bank.Account'])),
            ('history_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('history_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('history_user', self.gf('current_user.models.CurrentUserField')(related_name='_gasmember_history', null=True, to=orm['auth.User'])),
            ('history_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('gas', ['HistoricalGASMember'])

        # Adding model 'GASMember'
        db.create_table('gas_gasmember', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.Person'])),
            ('gas', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gas.GAS'])),
            ('id_in_gas', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bank.Account'])),
        ))
        db.send_create_signal('gas', ['GASMember'])

        # Adding M2M table for field available_for_roles on 'GASMember'
        db.create_table('gas_gasmember_available_for_roles', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('gasmember', models.ForeignKey(orm['gas.gasmember'], null=False)),
            ('role', models.ForeignKey(orm['permissions.role'], null=False))
        ))
        db.create_unique('gas_gasmember_available_for_roles', ['gasmember_id', 'role_id'])

        # Adding M2M table for field roles on 'GASMember'
        db.create_table('gas_gasmember_roles', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('gasmember', models.ForeignKey(orm['gas.gasmember'], null=False)),
            ('role', models.ForeignKey(orm['permissions.role'], null=False))
        ))
        db.create_unique('gas_gasmember_roles', ['gasmember_id', 'role_id'])

        # Adding model 'HistoricalGASSupplierSolidalPact'
        db.create_table('gas_historicalgassuppliersolidalpact', (
            ('id', self.gf('django.db.models.fields.IntegerField')(db_index=True, blank=True)),
            ('gas', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gas.GAS'])),
            ('supplier', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['supplier.Supplier'])),
            ('date_signed', self.gf('django.db.models.fields.DateField')()),
            ('order_minimum_amount', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('order_delivery_cost', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('order_deliver_interval', self.gf('django.db.models.fields.TimeField')()),
            ('order_price_percent_update', self.gf('django.db.models.fields.FloatField')()),
            ('default_withdrawal_day', self.gf('django.db.models.fields.CharField')(max_length=16, null=True)),
            ('default_withdrawal_time', self.gf('django.db.models.fields.TimeField')(null=True)),
            ('default_withdrawal_place', self.gf('django.db.models.fields.related.ForeignKey')(related_name='historicaldefault_for_solidal_pact_set', to=orm['base.Place'])),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bank.Account'])),
            ('history_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('history_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('history_user', self.gf('current_user.models.CurrentUserField')(related_name='_gassuppliersolidalpact_history', null=True, to=orm['auth.User'])),
            ('history_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('gas', ['HistoricalGASSupplierSolidalPact'])

        # Adding model 'GASSupplierSolidalPact'
        db.create_table('gas_gassuppliersolidalpact', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('gas', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gas.GAS'])),
            ('supplier', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['supplier.Supplier'])),
            ('date_signed', self.gf('django.db.models.fields.DateField')()),
            ('order_minimum_amount', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('order_delivery_cost', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('order_deliver_interval', self.gf('django.db.models.fields.TimeField')()),
            ('order_price_percent_update', self.gf('django.db.models.fields.FloatField')()),
            ('default_withdrawal_day', self.gf('django.db.models.fields.CharField')(max_length=16, null=True)),
            ('default_withdrawal_time', self.gf('django.db.models.fields.TimeField')(null=True)),
            ('default_withdrawal_place', self.gf('django.db.models.fields.related.ForeignKey')(related_name='default_for_solidal_pact_set', to=orm['base.Place'])),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bank.Account'])),
        ))
        db.send_create_signal('gas', ['GASSupplierSolidalPact'])

        # Adding M2M table for field supplier_gas_catalog on 'GASSupplierSolidalPact'
        db.create_table('gas_gassuppliersolidalpact_supplier_gas_catalog', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('gassuppliersolidalpact', models.ForeignKey(orm['gas.gassuppliersolidalpact'], null=False)),
            ('product', models.ForeignKey(orm['supplier.product'], null=False))
        ))
        db.create_unique('gas_gassuppliersolidalpact_supplier_gas_catalog', ['gassuppliersolidalpact_id', 'product_id'])

        # Adding model 'HistoricalGASSupplierStock'
        db.create_table('gas_historicalgassupplierstock', (
            ('id', self.gf('django.db.models.fields.IntegerField')(db_index=True, blank=True)),
            ('gas', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gas.GAS'])),
            ('supplier_stock', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['supplier.SupplierStock'])),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('order_minimum_amount', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('order_step', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('history_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('history_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('history_user', self.gf('current_user.models.CurrentUserField')(related_name='_gassupplierstock_history', null=True, to=orm['auth.User'])),
            ('history_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('gas', ['HistoricalGASSupplierStock'])

        # Adding model 'GASSupplierStock'
        db.create_table('gas_gassupplierstock', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('gas', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gas.GAS'])),
            ('supplier_stock', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['supplier.SupplierStock'])),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('order_minimum_amount', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('order_step', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('gas', ['GASSupplierStock'])

        # Adding model 'HistoricalGASSupplierOrder'
        db.create_table('gas_historicalgassupplierorder', (
            ('id', self.gf('django.db.models.fields.IntegerField')(db_index=True, blank=True)),
            ('gas', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gas.GAS'])),
            ('supplier', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['supplier.Supplier'])),
            ('date_start', self.gf('django.db.models.fields.DateTimeField')()),
            ('date_end', self.gf('django.db.models.fields.DateTimeField')()),
            ('delivery', self.gf('django.db.models.fields.related.ForeignKey')(related_name='historicalsupplier_order_set', to=orm['gas.Delivery'])),
            ('order_minimum_amount', self.gf('gasistafelice.base.fields.CurrencyField')(null=True, max_digits=10, decimal_places=4, blank=True)),
            ('withdrawal', self.gf('django.db.models.fields.related.ForeignKey')(related_name='historicalsupplier_order_set', to=orm['gas.Withdrawal'])),
            ('history_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('history_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('history_user', self.gf('current_user.models.CurrentUserField')(related_name='_gassupplierorder_history', null=True, to=orm['auth.User'])),
            ('history_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('gas', ['HistoricalGASSupplierOrder'])

        # Adding model 'GASSupplierOrder'
        db.create_table('gas_gassupplierorder', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('gas', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gas.GAS'])),
            ('supplier', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['supplier.Supplier'])),
            ('date_start', self.gf('django.db.models.fields.DateTimeField')()),
            ('date_end', self.gf('django.db.models.fields.DateTimeField')()),
            ('delivery', self.gf('django.db.models.fields.related.ForeignKey')(related_name='supplier_order_set', to=orm['gas.Delivery'])),
            ('order_minimum_amount', self.gf('gasistafelice.base.fields.CurrencyField')(null=True, max_digits=10, decimal_places=4, blank=True)),
            ('withdrawal', self.gf('django.db.models.fields.related.ForeignKey')(related_name='supplier_order_set', to=orm['gas.Withdrawal'])),
        ))
        db.send_create_signal('gas', ['GASSupplierOrder'])

        # Adding model 'HistoricalGASSupplierOrderProduct'
        db.create_table('gas_historicalgassupplierorderproduct', (
            ('id', self.gf('django.db.models.fields.IntegerField')(db_index=True, blank=True)),
            ('order', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gas.GASSupplierOrder'])),
            ('stock', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gas.GASSupplierStock'])),
            ('maximum_amount', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, blank=True)),
            ('ordered_price', self.gf('gasistafelice.base.fields.CurrencyField')(max_digits=10, decimal_places=4, blank=True)),
            ('delivered_price', self.gf('gasistafelice.base.fields.CurrencyField')(max_digits=10, decimal_places=4, blank=True)),
            ('delivered_amount', self.gf('django.db.models.fields.PositiveIntegerField')(blank=True)),
            ('history_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('history_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('history_user', self.gf('current_user.models.CurrentUserField')(related_name='_gassupplierorderproduct_history', null=True, to=orm['auth.User'])),
            ('history_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('gas', ['HistoricalGASSupplierOrderProduct'])

        # Adding model 'GASSupplierOrderProduct'
        db.create_table('gas_gassupplierorderproduct', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('order', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gas.GASSupplierOrder'])),
            ('stock', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gas.GASSupplierStock'])),
            ('maximum_amount', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, blank=True)),
            ('ordered_price', self.gf('gasistafelice.base.fields.CurrencyField')(max_digits=10, decimal_places=4, blank=True)),
            ('delivered_price', self.gf('gasistafelice.base.fields.CurrencyField')(max_digits=10, decimal_places=4, blank=True)),
            ('delivered_amount', self.gf('django.db.models.fields.PositiveIntegerField')(blank=True)),
        ))
        db.send_create_signal('gas', ['GASSupplierOrderProduct'])

        # Adding model 'HistoricalGASMemberOrder'
        db.create_table('gas_historicalgasmemberorder', (
            ('id', self.gf('django.db.models.fields.IntegerField')(db_index=True, blank=True)),
            ('purchaser', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gas.GASMember'])),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gas.GASSupplierOrderProduct'])),
            ('ordered_price', self.gf('gasistafelice.base.fields.CurrencyField')(max_digits=10, decimal_places=4, blank=True)),
            ('ordered_amount', self.gf('django.db.models.fields.PositiveIntegerField')(blank=True)),
            ('withdrawn_amount', self.gf('django.db.models.fields.PositiveIntegerField')(blank=True)),
            ('history_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('history_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('history_user', self.gf('current_user.models.CurrentUserField')(related_name='_gasmemberorder_history', null=True, to=orm['auth.User'])),
            ('history_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('gas', ['HistoricalGASMemberOrder'])

        # Adding model 'GASMemberOrder'
        db.create_table('gas_gasmemberorder', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('purchaser', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gas.GASMember'])),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gas.GASSupplierOrderProduct'])),
            ('ordered_price', self.gf('gasistafelice.base.fields.CurrencyField')(max_digits=10, decimal_places=4, blank=True)),
            ('ordered_amount', self.gf('django.db.models.fields.PositiveIntegerField')(blank=True)),
            ('withdrawn_amount', self.gf('django.db.models.fields.PositiveIntegerField')(blank=True)),
        ))
        db.send_create_signal('gas', ['GASMemberOrder'])

        # Adding model 'HistoricalDelivery'
        db.create_table('gas_historicaldelivery', (
            ('id', self.gf('django.db.models.fields.IntegerField')(db_index=True, blank=True)),
            ('place', self.gf('django.db.models.fields.related.ForeignKey')(related_name='historicaldelivery_set', to=orm['base.Place'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('history_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('history_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('history_user', self.gf('current_user.models.CurrentUserField')(related_name='_delivery_history', null=True, to=orm['auth.User'])),
            ('history_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('gas', ['HistoricalDelivery'])

        # Adding model 'Delivery'
        db.create_table('gas_delivery', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('place', self.gf('django.db.models.fields.related.ForeignKey')(related_name='delivery_set', to=orm['base.Place'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('gas', ['Delivery'])

        # Adding M2M table for field referrers on 'Delivery'
        db.create_table('gas_delivery_referrers', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('delivery', models.ForeignKey(orm['gas.delivery'], null=False)),
            ('gasmember', models.ForeignKey(orm['gas.gasmember'], null=False))
        ))
        db.create_unique('gas_delivery_referrers', ['delivery_id', 'gasmember_id'])

        # Adding model 'HistoricalWithdrawal'
        db.create_table('gas_historicalwithdrawal', (
            ('id', self.gf('django.db.models.fields.IntegerField')(db_index=True, blank=True)),
            ('place', self.gf('django.db.models.fields.related.ForeignKey')(related_name='historicalwithdrawal_set', to=orm['base.Place'])),
            ('start_time', self.gf('django.db.models.fields.TimeField')()),
            ('end_time', self.gf('django.db.models.fields.TimeField')()),
            ('history_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('history_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('history_user', self.gf('current_user.models.CurrentUserField')(related_name='_withdrawal_history', null=True, to=orm['auth.User'])),
            ('history_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('gas', ['HistoricalWithdrawal'])

        # Adding model 'Withdrawal'
        db.create_table('gas_withdrawal', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('place', self.gf('django.db.models.fields.related.ForeignKey')(related_name='withdrawal_set', to=orm['base.Place'])),
            ('start_time', self.gf('django.db.models.fields.TimeField')()),
            ('end_time', self.gf('django.db.models.fields.TimeField')()),
        ))
        db.send_create_signal('gas', ['Withdrawal'])

        # Adding M2M table for field referrers on 'Withdrawal'
        db.create_table('gas_withdrawal_referrers', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('withdrawal', models.ForeignKey(orm['gas.withdrawal'], null=False)),
            ('gasmember', models.ForeignKey(orm['gas.gasmember'], null=False))
        ))
        db.create_unique('gas_withdrawal_referrers', ['withdrawal_id', 'gasmember_id'])


    def backwards(self, orm):
        
        # Deleting model 'HistoricalGAS'
        db.delete_table('gas_historicalgas')

        # Deleting model 'GAS'
        db.delete_table('gas_gas')

        # Deleting model 'HistoricalGASMember'
        db.delete_table('gas_historicalgasmember')

        # Deleting model 'GASMember'
        db.delete_table('gas_gasmember')

        # Removing M2M table for field available_for_roles on 'GASMember'
        db.delete_table('gas_gasmember_available_for_roles')

        # Removing M2M table for field roles on 'GASMember'
        db.delete_table('gas_gasmember_roles')

        # Deleting model 'HistoricalGASSupplierSolidalPact'
        db.delete_table('gas_historicalgassuppliersolidalpact')

        # Deleting model 'GASSupplierSolidalPact'
        db.delete_table('gas_gassuppliersolidalpact')

        # Removing M2M table for field supplier_gas_catalog on 'GASSupplierSolidalPact'
        db.delete_table('gas_gassuppliersolidalpact_supplier_gas_catalog')

        # Deleting model 'HistoricalGASSupplierStock'
        db.delete_table('gas_historicalgassupplierstock')

        # Deleting model 'GASSupplierStock'
        db.delete_table('gas_gassupplierstock')

        # Deleting model 'HistoricalGASSupplierOrder'
        db.delete_table('gas_historicalgassupplierorder')

        # Deleting model 'GASSupplierOrder'
        db.delete_table('gas_gassupplierorder')

        # Deleting model 'HistoricalGASSupplierOrderProduct'
        db.delete_table('gas_historicalgassupplierorderproduct')

        # Deleting model 'GASSupplierOrderProduct'
        db.delete_table('gas_gassupplierorderproduct')

        # Deleting model 'HistoricalGASMemberOrder'
        db.delete_table('gas_historicalgasmemberorder')

        # Deleting model 'GASMemberOrder'
        db.delete_table('gas_gasmemberorder')

        # Deleting model 'HistoricalDelivery'
        db.delete_table('gas_historicaldelivery')

        # Deleting model 'Delivery'
        db.delete_table('gas_delivery')

        # Removing M2M table for field referrers on 'Delivery'
        db.delete_table('gas_delivery_referrers')

        # Deleting model 'HistoricalWithdrawal'
        db.delete_table('gas_historicalwithdrawal')

        # Deleting model 'Withdrawal'
        db.delete_table('gas_withdrawal')

        # Removing M2M table for field referrers on 'Withdrawal'
        db.delete_table('gas_withdrawal_referrers')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'bank.account': {
            'Meta': {'object_name': 'Account'},
            'balance': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '4'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'base.contact': {
            'Meta': {'object_name': 'Contact'},
            'contact_type': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'contact_value': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'base.person': {
            'Meta': {'object_name': 'Person'},
            'contacts': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['base.Contact']", 'null': 'True', 'blank': 'True'}),
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        'base.place': {
            'Meta': {'object_name': 'Place'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'lon': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'province': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'gas.delivery': {
            'Meta': {'object_name': 'Delivery'},
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'delivery_set'", 'to': "orm['base.Place']"}),
            'referrers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['gas.GASMember']", 'null': 'True', 'blank': 'True'})
        },
        'gas.gas': {
            'Meta': {'object_name': 'GAS'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'gas_set'", 'null': 'True', 'to': "orm['bank.Account']"}),
            'association_act': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'birthday': ('django.db.models.fields.DateField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'email_gas': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'email_referrer': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_in_des': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'intent_act': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'liquidity': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'gas_set2'", 'null': 'True', 'to': "orm['bank.Account']"}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'ssn': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True'}),
            'suppliers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['supplier.Supplier']", 'null': 'True', 'through': "orm['gas.GASSupplierSolidalPact']", 'blank': 'True'}),
            'vat': ('django.db.models.fields.CharField', [], {'max_length': '11', 'null': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'gas.gasmember': {
            'Meta': {'object_name': 'GASMember'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bank.Account']"}),
            'available_for_roles': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'gas_member_available_set'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['permissions.Role']"}),
            'gas': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gas.GAS']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_in_gas': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['base.Person']"}),
            'roles': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'gas_member_set'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['permissions.Role']"})
        },
        'gas.gasmemberorder': {
            'Meta': {'object_name': 'GASMemberOrder'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ordered_amount': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True'}),
            'ordered_price': ('gasistafelice.base.fields.CurrencyField', [], {'max_digits': '10', 'decimal_places': '4', 'blank': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gas.GASSupplierOrderProduct']"}),
            'purchaser': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gas.GASMember']"}),
            'withdrawn_amount': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True'})
        },
        'gas.gassupplierorder': {
            'Meta': {'object_name': 'GASSupplierOrder'},
            'date_end': ('django.db.models.fields.DateTimeField', [], {}),
            'date_start': ('django.db.models.fields.DateTimeField', [], {}),
            'delivery': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'supplier_order_set'", 'to': "orm['gas.Delivery']"}),
            'gas': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gas.GAS']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order_minimum_amount': ('gasistafelice.base.fields.CurrencyField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '4', 'blank': 'True'}),
            'products': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['gas.GASSupplierStock']", 'symmetrical': 'False', 'through': "orm['gas.GASSupplierOrderProduct']", 'blank': 'True'}),
            'supplier': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['supplier.Supplier']"}),
            'withdrawal': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'supplier_order_set'", 'to': "orm['gas.Withdrawal']"})
        },
        'gas.gassupplierorderproduct': {
            'Meta': {'object_name': 'GASSupplierOrderProduct'},
            'delivered_amount': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True'}),
            'delivered_price': ('gasistafelice.base.fields.CurrencyField', [], {'max_digits': '10', 'decimal_places': '4', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'maximum_amount': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'blank': 'True'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gas.GASSupplierOrder']"}),
            'ordered_price': ('gasistafelice.base.fields.CurrencyField', [], {'max_digits': '10', 'decimal_places': '4', 'blank': 'True'}),
            'stock': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gas.GASSupplierStock']"})
        },
        'gas.gassuppliersolidalpact': {
            'Meta': {'object_name': 'GASSupplierSolidalPact'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bank.Account']"}),
            'date_signed': ('django.db.models.fields.DateField', [], {}),
            'default_withdrawal_day': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True'}),
            'default_withdrawal_place': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'default_for_solidal_pact_set'", 'to': "orm['base.Place']"}),
            'default_withdrawal_time': ('django.db.models.fields.TimeField', [], {'null': 'True'}),
            'gas': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gas.GAS']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order_deliver_interval': ('django.db.models.fields.TimeField', [], {}),
            'order_delivery_cost': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'order_minimum_amount': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'order_price_percent_update': ('django.db.models.fields.FloatField', [], {}),
            'supplier': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['supplier.Supplier']"}),
            'supplier_gas_catalog': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['supplier.Product']", 'null': 'True', 'blank': 'True'})
        },
        'gas.gassupplierstock': {
            'Meta': {'object_name': 'GASSupplierStock'},
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'gas': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gas.GAS']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order_minimum_amount': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'order_step': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'supplier_stock': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['supplier.SupplierStock']"})
        },
        'gas.historicaldelivery': {
            'Meta': {'ordering': "('-history_date',)", 'object_name': 'HistoricalDelivery'},
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'history_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'history_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'history_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'history_user': ('current_user.models.CurrentUserField', [], {'related_name': "'_delivery_history'", 'null': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'blank': 'True'}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'historicaldelivery_set'", 'to': "orm['base.Place']"})
        },
        'gas.historicalgas': {
            'Meta': {'ordering': "('-history_date',)", 'object_name': 'HistoricalGAS'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'historicalgas_set'", 'null': 'True', 'to': "orm['bank.Account']"}),
            'association_act': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'birthday': ('django.db.models.fields.DateField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'email_gas': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'email_referrer': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'history_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'history_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'history_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'history_user': ('current_user.models.CurrentUserField', [], {'related_name': "'_gas_history'", 'null': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'blank': 'True'}),
            'id_in_des': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'intent_act': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'liquidity': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'historicalgas_set2'", 'null': 'True', 'to': "orm['bank.Account']"}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'ssn': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True'}),
            'vat': ('django.db.models.fields.CharField', [], {'max_length': '11', 'null': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'gas.historicalgasmember': {
            'Meta': {'ordering': "('-history_date',)", 'object_name': 'HistoricalGASMember'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bank.Account']"}),
            'gas': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gas.GAS']"}),
            'history_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'history_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'history_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'history_user': ('current_user.models.CurrentUserField', [], {'related_name': "'_gasmember_history'", 'null': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'blank': 'True'}),
            'id_in_gas': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['base.Person']"})
        },
        'gas.historicalgasmemberorder': {
            'Meta': {'ordering': "('-history_date',)", 'object_name': 'HistoricalGASMemberOrder'},
            'history_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'history_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'history_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'history_user': ('current_user.models.CurrentUserField', [], {'related_name': "'_gasmemberorder_history'", 'null': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'blank': 'True'}),
            'ordered_amount': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True'}),
            'ordered_price': ('gasistafelice.base.fields.CurrencyField', [], {'max_digits': '10', 'decimal_places': '4', 'blank': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gas.GASSupplierOrderProduct']"}),
            'purchaser': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gas.GASMember']"}),
            'withdrawn_amount': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True'})
        },
        'gas.historicalgassupplierorder': {
            'Meta': {'ordering': "('-history_date',)", 'object_name': 'HistoricalGASSupplierOrder'},
            'date_end': ('django.db.models.fields.DateTimeField', [], {}),
            'date_start': ('django.db.models.fields.DateTimeField', [], {}),
            'delivery': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'historicalsupplier_order_set'", 'to': "orm['gas.Delivery']"}),
            'gas': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gas.GAS']"}),
            'history_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'history_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'history_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'history_user': ('current_user.models.CurrentUserField', [], {'related_name': "'_gassupplierorder_history'", 'null': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'blank': 'True'}),
            'order_minimum_amount': ('gasistafelice.base.fields.CurrencyField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '4', 'blank': 'True'}),
            'supplier': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['supplier.Supplier']"}),
            'withdrawal': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'historicalsupplier_order_set'", 'to': "orm['gas.Withdrawal']"})
        },
        'gas.historicalgassupplierorderproduct': {
            'Meta': {'ordering': "('-history_date',)", 'object_name': 'HistoricalGASSupplierOrderProduct'},
            'delivered_amount': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True'}),
            'delivered_price': ('gasistafelice.base.fields.CurrencyField', [], {'max_digits': '10', 'decimal_places': '4', 'blank': 'True'}),
            'history_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'history_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'history_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'history_user': ('current_user.models.CurrentUserField', [], {'related_name': "'_gassupplierorderproduct_history'", 'null': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'blank': 'True'}),
            'maximum_amount': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'blank': 'True'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gas.GASSupplierOrder']"}),
            'ordered_price': ('gasistafelice.base.fields.CurrencyField', [], {'max_digits': '10', 'decimal_places': '4', 'blank': 'True'}),
            'stock': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gas.GASSupplierStock']"})
        },
        'gas.historicalgassuppliersolidalpact': {
            'Meta': {'ordering': "('-history_date',)", 'object_name': 'HistoricalGASSupplierSolidalPact'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bank.Account']"}),
            'date_signed': ('django.db.models.fields.DateField', [], {}),
            'default_withdrawal_day': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True'}),
            'default_withdrawal_place': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'historicaldefault_for_solidal_pact_set'", 'to': "orm['base.Place']"}),
            'default_withdrawal_time': ('django.db.models.fields.TimeField', [], {'null': 'True'}),
            'gas': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gas.GAS']"}),
            'history_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'history_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'history_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'history_user': ('current_user.models.CurrentUserField', [], {'related_name': "'_gassuppliersolidalpact_history'", 'null': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'blank': 'True'}),
            'order_deliver_interval': ('django.db.models.fields.TimeField', [], {}),
            'order_delivery_cost': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'order_minimum_amount': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'order_price_percent_update': ('django.db.models.fields.FloatField', [], {}),
            'supplier': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['supplier.Supplier']"})
        },
        'gas.historicalgassupplierstock': {
            'Meta': {'ordering': "('-history_date',)", 'object_name': 'HistoricalGASSupplierStock'},
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'gas': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gas.GAS']"}),
            'history_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'history_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'history_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'history_user': ('current_user.models.CurrentUserField', [], {'related_name': "'_gassupplierstock_history'", 'null': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'blank': 'True'}),
            'order_minimum_amount': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'order_step': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'supplier_stock': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['supplier.SupplierStock']"})
        },
        'gas.historicalwithdrawal': {
            'Meta': {'ordering': "('-history_date',)", 'object_name': 'HistoricalWithdrawal'},
            'end_time': ('django.db.models.fields.TimeField', [], {}),
            'history_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'history_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'history_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'history_user': ('current_user.models.CurrentUserField', [], {'related_name': "'_withdrawal_history'", 'null': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'blank': 'True'}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'historicalwithdrawal_set'", 'to': "orm['base.Place']"}),
            'start_time': ('django.db.models.fields.TimeField', [], {})
        },
        'gas.withdrawal': {
            'Meta': {'object_name': 'Withdrawal'},
            'end_time': ('django.db.models.fields.TimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'withdrawal_set'", 'to': "orm['base.Place']"}),
            'referrers': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['gas.GASMember']", 'symmetrical': 'False'}),
            'start_time': ('django.db.models.fields.TimeField', [], {})
        },
        'permissions.role': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Role'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'supplier.certification': {
            'Meta': {'object_name': 'Certification'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        },
        'supplier.product': {
            'Meta': {'object_name': 'Product'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['supplier.ProductCategory']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mu': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['supplier.ProductMU']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'producer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['supplier.Supplier']"}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        'supplier.productcategory': {
            'Meta': {'object_name': 'ProductCategory'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        },
        'supplier.productmu': {
            'Meta': {'object_name': 'ProductMU'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'})
        },
        'supplier.supplier': {
            'Meta': {'object_name': 'Supplier'},
            'certifications': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['supplier.Certification']", 'symmetrical': 'False'}),
            'flavour': ('django.db.models.fields.CharField', [], {'default': "'COMPANY'", 'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'referrers': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['base.Person']", 'through': "orm['supplier.SupplierAgent']", 'symmetrical': 'False'}),
            'seat': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['base.Place']"}),
            'vat_number': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'supplier.supplieragent': {
            'Meta': {'object_name': 'SupplierAgent'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'job_title': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['base.Person']"}),
            'supplier': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['supplier.Supplier']"})
        },
        'supplier.supplierstock': {
            'Meta': {'object_name': 'SupplierStock'},
            'amount_available': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1000000000'}),
            'delivery_terms': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order_minimum_amount': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'order_step': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['supplier.Product']"}),
            'supplier': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['supplier.Supplier']"})
        }
    }

    complete_apps = ['gas']
