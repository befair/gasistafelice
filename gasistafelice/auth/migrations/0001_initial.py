# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Permission'
        db.create_table('auth_permission', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('codename', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('auth', ['Permission'])

        # Adding unique constraint on 'Permission', fields ['content_type', 'codename']
        db.create_unique('auth_permission', ['content_type_id', 'codename'])

        # Adding model 'Group'
        db.create_table('auth_group', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=80)),
        ))
        db.send_create_signal('auth', ['Group'])

        # Adding M2M table for field permissions on 'Group'
        db.create_table('auth_group_permissions', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('group', models.ForeignKey(orm['auth.group'], null=False)),
            ('permission', models.ForeignKey(orm['auth.permission'], null=False))
        ))
        db.create_unique('auth_group_permissions', ['group_id', 'permission_id'])

        # Adding model 'User'
        db.create_table('auth_user', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('username', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('is_staff', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_superuser', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('date_joined', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal('auth', ['User'])

        # Adding M2M table for field groups on 'User'
        db.create_table('auth_user_groups', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('user', models.ForeignKey(orm['auth.user'], null=False)),
            ('group', models.ForeignKey(orm['auth.group'], null=False))
        ))
        db.create_unique('auth_user_groups', ['user_id', 'group_id'])

        # Adding M2M table for field user_permissions on 'User'
        db.create_table('auth_user_user_permissions', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('user', models.ForeignKey(orm['auth.user'], null=False)),
            ('permission', models.ForeignKey(orm['auth.permission'], null=False))
        ))
        db.create_unique('auth_user_user_permissions', ['user_id', 'permission_id'])

        # Adding model 'Message'
        db.create_table('auth_message', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_message_set', to=orm['auth.User'])),
            ('message', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('auth', ['Message'])

        # Adding model 'Param'
        db.create_table('auth_param', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('auth', ['Param'])

        # Adding model 'ParamRole'
        db.create_table('auth_paramrole', (
            ('role', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['permissions.Role'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('auth', ['ParamRole'])

        # Adding M2M table for field param_set on 'ParamRole'
        db.create_table('auth_paramrole_param_set', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('paramrole', models.ForeignKey(orm['auth.paramrole'], null=False)),
            ('param', models.ForeignKey(orm['auth.param'], null=False))
        ))
        db.create_unique('auth_paramrole_param_set', ['paramrole_id', 'param_id'])

        # Adding model 'PrincipalParamRoleRelation'
        db.create_table('auth_principalparamrolerelation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.Group'], null=True, blank=True)),
            ('role', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.ParamRole'])),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], null=True, blank=True)),
            ('content_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('auth', ['PrincipalParamRoleRelation'])

        # Adding model 'GlobalPermission'
        db.create_table('auth_globalpermission', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('permission', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['permissions.Permission'])),
            ('role', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['permissions.Role'])),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
        ))
        db.send_create_signal('auth', ['GlobalPermission'])

        # Adding unique constraint on 'GlobalPermission', fields ['permission', 'role', 'content_type']
        db.create_unique('auth_globalpermission', ['permission_id', 'role_id', 'content_type_id'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'GlobalPermission', fields ['permission', 'role', 'content_type']
        db.delete_unique('auth_globalpermission', ['permission_id', 'role_id', 'content_type_id'])

        # Removing unique constraint on 'Permission', fields ['content_type', 'codename']
        db.delete_unique('auth_permission', ['content_type_id', 'codename'])

        # Deleting model 'Permission'
        db.delete_table('auth_permission')

        # Deleting model 'Group'
        db.delete_table('auth_group')

        # Removing M2M table for field permissions on 'Group'
        db.delete_table('auth_group_permissions')

        # Deleting model 'User'
        db.delete_table('auth_user')

        # Removing M2M table for field groups on 'User'
        db.delete_table('auth_user_groups')

        # Removing M2M table for field user_permissions on 'User'
        db.delete_table('auth_user_user_permissions')

        # Deleting model 'Message'
        db.delete_table('auth_message')

        # Deleting model 'Param'
        db.delete_table('auth_param')

        # Deleting model 'ParamRole'
        db.delete_table('auth_paramrole')

        # Removing M2M table for field param_set on 'ParamRole'
        db.delete_table('auth_paramrole_param_set')

        # Deleting model 'PrincipalParamRoleRelation'
        db.delete_table('auth_principalparamrolerelation')

        # Deleting model 'GlobalPermission'
        db.delete_table('auth_globalpermission')


    models = {
        'auth.globalpermission': {
            'Meta': {'unique_together': "(('permission', 'role', 'content_type'),)", 'object_name': 'GlobalPermission'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'permission': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['permissions.Permission']"}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['permissions.Role']"})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.message': {
            'Meta': {'object_name': 'Message'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_message_set'", 'to': "orm['auth.User']"})
        },
        'auth.param': {
            'Meta': {'object_name': 'Param'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'auth.paramrole': {
            'Meta': {'ordering': "('name',)", 'object_name': 'ParamRole', '_ormbases': ['permissions.Role']},
            'param_set': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Param']", 'symmetrical': 'False'}),
            'role': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['permissions.Role']", 'unique': 'True', 'primary_key': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.principalparamrolerelation': {
            'Meta': {'object_name': 'PrincipalParamRoleRelation'},
            'content_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.Group']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.ParamRole']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
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
        'permissions.role': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Role'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        }
    }

    complete_apps = ['auth']
