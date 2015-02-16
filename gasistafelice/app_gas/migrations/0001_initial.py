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
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128, db_index=True)),
            ('id_in_des', self.gf('django.db.models.fields.CharField')(max_length=8, db_index=True)),
            ('logo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('headquarter_id', self.gf('django.db.models.fields.IntegerField')(db_index=True, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('membership_fee', self.gf('gasistafelice.lib.fields.models.CurrencyField')(default='0', max_digits=10, decimal_places=4, blank=True)),
            ('birthday', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('vat', self.gf('django.db.models.fields.CharField')(max_length=11, blank=True)),
            ('fcc', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
            ('orders_email_contact_id', self.gf('django.db.models.fields.IntegerField')(db_index=True, null=True, blank=True)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('association_act', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('intent_act', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('note', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('des_id', self.gf('django.db.models.fields.IntegerField')(db_index=True, null=True, blank=True)),
            ('history_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('history_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('history_user', self.gf('current_user.models.CurrentUserField')(related_name='_gas_history', null=True, to=orm['auth.User'])),
            ('history_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('gas', ['HistoricalGAS'])

        # Adding model 'GAS'
        db.create_table('gas_gas', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
            ('id_in_des', self.gf('django.db.models.fields.CharField')(unique=True, max_length=8)),
            ('logo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('headquarter', self.gf('django.db.models.fields.related.ForeignKey')(related_name='gas_headquarter_set', to=orm['base.Place'])),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('membership_fee', self.gf('gasistafelice.lib.fields.models.CurrencyField')(default='0', max_digits=10, decimal_places=4, blank=True)),
            ('birthday', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('vat', self.gf('django.db.models.fields.CharField')(max_length=11, blank=True)),
            ('fcc', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
            ('orders_email_contact', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='gas_use_for_orders_set', null=True, to=orm['base.Contact'])),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('association_act', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('intent_act', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('note', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('des', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['des.DES'])),
        ))
        db.send_create_signal('gas', ['GAS'])

        # Adding M2M table for field contact_set on 'GAS'
        db.create_table('gas_gas_contact_set', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('gas', models.ForeignKey(orm['gas.gas'], null=False)),
            ('contact', models.ForeignKey(orm['base.contact'], null=False))
        ))
        db.create_unique('gas_gas_contact_set', ['gas_id', 'contact_id'])

        # Adding model 'HistoricalGASConfig'
        db.create_table('gas_historicalgasconfig', (
            ('id', self.gf('django.db.models.fields.IntegerField')(db_index=True, blank=True)),
            ('gas_id', self.gf('django.db.models.fields.IntegerField')(db_index=True, null=True, blank=True)),
            ('default_workflow_gasmember_order_id', self.gf('django.db.models.fields.IntegerField')(db_index=True, null=True, blank=True)),
            ('default_workflow_gassupplier_order_id', self.gf('django.db.models.fields.IntegerField')(db_index=True, null=True, blank=True)),
            ('can_change_price', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('order_show_only_next_delivery', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('order_show_only_one_at_a_time', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('default_close_day', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
            ('default_delivery_day', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
            ('default_close_time', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
            ('default_delivery_time', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
            ('use_withdrawal_place', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('can_change_withdrawal_place_on_each_order', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('can_change_delivery_place_on_each_order', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('default_withdrawal_place_id', self.gf('django.db.models.fields.IntegerField')(db_index=True, null=True, blank=True)),
            ('default_delivery_place_id', self.gf('django.db.models.fields.IntegerField')(db_index=True, null=True, blank=True)),
            ('auto_populate_products', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('use_scheduler', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('gasmember_auto_confirm_order', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_suspended', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('suspend_datetime', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True, blank=True)),
            ('suspend_reason', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('suspend_auto_resume', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True, db_index=True, blank=True)),
            ('notice_days_before_order_close', self.gf('django.db.models.fields.PositiveIntegerField')(default=1, null=True)),
            ('history_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('history_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('history_user', self.gf('current_user.models.CurrentUserField')(related_name='_gasconfig_history', null=True, to=orm['auth.User'])),
            ('history_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('gas', ['HistoricalGASConfig'])

        # Adding model 'GASConfig'
        db.create_table('gas_gasconfig', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('gas', self.gf('django.db.models.fields.related.OneToOneField')(related_name='config', unique=True, to=orm['gas.GAS'])),
            ('default_workflow_gasmember_order', self.gf('django.db.models.fields.related.ForeignKey')(related_name='gmow_gasconfig_set', blank=True, to=orm['workflows.Workflow'])),
            ('default_workflow_gassupplier_order', self.gf('django.db.models.fields.related.ForeignKey')(related_name='gsopw_gasconfig_set', blank=True, to=orm['workflows.Workflow'])),
            ('can_change_price', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('order_show_only_next_delivery', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('order_show_only_one_at_a_time', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('default_close_day', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
            ('default_delivery_day', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
            ('default_close_time', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
            ('default_delivery_time', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
            ('use_withdrawal_place', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('can_change_withdrawal_place_on_each_order', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('can_change_delivery_place_on_each_order', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('default_withdrawal_place', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='gas_default_withdrawal_set', null=True, to=orm['base.Place'])),
            ('default_delivery_place', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='gas_default_delivery_set', null=True, to=orm['base.Place'])),
            ('auto_populate_products', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('use_scheduler', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('gasmember_auto_confirm_order', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_suspended', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('suspend_datetime', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True, blank=True)),
            ('suspend_reason', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('suspend_auto_resume', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True, db_index=True, blank=True)),
            ('notice_days_before_order_close', self.gf('django.db.models.fields.PositiveIntegerField')(default=1, null=True)),
        ))
        db.send_create_signal('gas', ['GASConfig'])

        # Adding model 'HistoricalGASActivist'
        db.create_table('gas_historicalgasactivist', (
            ('id', self.gf('django.db.models.fields.IntegerField')(db_index=True, blank=True)),
            ('gas_id', self.gf('django.db.models.fields.IntegerField')(db_index=True, null=True, blank=True)),
            ('person_id', self.gf('django.db.models.fields.IntegerField')(db_index=True, null=True, blank=True)),
            ('info_title', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('info_description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('history_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('history_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('history_user', self.gf('current_user.models.CurrentUserField')(related_name='_gasactivist_history', null=True, to=orm['auth.User'])),
            ('history_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('gas', ['HistoricalGASActivist'])

        # Adding model 'GASActivist'
        db.create_table('gas_gasactivist', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('gas', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gas.GAS'])),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.Person'])),
            ('info_title', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('info_description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('gas', ['GASActivist'])

        # Adding model 'HistoricalGASMember'
        db.create_table('gas_historicalgasmember', (
            ('id', self.gf('django.db.models.fields.IntegerField')(db_index=True, blank=True)),
            ('person_id', self.gf('django.db.models.fields.IntegerField')(db_index=True, null=True, blank=True)),
            ('gas_id', self.gf('django.db.models.fields.IntegerField')(db_index=True, null=True, blank=True)),
            ('id_in_gas', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('membership_fee_payed', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('user_planned_list', self.gf('django.db.models.fields.BooleanField')(default=False)),
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
            ('id_in_gas', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('membership_fee_payed', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('user_planned_list', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('gas', ['GASMember'])

        # Adding unique constraint on 'GASMember', fields ['gas', 'id_in_gas']
        db.create_unique('gas_gasmember', ['gas_id', 'id_in_gas'])

        # Adding unique constraint on 'GASMember', fields ['person', 'gas']
        db.create_unique('gas_gasmember', ['person_id', 'gas_id'])

        # Adding M2M table for field available_for_roles on 'GASMember'
        db.create_table('gas_gasmember_available_for_roles', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('gasmember', models.ForeignKey(orm['gas.gasmember'], null=False)),
            ('role', models.ForeignKey(orm['permissions.role'], null=False))
        ))
        db.create_unique('gas_gasmember_available_for_roles', ['gasmember_id', 'role_id'])

        # Adding model 'HistoricalGASSupplierStock'
        db.create_table('gas_historicalgassupplierstock', (
            ('id', self.gf('django.db.models.fields.IntegerField')(db_index=True, blank=True)),
            ('pact_id', self.gf('django.db.models.fields.IntegerField')(db_index=True, null=True, blank=True)),
            ('stock_id', self.gf('django.db.models.fields.IntegerField')(db_index=True, null=True, blank=True)),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('minimum_amount', self.gf('gasistafelice.lib.fields.models.PrettyDecimalField')(default=1, max_digits=5, decimal_places=2)),
            ('step', self.gf('gasistafelice.lib.fields.models.PrettyDecimalField')(default=1, max_digits=5, decimal_places=2)),
            ('history_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('history_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('history_user', self.gf('current_user.models.CurrentUserField')(related_name='_gassupplierstock_history', null=True, to=orm['auth.User'])),
            ('history_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('gas', ['HistoricalGASSupplierStock'])

        # Adding model 'GASSupplierStock'
        db.create_table('gas_gassupplierstock', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pact', self.gf('django.db.models.fields.related.ForeignKey')(related_name='gasstock_set', to=orm['gas.GASSupplierSolidalPact'])),
            ('stock', self.gf('django.db.models.fields.related.ForeignKey')(related_name='gasstock_set', to=orm['supplier.SupplierStock'])),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('minimum_amount', self.gf('gasistafelice.lib.fields.models.PrettyDecimalField')(default=1, max_digits=5, decimal_places=2)),
            ('step', self.gf('gasistafelice.lib.fields.models.PrettyDecimalField')(default=1, max_digits=5, decimal_places=2)),
        ))
        db.send_create_signal('gas', ['GASSupplierStock'])

        # Adding model 'HistoricalGASSupplierSolidalPact'
        db.create_table('gas_historicalgassuppliersolidalpact', (
            ('id', self.gf('django.db.models.fields.IntegerField')(db_index=True, blank=True)),
            ('gas_id', self.gf('django.db.models.fields.IntegerField')(db_index=True, null=True, blank=True)),
            ('supplier_id', self.gf('django.db.models.fields.IntegerField')(db_index=True, null=True, blank=True)),
            ('date_signed', self.gf('django.db.models.fields.DateField')(default=None, null=True, blank=True)),
            ('order_minimum_amount', self.gf('gasistafelice.lib.fields.models.CurrencyField')(null=True, max_digits=10, decimal_places=4, blank=True)),
            ('order_delivery_cost', self.gf('gasistafelice.lib.fields.models.CurrencyField')(null=True, max_digits=10, decimal_places=4, blank=True)),
            ('order_deliver_interval', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
            ('order_price_percent_update', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=3, decimal_places=2, blank=True)),
            ('default_delivery_day', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
            ('default_delivery_time', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
            ('default_delivery_place_id', self.gf('django.db.models.fields.IntegerField')(db_index=True, null=True, blank=True)),
            ('auto_populate_products', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('orders_can_be_grouped', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('document', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('is_suspended', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('suspend_datetime', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True, blank=True)),
            ('suspend_reason', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('suspend_auto_resume', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True, db_index=True, blank=True)),
            ('history_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('history_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('history_user', self.gf('current_user.models.CurrentUserField')(related_name='_gassuppliersolidalpact_history', null=True, to=orm['auth.User'])),
            ('history_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('gas', ['HistoricalGASSupplierSolidalPact'])

        # Adding model 'GASSupplierSolidalPact'
        db.create_table('gas_gassuppliersolidalpact', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('gas', self.gf('django.db.models.fields.related.ForeignKey')(related_name='pact_set', to=orm['gas.GAS'])),
            ('supplier', self.gf('django.db.models.fields.related.ForeignKey')(related_name='pact_set', to=orm['supplier.Supplier'])),
            ('date_signed', self.gf('django.db.models.fields.DateField')(default=None, null=True, blank=True)),
            ('order_minimum_amount', self.gf('gasistafelice.lib.fields.models.CurrencyField')(null=True, max_digits=10, decimal_places=4, blank=True)),
            ('order_delivery_cost', self.gf('gasistafelice.lib.fields.models.CurrencyField')(null=True, max_digits=10, decimal_places=4, blank=True)),
            ('order_deliver_interval', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
            ('order_price_percent_update', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=3, decimal_places=2, blank=True)),
            ('default_delivery_day', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
            ('default_delivery_time', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
            ('default_delivery_place', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='pact_default_delivery_place_set', null=True, to=orm['base.Place'])),
            ('auto_populate_products', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('orders_can_be_grouped', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('document', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('is_suspended', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('suspend_datetime', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True, blank=True)),
            ('suspend_reason', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('suspend_auto_resume', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True, db_index=True, blank=True)),
        ))
        db.send_create_signal('gas', ['GASSupplierSolidalPact'])

        # Adding unique constraint on 'GASSupplierSolidalPact', fields ['gas', 'supplier']
        db.create_unique('gas_gassuppliersolidalpact', ['gas_id', 'supplier_id'])

        # Adding model 'HistoricalGASSupplierOrder'
        db.create_table('gas_historicalgassupplierorder', (
            ('id', self.gf('django.db.models.fields.IntegerField')(db_index=True, blank=True)),
            ('pact_id', self.gf('django.db.models.fields.IntegerField')(db_index=True, null=True, blank=True)),
            ('datetime_start', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('datetime_end', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('order_minimum_amount', self.gf('gasistafelice.lib.fields.models.CurrencyField')(null=True, max_digits=10, decimal_places=4, blank=True)),
            ('delivery_id', self.gf('django.db.models.fields.IntegerField')(db_index=True, null=True, blank=True)),
            ('withdrawal_id', self.gf('django.db.models.fields.IntegerField')(db_index=True, null=True, blank=True)),
            ('delivery_cost', self.gf('gasistafelice.lib.fields.models.CurrencyField')(null=True, max_digits=10, decimal_places=4, blank=True)),
            ('referrer_person_id', self.gf('django.db.models.fields.IntegerField')(db_index=True, null=True, blank=True)),
            ('delivery_referrer_person_id', self.gf('django.db.models.fields.IntegerField')(db_index=True, null=True, blank=True)),
            ('withdrawal_referrer_person_id', self.gf('django.db.models.fields.IntegerField')(db_index=True, null=True, blank=True)),
            ('group_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('invoice_amount', self.gf('gasistafelice.lib.fields.models.CurrencyField')(null=True, max_digits=10, decimal_places=4, blank=True)),
            ('invoice_note', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('root_plan_id', self.gf('django.db.models.fields.IntegerField')(default=None, null=True, db_index=True, blank=True)),
            ('history_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('history_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('history_user', self.gf('current_user.models.CurrentUserField')(related_name='_gassupplierorder_history', null=True, to=orm['auth.User'])),
            ('history_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('gas', ['HistoricalGASSupplierOrder'])

        # Adding model 'GASSupplierOrder'
        db.create_table('gas_gassupplierorder', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pact', self.gf('django.db.models.fields.related.ForeignKey')(related_name='order_set', to=orm['gas.GASSupplierSolidalPact'])),
            ('datetime_start', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('datetime_end', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('order_minimum_amount', self.gf('gasistafelice.lib.fields.models.CurrencyField')(null=True, max_digits=10, decimal_places=4, blank=True)),
            ('delivery', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='order_set', null=True, to=orm['gas.Delivery'])),
            ('withdrawal', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='order_set', null=True, to=orm['gas.Withdrawal'])),
            ('delivery_cost', self.gf('gasistafelice.lib.fields.models.CurrencyField')(null=True, max_digits=10, decimal_places=4, blank=True)),
            ('referrer_person', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='order_set', null=True, to=orm['base.Person'])),
            ('delivery_referrer_person', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='delivery_for_order_set', null=True, to=orm['base.Person'])),
            ('withdrawal_referrer_person', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='withdrawal_for_order_set', null=True, to=orm['base.Person'])),
            ('group_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('invoice_amount', self.gf('gasistafelice.lib.fields.models.CurrencyField')(null=True, max_digits=10, decimal_places=4, blank=True)),
            ('invoice_note', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('root_plan', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['gas.GASSupplierOrder'], null=True, blank=True)),
        ))
        db.send_create_signal('gas', ['GASSupplierOrder'])

        # Adding model 'HistoricalGASSupplierOrderProduct'
        db.create_table('gas_historicalgassupplierorderproduct', (
            ('id', self.gf('django.db.models.fields.IntegerField')(db_index=True, blank=True)),
            ('order_id', self.gf('django.db.models.fields.IntegerField')(db_index=True, null=True, blank=True)),
            ('gasstock_id', self.gf('django.db.models.fields.IntegerField')(db_index=True, null=True, blank=True)),
            ('maximum_amount', self.gf('gasistafelice.lib.fields.models.PrettyDecimalField')(null=True, max_digits=8, decimal_places=2, blank=True)),
            ('initial_price', self.gf('gasistafelice.lib.fields.models.CurrencyField')(max_digits=10, decimal_places=4)),
            ('order_price', self.gf('gasistafelice.lib.fields.models.CurrencyField')(max_digits=10, decimal_places=4)),
            ('delivered_price', self.gf('gasistafelice.lib.fields.models.CurrencyField')(null=True, max_digits=10, decimal_places=4, blank=True)),
            ('delivered_amount', self.gf('gasistafelice.lib.fields.models.PrettyDecimalField')(null=True, max_digits=8, decimal_places=2, blank=True)),
            ('history_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('history_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('history_user', self.gf('current_user.models.CurrentUserField')(related_name='_gassupplierorderproduct_history', null=True, to=orm['auth.User'])),
            ('history_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('gas', ['HistoricalGASSupplierOrderProduct'])

        # Adding model 'GASSupplierOrderProduct'
        db.create_table('gas_gassupplierorderproduct', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('order', self.gf('django.db.models.fields.related.ForeignKey')(related_name='orderable_product_set', to=orm['gas.GASSupplierOrder'])),
            ('gasstock', self.gf('django.db.models.fields.related.ForeignKey')(related_name='orderable_product_set', to=orm['gas.GASSupplierStock'])),
            ('maximum_amount', self.gf('gasistafelice.lib.fields.models.PrettyDecimalField')(null=True, max_digits=8, decimal_places=2, blank=True)),
            ('initial_price', self.gf('gasistafelice.lib.fields.models.CurrencyField')(max_digits=10, decimal_places=4)),
            ('order_price', self.gf('gasistafelice.lib.fields.models.CurrencyField')(max_digits=10, decimal_places=4)),
            ('delivered_price', self.gf('gasistafelice.lib.fields.models.CurrencyField')(null=True, max_digits=10, decimal_places=4, blank=True)),
            ('delivered_amount', self.gf('gasistafelice.lib.fields.models.PrettyDecimalField')(null=True, max_digits=8, decimal_places=2, blank=True)),
        ))
        db.send_create_signal('gas', ['GASSupplierOrderProduct'])

        # Adding model 'HistoricalGASMemberOrder'
        db.create_table('gas_historicalgasmemberorder', (
            ('id', self.gf('django.db.models.fields.IntegerField')(db_index=True, blank=True)),
            ('purchaser_id', self.gf('django.db.models.fields.IntegerField')(db_index=True, null=True, blank=True)),
            ('ordered_product_id', self.gf('django.db.models.fields.IntegerField')(db_index=True, null=True, blank=True)),
            ('ordered_price', self.gf('gasistafelice.lib.fields.models.CurrencyField')(max_digits=10, decimal_places=4)),
            ('ordered_amount', self.gf('gasistafelice.lib.fields.models.PrettyDecimalField')(max_digits=6, decimal_places=2)),
            ('withdrawn_amount', self.gf('gasistafelice.lib.fields.models.PrettyDecimalField')(null=True, max_digits=6, decimal_places=2, blank=True)),
            ('is_confirmed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('note', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('history_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('history_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('history_user', self.gf('current_user.models.CurrentUserField')(related_name='_gasmemberorder_history', null=True, to=orm['auth.User'])),
            ('history_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('gas', ['HistoricalGASMemberOrder'])

        # Adding model 'GASMemberOrder'
        db.create_table('gas_gasmemberorder', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('purchaser', self.gf('django.db.models.fields.related.ForeignKey')(related_name='gasmember_order_set', to=orm['gas.GASMember'])),
            ('ordered_product', self.gf('django.db.models.fields.related.ForeignKey')(related_name='gasmember_order_set', to=orm['gas.GASSupplierOrderProduct'])),
            ('ordered_price', self.gf('gasistafelice.lib.fields.models.CurrencyField')(max_digits=10, decimal_places=4)),
            ('ordered_amount', self.gf('gasistafelice.lib.fields.models.PrettyDecimalField')(max_digits=6, decimal_places=2)),
            ('withdrawn_amount', self.gf('gasistafelice.lib.fields.models.PrettyDecimalField')(null=True, max_digits=6, decimal_places=2, blank=True)),
            ('is_confirmed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('note', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
        ))
        db.send_create_signal('gas', ['GASMemberOrder'])

        # Adding unique constraint on 'GASMemberOrder', fields ['ordered_product', 'purchaser']
        db.create_unique('gas_gasmemberorder', ['ordered_product_id', 'purchaser_id'])

        # Adding model 'HistoricalDelivery'
        db.create_table('gas_historicaldelivery', (
            ('id', self.gf('django.db.models.fields.IntegerField')(db_index=True, blank=True)),
            ('place_id', self.gf('django.db.models.fields.IntegerField')(db_index=True, null=True, blank=True)),
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

        # Adding model 'HistoricalWithdrawal'
        db.create_table('gas_historicalwithdrawal', (
            ('id', self.gf('django.db.models.fields.IntegerField')(db_index=True, blank=True)),
            ('place_id', self.gf('django.db.models.fields.IntegerField')(db_index=True, null=True, blank=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('start_time', self.gf('django.db.models.fields.TimeField')(default='18:00')),
            ('end_time', self.gf('django.db.models.fields.TimeField')(default='22:00')),
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
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('start_time', self.gf('django.db.models.fields.TimeField')(default='18:00')),
            ('end_time', self.gf('django.db.models.fields.TimeField')(default='22:00')),
        ))
        db.send_create_signal('gas', ['Withdrawal'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'GASMemberOrder', fields ['ordered_product', 'purchaser']
        db.delete_unique('gas_gasmemberorder', ['ordered_product_id', 'purchaser_id'])

        # Removing unique constraint on 'GASSupplierSolidalPact', fields ['gas', 'supplier']
        db.delete_unique('gas_gassuppliersolidalpact', ['gas_id', 'supplier_id'])

        # Removing unique constraint on 'GASMember', fields ['person', 'gas']
        db.delete_unique('gas_gasmember', ['person_id', 'gas_id'])

        # Removing unique constraint on 'GASMember', fields ['gas', 'id_in_gas']
        db.delete_unique('gas_gasmember', ['gas_id', 'id_in_gas'])

        # Deleting model 'HistoricalGAS'
        db.delete_table('gas_historicalgas')

        # Deleting model 'GAS'
        db.delete_table('gas_gas')

        # Removing M2M table for field contact_set on 'GAS'
        db.delete_table('gas_gas_contact_set')

        # Deleting model 'HistoricalGASConfig'
        db.delete_table('gas_historicalgasconfig')

        # Deleting model 'GASConfig'
        db.delete_table('gas_gasconfig')

        # Deleting model 'HistoricalGASActivist'
        db.delete_table('gas_historicalgasactivist')

        # Deleting model 'GASActivist'
        db.delete_table('gas_gasactivist')

        # Deleting model 'HistoricalGASMember'
        db.delete_table('gas_historicalgasmember')

        # Deleting model 'GASMember'
        db.delete_table('gas_gasmember')

        # Removing M2M table for field available_for_roles on 'GASMember'
        db.delete_table('gas_gasmember_available_for_roles')

        # Deleting model 'HistoricalGASSupplierStock'
        db.delete_table('gas_historicalgassupplierstock')

        # Deleting model 'GASSupplierStock'
        db.delete_table('gas_gassupplierstock')

        # Deleting model 'HistoricalGASSupplierSolidalPact'
        db.delete_table('gas_historicalgassuppliersolidalpact')

        # Deleting model 'GASSupplierSolidalPact'
        db.delete_table('gas_gassuppliersolidalpact')

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

        # Deleting model 'HistoricalWithdrawal'
        db.delete_table('gas_historicalwithdrawal')

        # Deleting model 'Withdrawal'
        db.delete_table('gas_withdrawal')


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
        'base.contact': {
            'Meta': {'object_name': 'Contact'},
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128', 'blank': 'True'}),
            'flavour': ('django.db.models.fields.CharField', [], {'default': "'EMAIL'", 'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_preferred': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'base.person': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Person'},
            'address': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['base.Place']", 'null': 'True', 'blank': 'True'}),
            'avatar': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'contact_set': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['base.Contact']", 'null': 'True', 'blank': 'True'}),
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'ssn': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'base.place': {
            'Meta': {'ordering': "('name', 'address', 'city')", 'object_name': 'Place'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'lon': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'province': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'des.des': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'DES', '_ormbases': ['sites.Site']},
            'cfg_time': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'info_people_set': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['base.Person']", 'null': 'True', 'blank': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'site_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['sites.Site']", 'unique': 'True', 'primary_key': 'True'})
        },
        'gas.delivery': {
            'Meta': {'object_name': 'Delivery'},
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'delivery_set'", 'to': "orm['base.Place']"})
        },
        'gas.gas': {
            'Meta': {'ordering': "('-birthday',)", 'object_name': 'GAS'},
            'activist_set': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['base.Person']", 'null': 'True', 'through': "orm['gas.GASActivist']", 'blank': 'True'}),
            'association_act': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'birthday': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'contact_set': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['base.Contact']", 'null': 'True', 'blank': 'True'}),
            'des': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['des.DES']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'fcc': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'headquarter': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'gas_headquarter_set'", 'to': "orm['base.Place']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_in_des': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '8'}),
            'intent_act': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'membership_fee': ('gasistafelice.lib.fields.models.CurrencyField', [], {'default': "'0'", 'max_digits': '10', 'decimal_places': '4', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'orders_email_contact': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'gas_use_for_orders_set'", 'null': 'True', 'to': "orm['base.Contact']"}),
            'supplier_set': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['supplier.Supplier']", 'null': 'True', 'through': "orm['gas.GASSupplierSolidalPact']", 'blank': 'True'}),
            'vat': ('django.db.models.fields.CharField', [], {'max_length': '11', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'gas.gasactivist': {
            'Meta': {'object_name': 'GASActivist'},
            'gas': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gas.GAS']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'info_title': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['base.Person']"})
        },
        'gas.gasconfig': {
            'Meta': {'object_name': 'GASConfig'},
            'auto_populate_products': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'can_change_delivery_place_on_each_order': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'can_change_price': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'can_change_withdrawal_place_on_each_order': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'default_close_day': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'default_close_time': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'default_delivery_day': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'default_delivery_place': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'gas_default_delivery_set'", 'null': 'True', 'to': "orm['base.Place']"}),
            'default_delivery_time': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'default_withdrawal_place': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'gas_default_withdrawal_set'", 'null': 'True', 'to': "orm['base.Place']"}),
            'default_workflow_gasmember_order': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'gmow_gasconfig_set'", 'blank': 'True', 'to': "orm['workflows.Workflow']"}),
            'default_workflow_gassupplier_order': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'gsopw_gasconfig_set'", 'blank': 'True', 'to': "orm['workflows.Workflow']"}),
            'gas': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'config'", 'unique': 'True', 'to': "orm['gas.GAS']"}),
            'gasmember_auto_confirm_order': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_suspended': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'notice_days_before_order_close': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1', 'null': 'True'}),
            'order_show_only_next_delivery': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'order_show_only_one_at_a_time': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'suspend_auto_resume': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'suspend_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'suspend_reason': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'use_scheduler': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'use_withdrawal_place': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'gas.gasmember': {
            'Meta': {'ordering': "('gas__name',)", 'unique_together': "(('gas', 'id_in_gas'), ('person', 'gas'))", 'object_name': 'GASMember'},
            'available_for_roles': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'gas_member_available_set'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['permissions.Role']"}),
            'gas': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gas.GAS']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_in_gas': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'membership_fee_payed': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['base.Person']"}),
            'user_planned_list': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'gas.gasmemberorder': {
            'Meta': {'unique_together': "(('ordered_product', 'purchaser'),)", 'object_name': 'GASMemberOrder'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'note': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'ordered_amount': ('gasistafelice.lib.fields.models.PrettyDecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            'ordered_price': ('gasistafelice.lib.fields.models.CurrencyField', [], {'max_digits': '10', 'decimal_places': '4'}),
            'ordered_product': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'gasmember_order_set'", 'to': "orm['gas.GASSupplierOrderProduct']"}),
            'purchaser': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'gasmember_order_set'", 'to': "orm['gas.GASMember']"}),
            'withdrawn_amount': ('gasistafelice.lib.fields.models.PrettyDecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '2', 'blank': 'True'})
        },
        'gas.gassupplierorder': {
            'Meta': {'ordering': "('datetime_end', 'datetime_start')", 'object_name': 'GASSupplierOrder'},
            'datetime_end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'datetime_start': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'delivery': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'order_set'", 'null': 'True', 'to': "orm['gas.Delivery']"}),
            'delivery_cost': ('gasistafelice.lib.fields.models.CurrencyField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '4', 'blank': 'True'}),
            'delivery_referrer_person': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'delivery_for_order_set'", 'null': 'True', 'to': "orm['base.Person']"}),
            'gasstock_set': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['gas.GASSupplierStock']", 'symmetrical': 'False', 'through': "orm['gas.GASSupplierOrderProduct']", 'blank': 'True'}),
            'group_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice_amount': ('gasistafelice.lib.fields.models.CurrencyField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '4', 'blank': 'True'}),
            'invoice_note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'order_minimum_amount': ('gasistafelice.lib.fields.models.CurrencyField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '4', 'blank': 'True'}),
            'pact': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'order_set'", 'to': "orm['gas.GASSupplierSolidalPact']"}),
            'referrer_person': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'order_set'", 'null': 'True', 'to': "orm['base.Person']"}),
            'root_plan': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['gas.GASSupplierOrder']", 'null': 'True', 'blank': 'True'}),
            'withdrawal': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'order_set'", 'null': 'True', 'to': "orm['gas.Withdrawal']"}),
            'withdrawal_referrer_person': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'withdrawal_for_order_set'", 'null': 'True', 'to': "orm['base.Person']"})
        },
        'gas.gassupplierorderproduct': {
            'Meta': {'ordering': "('gasstock__stock__supplier__name', 'gasstock__stock__supplier_category__sorting', 'gasstock__stock__product__category__name', 'gasstock__stock__product__name')", 'object_name': 'GASSupplierOrderProduct'},
            'delivered_amount': ('gasistafelice.lib.fields.models.PrettyDecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '2', 'blank': 'True'}),
            'delivered_price': ('gasistafelice.lib.fields.models.CurrencyField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '4', 'blank': 'True'}),
            'gasstock': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'orderable_product_set'", 'to': "orm['gas.GASSupplierStock']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initial_price': ('gasistafelice.lib.fields.models.CurrencyField', [], {'max_digits': '10', 'decimal_places': '4'}),
            'maximum_amount': ('gasistafelice.lib.fields.models.PrettyDecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '2', 'blank': 'True'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'orderable_product_set'", 'to': "orm['gas.GASSupplierOrder']"}),
            'order_price': ('gasistafelice.lib.fields.models.CurrencyField', [], {'max_digits': '10', 'decimal_places': '4'})
        },
        'gas.gassuppliersolidalpact': {
            'Meta': {'unique_together': "(('gas', 'supplier'),)", 'object_name': 'GASSupplierSolidalPact'},
            'auto_populate_products': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'date_signed': ('django.db.models.fields.DateField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'default_delivery_day': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'default_delivery_place': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'pact_default_delivery_place_set'", 'null': 'True', 'to': "orm['base.Place']"}),
            'default_delivery_time': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'document': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'gas': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pact_set'", 'to': "orm['gas.GAS']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_suspended': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'order_deliver_interval': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'order_delivery_cost': ('gasistafelice.lib.fields.models.CurrencyField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '4', 'blank': 'True'}),
            'order_minimum_amount': ('gasistafelice.lib.fields.models.CurrencyField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '4', 'blank': 'True'}),
            'order_price_percent_update': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '3', 'decimal_places': '2', 'blank': 'True'}),
            'orders_can_be_grouped': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'stock_set': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['supplier.SupplierStock']", 'null': 'True', 'through': "orm['gas.GASSupplierStock']", 'blank': 'True'}),
            'supplier': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pact_set'", 'to': "orm['supplier.Supplier']"}),
            'suspend_auto_resume': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'suspend_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'suspend_reason': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'})
        },
        'gas.gassupplierstock': {
            'Meta': {'object_name': 'GASSupplierStock'},
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'minimum_amount': ('gasistafelice.lib.fields.models.PrettyDecimalField', [], {'default': '1', 'max_digits': '5', 'decimal_places': '2'}),
            'pact': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'gasstock_set'", 'to': "orm['gas.GASSupplierSolidalPact']"}),
            'step': ('gasistafelice.lib.fields.models.PrettyDecimalField', [], {'default': '1', 'max_digits': '5', 'decimal_places': '2'}),
            'stock': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'gasstock_set'", 'to': "orm['supplier.SupplierStock']"})
        },
        'gas.historicaldelivery': {
            'Meta': {'ordering': "('-history_date',)", 'object_name': 'HistoricalDelivery'},
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'history_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'history_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'history_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'history_user': ('current_user.models.CurrentUserField', [], {'related_name': "'_delivery_history'", 'null': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'blank': 'True'}),
            'place_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'})
        },
        'gas.historicalgas': {
            'Meta': {'ordering': "('-history_date',)", 'object_name': 'HistoricalGAS'},
            'association_act': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'birthday': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'des_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'fcc': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'headquarter_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'history_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'history_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'history_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'history_user': ('current_user.models.CurrentUserField', [], {'related_name': "'_gas_history'", 'null': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'blank': 'True'}),
            'id_in_des': ('django.db.models.fields.CharField', [], {'max_length': '8', 'db_index': 'True'}),
            'intent_act': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'membership_fee': ('gasistafelice.lib.fields.models.CurrencyField', [], {'default': "'0'", 'max_digits': '10', 'decimal_places': '4', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'db_index': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'orders_email_contact_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'vat': ('django.db.models.fields.CharField', [], {'max_length': '11', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'gas.historicalgasactivist': {
            'Meta': {'ordering': "('-history_date',)", 'object_name': 'HistoricalGASActivist'},
            'gas_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'history_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'history_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'history_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'history_user': ('current_user.models.CurrentUserField', [], {'related_name': "'_gasactivist_history'", 'null': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'blank': 'True'}),
            'info_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'info_title': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'person_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'})
        },
        'gas.historicalgasconfig': {
            'Meta': {'ordering': "('-history_date',)", 'object_name': 'HistoricalGASConfig'},
            'auto_populate_products': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'can_change_delivery_place_on_each_order': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'can_change_price': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'can_change_withdrawal_place_on_each_order': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'default_close_day': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'default_close_time': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'default_delivery_day': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'default_delivery_place_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'default_delivery_time': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'default_withdrawal_place_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'default_workflow_gasmember_order_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'default_workflow_gassupplier_order_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'gas_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'gasmember_auto_confirm_order': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'history_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'history_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'history_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'history_user': ('current_user.models.CurrentUserField', [], {'related_name': "'_gasconfig_history'", 'null': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'blank': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_suspended': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'notice_days_before_order_close': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1', 'null': 'True'}),
            'order_show_only_next_delivery': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'order_show_only_one_at_a_time': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'suspend_auto_resume': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'suspend_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'suspend_reason': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'use_scheduler': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'use_withdrawal_place': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'gas.historicalgasmember': {
            'Meta': {'ordering': "('-history_date',)", 'object_name': 'HistoricalGASMember'},
            'gas_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'history_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'history_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'history_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'history_user': ('current_user.models.CurrentUserField', [], {'related_name': "'_gasmember_history'", 'null': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'blank': 'True'}),
            'id_in_gas': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'membership_fee_payed': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'person_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'user_planned_list': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'gas.historicalgasmemberorder': {
            'Meta': {'ordering': "('-history_date',)", 'object_name': 'HistoricalGASMemberOrder'},
            'history_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'history_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'history_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'history_user': ('current_user.models.CurrentUserField', [], {'related_name': "'_gasmemberorder_history'", 'null': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'blank': 'True'}),
            'is_confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'note': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'ordered_amount': ('gasistafelice.lib.fields.models.PrettyDecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            'ordered_price': ('gasistafelice.lib.fields.models.CurrencyField', [], {'max_digits': '10', 'decimal_places': '4'}),
            'ordered_product_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'purchaser_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'withdrawn_amount': ('gasistafelice.lib.fields.models.PrettyDecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '2', 'blank': 'True'})
        },
        'gas.historicalgassupplierorder': {
            'Meta': {'ordering': "('-history_date',)", 'object_name': 'HistoricalGASSupplierOrder'},
            'datetime_end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'datetime_start': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'delivery_cost': ('gasistafelice.lib.fields.models.CurrencyField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '4', 'blank': 'True'}),
            'delivery_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'delivery_referrer_person_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'group_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'history_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'history_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'history_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'history_user': ('current_user.models.CurrentUserField', [], {'related_name': "'_gassupplierorder_history'", 'null': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'blank': 'True'}),
            'invoice_amount': ('gasistafelice.lib.fields.models.CurrencyField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '4', 'blank': 'True'}),
            'invoice_note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'order_minimum_amount': ('gasistafelice.lib.fields.models.CurrencyField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '4', 'blank': 'True'}),
            'pact_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'referrer_person_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'root_plan_id': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'withdrawal_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'withdrawal_referrer_person_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'})
        },
        'gas.historicalgassupplierorderproduct': {
            'Meta': {'ordering': "('-history_date',)", 'object_name': 'HistoricalGASSupplierOrderProduct'},
            'delivered_amount': ('gasistafelice.lib.fields.models.PrettyDecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '2', 'blank': 'True'}),
            'delivered_price': ('gasistafelice.lib.fields.models.CurrencyField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '4', 'blank': 'True'}),
            'gasstock_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'history_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'history_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'history_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'history_user': ('current_user.models.CurrentUserField', [], {'related_name': "'_gassupplierorderproduct_history'", 'null': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'blank': 'True'}),
            'initial_price': ('gasistafelice.lib.fields.models.CurrencyField', [], {'max_digits': '10', 'decimal_places': '4'}),
            'maximum_amount': ('gasistafelice.lib.fields.models.PrettyDecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '2', 'blank': 'True'}),
            'order_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'order_price': ('gasistafelice.lib.fields.models.CurrencyField', [], {'max_digits': '10', 'decimal_places': '4'})
        },
        'gas.historicalgassuppliersolidalpact': {
            'Meta': {'ordering': "('-history_date',)", 'object_name': 'HistoricalGASSupplierSolidalPact'},
            'auto_populate_products': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'date_signed': ('django.db.models.fields.DateField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'default_delivery_day': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'default_delivery_place_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'default_delivery_time': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'document': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'gas_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'history_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'history_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'history_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'history_user': ('current_user.models.CurrentUserField', [], {'related_name': "'_gassuppliersolidalpact_history'", 'null': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'blank': 'True'}),
            'is_suspended': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'order_deliver_interval': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'order_delivery_cost': ('gasistafelice.lib.fields.models.CurrencyField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '4', 'blank': 'True'}),
            'order_minimum_amount': ('gasistafelice.lib.fields.models.CurrencyField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '4', 'blank': 'True'}),
            'order_price_percent_update': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '3', 'decimal_places': '2', 'blank': 'True'}),
            'orders_can_be_grouped': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'supplier_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'suspend_auto_resume': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'suspend_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'suspend_reason': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'})
        },
        'gas.historicalgassupplierstock': {
            'Meta': {'ordering': "('-history_date',)", 'object_name': 'HistoricalGASSupplierStock'},
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'history_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'history_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'history_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'history_user': ('current_user.models.CurrentUserField', [], {'related_name': "'_gassupplierstock_history'", 'null': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'blank': 'True'}),
            'minimum_amount': ('gasistafelice.lib.fields.models.PrettyDecimalField', [], {'default': '1', 'max_digits': '5', 'decimal_places': '2'}),
            'pact_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'step': ('gasistafelice.lib.fields.models.PrettyDecimalField', [], {'default': '1', 'max_digits': '5', 'decimal_places': '2'}),
            'stock_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'})
        },
        'gas.historicalwithdrawal': {
            'Meta': {'ordering': "('-history_date',)", 'object_name': 'HistoricalWithdrawal'},
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'end_time': ('django.db.models.fields.TimeField', [], {'default': "'22:00'"}),
            'history_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'history_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'history_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'history_user': ('current_user.models.CurrentUserField', [], {'related_name': "'_withdrawal_history'", 'null': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'blank': 'True'}),
            'place_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'start_time': ('django.db.models.fields.TimeField', [], {'default': "'18:00'"})
        },
        'gas.withdrawal': {
            'Meta': {'object_name': 'Withdrawal'},
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'end_time': ('django.db.models.fields.TimeField', [], {'default': "'22:00'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'withdrawal_set'", 'to': "orm['base.Place']"}),
            'start_time': ('django.db.models.fields.TimeField', [], {'default': "'18:00'"})
        },
        'permissions.permission': {
            'Meta': {'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'content_types': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'content_types'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'permissions.role': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Role'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'supplier.certification': {
            'Meta': {'ordering': "['name']", 'object_name': 'Certification'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'}),
            'symbol': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '5'})
        },
        'supplier.product': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Product'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'product_set'", 'blank': 'True', 'to': "orm['supplier.ProductCategory']"}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mu': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['supplier.ProductMU']", 'null': 'True', 'blank': 'True'}),
            'muppu': ('gasistafelice.lib.fields.models.PrettyDecimalField', [], {'default': "'1.00'", 'null': 'True', 'max_digits': '6', 'decimal_places': '2'}),
            'muppu_is_variable': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'producer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'produced_product_set'", 'to': "orm['supplier.Supplier']"}),
            'pu': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['supplier.ProductPU']"}),
            'vat_percent': ('django.db.models.fields.DecimalField', [], {'default': "'0.21'", 'max_digits': '3', 'decimal_places': '2'})
        },
        'supplier.productcategory': {
            'Meta': {'ordering': "('name',)", 'object_name': 'ProductCategory'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        },
        'supplier.productmu': {
            'Meta': {'ordering': "('name',)", 'object_name': 'ProductMU'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'symbol': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '5'})
        },
        'supplier.productpu': {
            'Meta': {'ordering': "('name',)", 'object_name': 'ProductPU'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'symbol': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '5'})
        },
        'supplier.supplier': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Supplier'},
            'agent_set': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['base.Person']", 'through': "orm['supplier.SupplierAgent']", 'symmetrical': 'False'}),
            'certifications': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['supplier.Certification']", 'null': 'True', 'blank': 'True'}),
            'contact_set': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['base.Contact']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'flavour': ('django.db.models.fields.CharField', [], {'default': "'COMPANY'", 'max_length': '128'}),
            'frontman': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'supplier_frontman_set'", 'null': 'True', 'to': "orm['base.Person']"}),
            'iban': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'n_employers': ('django.db.models.fields.PositiveIntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'seat': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['base.Place']", 'null': 'True', 'blank': 'True'}),
            'ssn': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'vat_number': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
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
        'supplier.supplierproductcategory': {
            'Meta': {'ordering': "('supplier', 'sorting')", 'object_name': 'SupplierProductCategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'sorting': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'supplier': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['supplier.Supplier']"})
        },
        'supplier.supplierstock': {
            'Meta': {'ordering': "('supplier_category__sorting', 'product__category')", 'object_name': 'SupplierStock'},
            'amount_available': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1000000000'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'delivery_notes': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'detail_minimum_amount': ('gasistafelice.lib.fields.models.PrettyDecimalField', [], {'default': '1', 'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'detail_step': ('gasistafelice.lib.fields.models.PrettyDecimalField', [], {'default': '1', 'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'price': ('gasistafelice.lib.fields.models.CurrencyField', [], {'max_digits': '10', 'decimal_places': '4'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stock_set'", 'to': "orm['supplier.Product']"}),
            'supplier': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stock_set'", 'to': "orm['supplier.Supplier']"}),
            'supplier_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['supplier.SupplierProductCategory']", 'null': 'True', 'blank': 'True'}),
            'units_minimum_amount': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'units_per_box': ('gasistafelice.lib.fields.models.PrettyDecimalField', [], {'default': '1', 'max_digits': '5', 'decimal_places': '2'})
        },
        'workflows.state': {
            'Meta': {'ordering': "('name',)", 'object_name': 'State'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'transitions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'states'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['workflows.Transition']"}),
            'workflow': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'states'", 'to': "orm['workflows.Workflow']"})
        },
        'workflows.transition': {
            'Meta': {'object_name': 'Transition'},
            'condition': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'destination': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'destination_state'", 'null': 'True', 'to': "orm['workflows.State']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'permission': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['permissions.Permission']", 'null': 'True', 'blank': 'True'}),
            'workflow': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'transitions'", 'to': "orm['workflows.Workflow']"})
        },
        'workflows.workflow': {
            'Meta': {'object_name': 'Workflow'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initial_state': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'workflow_state'", 'null': 'True', 'to': "orm['workflows.State']"}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['permissions.Permission']", 'through': "orm['workflows.WorkflowPermissionRelation']", 'symmetrical': 'False'})
        },
        'workflows.workflowpermissionrelation': {
            'Meta': {'unique_together': "(('workflow', 'permission'),)", 'object_name': 'WorkflowPermissionRelation'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'permission': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'permissions'", 'to': "orm['permissions.Permission']"}),
            'workflow': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['workflows.Workflow']"})
        }
    }

    complete_apps = ['gas']
