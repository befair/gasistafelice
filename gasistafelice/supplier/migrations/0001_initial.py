# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'HistoricalSupplier'
        db.create_table('supplier_historicalsupplier', (
            ('id', self.gf('django.db.models.fields.IntegerField')(db_index=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('seat', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.Place'])),
            ('vat_number', self.gf('django.db.models.fields.CharField')(max_length=128, db_index=True)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('flavour', self.gf('django.db.models.fields.CharField')(default='COMPANY', max_length=128)),
            ('history_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('history_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('history_user', self.gf('current_user.models.CurrentUserField')(related_name='_supplier_history', null=True, to=orm['auth.User'])),
            ('history_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('supplier', ['HistoricalSupplier'])

        # Adding model 'Supplier'
        db.create_table('supplier_supplier', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('seat', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.Place'])),
            ('vat_number', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('flavour', self.gf('django.db.models.fields.CharField')(default='COMPANY', max_length=128)),
        ))
        db.send_create_signal('supplier', ['Supplier'])

        # Adding M2M table for field certifications on 'Supplier'
        db.create_table('supplier_supplier_certifications', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('supplier', models.ForeignKey(orm['supplier.supplier'], null=False)),
            ('certification', models.ForeignKey(orm['supplier.certification'], null=False))
        ))
        db.create_unique('supplier_supplier_certifications', ['supplier_id', 'certification_id'])

        # Adding model 'HistoricalSupplierReferrer'
        db.create_table('supplier_historicalsupplierreferrer', (
            ('id', self.gf('django.db.models.fields.IntegerField')(db_index=True, blank=True)),
            ('supplier', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['supplier.Supplier'])),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.Person'])),
            ('job_title', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('job_description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('history_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('history_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('history_user', self.gf('current_user.models.CurrentUserField')(related_name='_supplierreferrer_history', null=True, to=orm['auth.User'])),
            ('history_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('supplier', ['HistoricalSupplierReferrer'])

        # Adding model 'SupplierReferrer'
        db.create_table('supplier_supplierreferrer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('supplier', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['supplier.Supplier'])),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.Person'])),
            ('job_title', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('job_description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('supplier', ['SupplierReferrer'])

        # Adding model 'HistoricalCertification'
        db.create_table('supplier_historicalcertification', (
            ('id', self.gf('django.db.models.fields.IntegerField')(db_index=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128, db_index=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('history_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('history_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('history_user', self.gf('current_user.models.CurrentUserField')(related_name='_certification_history', null=True, to=orm['auth.User'])),
            ('history_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('supplier', ['HistoricalCertification'])

        # Adding model 'Certification'
        db.create_table('supplier_certification', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('supplier', ['Certification'])

        # Adding model 'HistoricalProductCategory'
        db.create_table('supplier_historicalproductcategory', (
            ('id', self.gf('django.db.models.fields.IntegerField')(db_index=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128, db_index=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('history_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('history_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('history_user', self.gf('current_user.models.CurrentUserField')(related_name='_productcategory_history', null=True, to=orm['auth.User'])),
            ('history_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('supplier', ['HistoricalProductCategory'])

        # Adding model 'ProductCategory'
        db.create_table('supplier_productcategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('supplier', ['ProductCategory'])

        # Adding model 'HistoricalProductMU'
        db.create_table('supplier_historicalproductmu', (
            ('id', self.gf('django.db.models.fields.IntegerField')(db_index=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32, db_index=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('history_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('history_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('history_user', self.gf('current_user.models.CurrentUserField')(related_name='_productmu_history', null=True, to=orm['auth.User'])),
            ('history_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('supplier', ['HistoricalProductMU'])

        # Adding model 'ProductMU'
        db.create_table('supplier_productmu', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=32)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('supplier', ['ProductMU'])

        # Adding model 'HistoricalProduct'
        db.create_table('supplier_historicalproduct', (
            ('id', self.gf('django.db.models.fields.IntegerField')(db_index=True, blank=True)),
            ('uuid', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=128, null=True, blank=True)),
            ('producer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['supplier.Supplier'])),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['supplier.ProductCategory'])),
            ('mu', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['supplier.ProductMU'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('history_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('history_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('history_user', self.gf('current_user.models.CurrentUserField')(related_name='_product_history', null=True, to=orm['auth.User'])),
            ('history_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('supplier', ['HistoricalProduct'])

        # Adding model 'Product'
        db.create_table('supplier_product', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=128, unique=True, null=True, blank=True)),
            ('producer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['supplier.Supplier'])),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['supplier.ProductCategory'])),
            ('mu', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['supplier.ProductMU'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('supplier', ['Product'])

        # Adding model 'HistoricalSupplierStock'
        db.create_table('supplier_historicalsupplierstock', (
            ('id', self.gf('django.db.models.fields.IntegerField')(db_index=True, blank=True)),
            ('supplier', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['supplier.Supplier'])),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['supplier.Product'])),
            ('price', self.gf('django.db.models.fields.FloatField')()),
            ('amount_available', self.gf('django.db.models.fields.PositiveIntegerField')(default=1000000000)),
            ('order_minimum_amount', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('order_step', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('delivery_terms', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('history_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('history_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('history_user', self.gf('current_user.models.CurrentUserField')(related_name='_supplierstock_history', null=True, to=orm['auth.User'])),
            ('history_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('supplier', ['HistoricalSupplierStock'])

        # Adding model 'SupplierStock'
        db.create_table('supplier_supplierstock', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('supplier', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['supplier.Supplier'])),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['supplier.Product'])),
            ('price', self.gf('django.db.models.fields.FloatField')()),
            ('amount_available', self.gf('django.db.models.fields.PositiveIntegerField')(default=1000000000)),
            ('order_minimum_amount', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('order_step', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('delivery_terms', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('supplier', ['SupplierStock'])


    def backwards(self, orm):
        
        # Deleting model 'HistoricalSupplier'
        db.delete_table('supplier_historicalsupplier')

        # Deleting model 'Supplier'
        db.delete_table('supplier_supplier')

        # Removing M2M table for field certifications on 'Supplier'
        db.delete_table('supplier_supplier_certifications')

        # Deleting model 'HistoricalSupplierReferrer'
        db.delete_table('supplier_historicalsupplierreferrer')

        # Deleting model 'SupplierReferrer'
        db.delete_table('supplier_supplierreferrer')

        # Deleting model 'HistoricalCertification'
        db.delete_table('supplier_historicalcertification')

        # Deleting model 'Certification'
        db.delete_table('supplier_certification')

        # Deleting model 'HistoricalProductCategory'
        db.delete_table('supplier_historicalproductcategory')

        # Deleting model 'ProductCategory'
        db.delete_table('supplier_productcategory')

        # Deleting model 'HistoricalProductMU'
        db.delete_table('supplier_historicalproductmu')

        # Deleting model 'ProductMU'
        db.delete_table('supplier_productmu')

        # Deleting model 'HistoricalProduct'
        db.delete_table('supplier_historicalproduct')

        # Deleting model 'Product'
        db.delete_table('supplier_product')

        # Deleting model 'HistoricalSupplierStock'
        db.delete_table('supplier_historicalsupplierstock')

        # Deleting model 'SupplierStock'
        db.delete_table('supplier_supplierstock')


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
        'supplier.certification': {
            'Meta': {'object_name': 'Certification'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        },
        'supplier.historicalcertification': {
            'Meta': {'ordering': "('-history_date',)", 'object_name': 'HistoricalCertification'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'history_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'history_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'history_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'history_user': ('current_user.models.CurrentUserField', [], {'related_name': "'_certification_history'", 'null': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'db_index': 'True'})
        },
        'supplier.historicalproduct': {
            'Meta': {'ordering': "('-history_date',)", 'object_name': 'HistoricalProduct'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['supplier.ProductCategory']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'history_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'history_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'history_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'history_user': ('current_user.models.CurrentUserField', [], {'related_name': "'_product_history'", 'null': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'blank': 'True'}),
            'mu': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['supplier.ProductMU']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'producer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['supplier.Supplier']"}),
            'uuid': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '128', 'null': 'True', 'blank': 'True'})
        },
        'supplier.historicalproductcategory': {
            'Meta': {'ordering': "('-history_date',)", 'object_name': 'HistoricalProductCategory'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'history_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'history_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'history_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'history_user': ('current_user.models.CurrentUserField', [], {'related_name': "'_productcategory_history'", 'null': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'db_index': 'True'})
        },
        'supplier.historicalproductmu': {
            'Meta': {'ordering': "('-history_date',)", 'object_name': 'HistoricalProductMU'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'history_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'history_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'history_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'history_user': ('current_user.models.CurrentUserField', [], {'related_name': "'_productmu_history'", 'null': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'db_index': 'True'})
        },
        'supplier.historicalsupplier': {
            'Meta': {'ordering': "('-history_date',)", 'object_name': 'HistoricalSupplier'},
            'flavour': ('django.db.models.fields.CharField', [], {'default': "'COMPANY'", 'max_length': '128'}),
            'history_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'history_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'history_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'history_user': ('current_user.models.CurrentUserField', [], {'related_name': "'_supplier_history'", 'null': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'seat': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['base.Place']"}),
            'vat_number': ('django.db.models.fields.CharField', [], {'max_length': '128', 'db_index': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'supplier.historicalsupplierreferrer': {
            'Meta': {'ordering': "('-history_date',)", 'object_name': 'HistoricalSupplierReferrer'},
            'history_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'history_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'history_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'history_user': ('current_user.models.CurrentUserField', [], {'related_name': "'_supplierreferrer_history'", 'null': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'blank': 'True'}),
            'job_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'job_title': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['base.Person']"}),
            'supplier': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['supplier.Supplier']"})
        },
        'supplier.historicalsupplierstock': {
            'Meta': {'ordering': "('-history_date',)", 'object_name': 'HistoricalSupplierStock'},
            'amount_available': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1000000000'}),
            'delivery_terms': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'history_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'history_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'history_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'history_user': ('current_user.models.CurrentUserField', [], {'related_name': "'_supplierstock_history'", 'null': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'blank': 'True'}),
            'order_minimum_amount': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'order_step': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['supplier.Product']"}),
            'supplier': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['supplier.Supplier']"})
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
            'referrers': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['base.Person']", 'through': "orm['supplier.SupplierReferrer']", 'symmetrical': 'False'}),
            'seat': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['base.Place']"}),
            'vat_number': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'supplier.supplierreferrer': {
            'Meta': {'object_name': 'SupplierReferrer'},
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

    complete_apps = ['supplier']
