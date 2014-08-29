# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration

from . import get_custom_user_model_for_migrations, custom_user_frozen_models


USER_MODEL = get_custom_user_model_for_migrations()


class Migration(SchemaMigration):
    def forwards(self, orm):
        # Adding model 'UserSocialAuth'
        db.create_table('social_auth_usersocialauth', (
            (u'id', self.gf('django.db.models.fields.AutoField')(
                primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(
                related_name='social_auth', to=orm[USER_MODEL])),
            ('provider', self.gf('django.db.models.fields.CharField')(
                max_length=32)),
            ('uid', self.gf('django.db.models.fields.CharField')(
                max_length=255)),
            ('extra_data', self.gf(
                'social.apps.django_app.default.fields.JSONField'
            )(default='{}')),
        ))
        db.send_create_signal(u'default', ['UserSocialAuth'])

        # Adding unique constraint on 'UserSocialAuth',
        # fields ['provider', 'uid']
        db.create_unique('social_auth_usersocialauth', ['provider', 'uid'])

        # Adding model 'Nonce'
        db.create_table('social_auth_nonce', (
            (u'id', self.gf('django.db.models.fields.AutoField')(
                primary_key=True)),
            ('server_url', self.gf('django.db.models.fields.CharField')(
                max_length=255)),
            ('timestamp', self.gf('django.db.models.fields.IntegerField')()),
            ('salt', self.gf('django.db.models.fields.CharField')(
                max_length=65)),
        ))
        db.send_create_signal(u'default', ['Nonce'])

        # Adding model 'Association'
        db.create_table('social_auth_association', (
            (u'id', self.gf('django.db.models.fields.AutoField')(
                primary_key=True)),
            ('server_url', self.gf('django.db.models.fields.CharField')(
                max_length=255)),
            ('handle', self.gf('django.db.models.fields.CharField')(
                max_length=255)),
            ('secret', self.gf('django.db.models.fields.CharField')(
                max_length=255)),
            ('issued', self.gf('django.db.models.fields.IntegerField')()),
            ('lifetime', self.gf('django.db.models.fields.IntegerField')()),
            ('assoc_type', self.gf('django.db.models.fields.CharField')(
                max_length=64)),
        ))
        db.send_create_signal(u'default', ['Association'])

        # Adding model 'Code'
        db.create_table('social_auth_code', (
            (u'id', self.gf('django.db.models.fields.AutoField')(
                primary_key=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(
                max_length=75)),
            ('code', self.gf('django.db.models.fields.CharField')(
                max_length=32,
                db_index=True)),
            ('verified', self.gf('django.db.models.fields.BooleanField')(
                default=False)),
        ))
        db.send_create_signal(u'default', ['Code'])

        # Adding unique constraint on 'Code', fields ['email', 'code']
        db.create_unique('social_auth_code', ['email', 'code'])

    def backwards(self, orm):
        # Removing unique constraint on 'Code', fields ['email', 'code']
        db.delete_unique('social_auth_code', ['email', 'code'])

        # Removing unique constraint on 'UserSocialAuth',
        # fields ['provider', 'uid']
        db.delete_unique('social_auth_usersocialauth', ['provider', 'uid'])

        # Deleting model 'UserSocialAuth'
        db.delete_table('social_auth_usersocialauth')

        # Deleting model 'Nonce'
        db.delete_table('social_auth_nonce')

        # Deleting model 'Association'
        db.delete_table('social_auth_association')

        # Deleting model 'Code'
        db.delete_table('social_auth_code')

    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [],
                    {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [],
                     {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField',
                            [], {'to': u"orm['auth.Permission']",
                                 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {
                'ordering':
                    "(u'content_type__app_label', "
                    "u'content_type__model', u'codename')",
                'unique_together': "((u'content_type', u'codename'),)",
                'object_name': 'Permission'
            },
            'codename': ('django.db.models.fields.CharField', [],
                         {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [],
                             {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [],
                    {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [],
                     {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [],
                            {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [],
                      {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [],
                           {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [],
                       {'symmetrical': 'False', 'related_name': "u'user_set'",
                        'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [],
                    {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [],
                          {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [],
                         {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [],
                             {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [],
                           {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [],
                          {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [],
                         {'max_length': '128'}),
            'user_permissions': (
                'django.db.models.fields.related.ManyToManyField', [],
                {'symmetrical': 'False', 'related_name': "u'user_set'",
                 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [],
                         {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)",
                     'unique_together': "(('app_label', 'model'),)",
                     'object_name': 'ContentType',
                     'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [],
                          {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [],
                    {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [],
                      {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [],
                     {'max_length': '100'})
        },
        u'default.association': {
            'Meta': {'object_name': 'Association',
                     'db_table': "'social_auth_association'"},
            'assoc_type': ('django.db.models.fields.CharField', [],
                           {'max_length': '64'}),
            'handle': ('django.db.models.fields.CharField', [],
                       {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [],
                    {'primary_key': 'True'}),
            'issued': ('django.db.models.fields.IntegerField', [], {}),
            'lifetime': ('django.db.models.fields.IntegerField', [], {}),
            'secret': ('django.db.models.fields.CharField', [],
                       {'max_length': '255'}),
            'server_url': ('django.db.models.fields.CharField', [],
                           {'max_length': '255'})
        },
        u'default.code': {
            'Meta': {'unique_together': "(('email', 'code'),)",
                     'object_name': 'Code', 'db_table': "'social_auth_code'"},
            'code': ('django.db.models.fields.CharField', [],
                     {'max_length': '32', 'db_index': 'True'}),
            'email': ('django.db.models.fields.EmailField', [],
                      {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [],
                    {'primary_key': 'True'}),
            'verified': ('django.db.models.fields.BooleanField', [],
                         {'default': 'False'})
        },
        u'default.nonce': {
            'Meta': {'object_name': 'Nonce',
                     'db_table': "'social_auth_nonce'"},
            u'id': ('django.db.models.fields.AutoField', [],
                    {'primary_key': 'True'}),
            'salt': ('django.db.models.fields.CharField', [],
                     {'max_length': '65'}),
            'server_url': ('django.db.models.fields.CharField', [],
                           {'max_length': '255'}),
            'timestamp': ('django.db.models.fields.IntegerField', [], {})
        },
        u'default.usersocialauth': {
            'Meta': {'unique_together': "(('provider', 'uid'),)",
                     'object_name': 'UserSocialAuth',
                     'db_table': "'social_auth_usersocialauth'"},
            'extra_data': ('social.apps.django_app.default.fields.JSONField',
                           [], {'default': "'{}'"}),
            u'id': ('django.db.models.fields.AutoField', [],
                    {'primary_key': 'True'}),
            'provider': ('django.db.models.fields.CharField', [],
                         {'max_length': '32'}),
            'uid': ('django.db.models.fields.CharField', [],
                    {'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [],
                     {'related_name': "'social_auth'",
                      'to': u"orm['auth.User']"})
        }
    }
    models.update(custom_user_frozen_models(USER_MODEL))

    complete_apps = ['default']
