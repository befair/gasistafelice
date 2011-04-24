# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'HistoricalPerson'
        db.create_table('base_historicalperson', (
            ('id', self.gf('django.db.models.fields.IntegerField')(db_index=True, blank=True)),
            ('uuid', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=128, null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('surname', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('display_name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], null=True, blank=True)),
            ('history_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('history_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('history_user', self.gf('current_user.models.CurrentUserField')(related_name='_person_history', null=True, to=orm['auth.User'])),
            ('history_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('base', ['HistoricalPerson'])

        # Adding model 'Person'
        db.create_table('base_person', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=128, unique=True, null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('surname', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('display_name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, null=True, blank=True)),
        ))
        db.send_create_signal('base', ['Person'])

        # Adding M2M table for field contacts on 'Person'
        db.create_table('base_person_contacts', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('person', models.ForeignKey(orm['base.person'], null=False)),
            ('contact', models.ForeignKey(orm['base.contact'], null=False))
        ))
        db.create_unique('base_person_contacts', ['person_id', 'contact_id'])

        # Adding model 'HistoricalContact'
        db.create_table('base_historicalcontact', (
            ('id', self.gf('django.db.models.fields.IntegerField')(db_index=True, blank=True)),
            ('contact_type', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('contact_value', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('history_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('history_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('history_user', self.gf('current_user.models.CurrentUserField')(related_name='_contact_history', null=True, to=orm['auth.User'])),
            ('history_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('base', ['HistoricalContact'])

        # Adding model 'Contact'
        db.create_table('base_contact', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('contact_type', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('contact_value', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal('base', ['Contact'])

        # Adding model 'HistoricalPlace'
        db.create_table('base_historicalplace', (
            ('id', self.gf('django.db.models.fields.IntegerField')(db_index=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('province', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('lon', self.gf('django.db.models.fields.FloatField')(blank=True)),
            ('lat', self.gf('django.db.models.fields.FloatField')(blank=True)),
            ('history_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('history_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('history_user', self.gf('current_user.models.CurrentUserField')(related_name='_place_history', null=True, to=orm['auth.User'])),
            ('history_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('base', ['HistoricalPlace'])

        # Adding model 'Place'
        db.create_table('base_place', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('province', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('lon', self.gf('django.db.models.fields.FloatField')(blank=True)),
            ('lat', self.gf('django.db.models.fields.FloatField')(blank=True)),
        ))
        db.send_create_signal('base', ['Place'])

        # Adding model 'HistoricalDefaultTransition'
        db.create_table('base_historicaldefaulttransition', (
            ('id', self.gf('django.db.models.fields.IntegerField')(db_index=True, blank=True)),
            ('workflow', self.gf('django.db.models.fields.related.ForeignKey')(related_name='historicaldefault_transition_set', to=orm['workflows.Workflow'])),
            ('state', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['workflows.State'])),
            ('transition', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['workflows.Transition'])),
            ('history_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('history_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('history_user', self.gf('current_user.models.CurrentUserField')(related_name='_defaulttransition_history', null=True, to=orm['auth.User'])),
            ('history_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('base', ['HistoricalDefaultTransition'])

        # Adding model 'DefaultTransition'
        db.create_table('base_defaulttransition', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('workflow', self.gf('django.db.models.fields.related.ForeignKey')(related_name='default_transition_set', to=orm['workflows.Workflow'])),
            ('state', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['workflows.State'])),
            ('transition', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['workflows.Transition'])),
        ))
        db.send_create_signal('base', ['DefaultTransition'])


    def backwards(self, orm):
        
        # Deleting model 'HistoricalPerson'
        db.delete_table('base_historicalperson')

        # Deleting model 'Person'
        db.delete_table('base_person')

        # Removing M2M table for field contacts on 'Person'
        db.delete_table('base_person_contacts')

        # Deleting model 'HistoricalContact'
        db.delete_table('base_historicalcontact')

        # Deleting model 'Contact'
        db.delete_table('base_contact')

        # Deleting model 'HistoricalPlace'
        db.delete_table('base_historicalplace')

        # Deleting model 'Place'
        db.delete_table('base_place')

        # Deleting model 'HistoricalDefaultTransition'
        db.delete_table('base_historicaldefaulttransition')

        # Deleting model 'DefaultTransition'
        db.delete_table('base_defaulttransition')


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
        'base.defaulttransition': {
            'Meta': {'object_name': 'DefaultTransition'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['workflows.State']"}),
            'transition': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['workflows.Transition']"}),
            'workflow': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'default_transition_set'", 'to': "orm['workflows.Workflow']"})
        },
        'base.historicalcontact': {
            'Meta': {'ordering': "('-history_date',)", 'object_name': 'HistoricalContact'},
            'contact_type': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'contact_value': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'history_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'history_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'history_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'history_user': ('current_user.models.CurrentUserField', [], {'related_name': "'_contact_history'", 'null': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'blank': 'True'})
        },
        'base.historicaldefaulttransition': {
            'Meta': {'ordering': "('-history_date',)", 'object_name': 'HistoricalDefaultTransition'},
            'history_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'history_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'history_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'history_user': ('current_user.models.CurrentUserField', [], {'related_name': "'_defaulttransition_history'", 'null': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['workflows.State']"}),
            'transition': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['workflows.Transition']"}),
            'workflow': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'historicaldefault_transition_set'", 'to': "orm['workflows.Workflow']"})
        },
        'base.historicalperson': {
            'Meta': {'ordering': "('-history_date',)", 'object_name': 'HistoricalPerson'},
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'history_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'history_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'history_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'history_user': ('current_user.models.CurrentUserField', [], {'related_name': "'_person_history'", 'null': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '128', 'null': 'True', 'blank': 'True'})
        },
        'base.historicalplace': {
            'Meta': {'ordering': "('-history_date',)", 'object_name': 'HistoricalPlace'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'history_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'history_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'history_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'history_user': ('current_user.models.CurrentUserField', [], {'related_name': "'_place_history'", 'null': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'blank': 'True'}),
            'lat': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'lon': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'province': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'})
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
        'permissions.permission': {
            'Meta': {'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'content_types': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'content_types'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
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

    complete_apps = ['base']
