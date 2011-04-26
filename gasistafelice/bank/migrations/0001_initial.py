# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Account'
        db.create_table('bank_account', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('balance', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=4)),
        ))
        db.send_create_signal('bank', ['Account'])

        # Adding model 'Movement'
        db.create_table('bank_movement', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bank.Account'])),
            ('balance', self.gf('gasistafelice.base.fields.CurrencyField')(max_digits=10, decimal_places=4)),
            ('causal', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('bank', ['Movement'])


    def backwards(self, orm):
        
        # Deleting model 'Account'
        db.delete_table('bank_account')

        # Deleting model 'Movement'
        db.delete_table('bank_movement')


    models = {
        'bank.account': {
            'Meta': {'object_name': 'Account'},
            'balance': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '4'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'bank.movement': {
            'Meta': {'object_name': 'Movement'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bank.Account']"}),
            'balance': ('gasistafelice.base.fields.CurrencyField', [], {'max_digits': '10', 'decimal_places': '4'}),
            'causal': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['bank']
