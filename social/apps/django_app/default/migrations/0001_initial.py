# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models, migrations
import jsonfield

import social.storage.django_orm
from social.utils import setting_name

USER_MODEL = getattr(settings, setting_name('USER_MODEL'), None) or \
             getattr(settings, 'AUTH_USER_MODEL', None) or \
             'auth.User'
UID_LENGTH = getattr(settings, setting_name('UID_LENGTH'), 255)
NONCE_SERVER_URL_LENGTH = getattr(
    settings, setting_name('NONCE_SERVER_URL_LENGTH'), 255
)
ASSOCIATION_SERVER_URL_LENGTH = getattr(
    settings, setting_name('ASSOCIATION_SERVER_URL_LENGTH'), 255
)
ASSOCIATION_HANDLE_LENGTH = getattr(
    settings, setting_name('ASSOCIATION_HANDLE_LENGTH'), 255
)


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Association',
            fields=[
                ('id', models.AutoField(
                    verbose_name='ID', serialize=False, auto_created=True,
                    primary_key=True)),
                ('server_url',
                 models.CharField(max_length=ASSOCIATION_SERVER_URL_LENGTH)),
                ('handle',
                 models.CharField(max_length=ASSOCIATION_HANDLE_LENGTH)),
                ('secret', models.CharField(max_length=255)),
                ('issued', models.IntegerField()),
                ('lifetime', models.IntegerField()),
                ('assoc_type', models.CharField(max_length=64)),
            ],
            options={
                'db_table': 'social_auth_association',
            },
            bases=(
                models.Model, social.storage.django_orm.DjangoAssociationMixin
            ),
        ),
        migrations.CreateModel(
            name='Code',
            fields=[
                ('id', models.AutoField(
                    verbose_name='ID', serialize=False, auto_created=True,
                    primary_key=True)),
                ('email', models.EmailField(max_length=75)),
                ('code', models.CharField(max_length=32, db_index=True)),
                ('verified', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'social_auth_code',
            },
            bases=(models.Model, social.storage.django_orm.DjangoCodeMixin),
        ),
        migrations.CreateModel(
            name='Nonce',
            fields=[
                ('id', models.AutoField(
                    verbose_name='ID', serialize=False, auto_created=True,
                    primary_key=True
                )),
                ('server_url',
                 models.CharField(max_length=NONCE_SERVER_URL_LENGTH)),
                ('timestamp', models.IntegerField()),
                ('salt', models.CharField(max_length=65)),
            ],
            options={
                'db_table': 'social_auth_nonce',
            },
            bases=(models.Model, social.storage.django_orm.DjangoNonceMixin),
        ),
        migrations.CreateModel(
            name='UserSocialAuth',
            fields=[
                ('id', models.AutoField(
                    verbose_name='ID', serialize=False, auto_created=True,
                    primary_key=True)),
                ('provider', models.CharField(max_length=32)),
                ('uid', models.CharField(max_length=UID_LENGTH)),
                ('extra_data', jsonfield.JSONField(
                    default='{}')),
                ('user', models.ForeignKey(
                    related_name='social_auth', to=USER_MODEL)),
            ],
            options={
                'db_table': 'social_auth_usersocialauth',
            },
            bases=(models.Model, social.storage.django_orm.DjangoUserMixin),
        ),
        migrations.AlterUniqueTogether(
            name='usersocialauth',
            unique_together={('provider', 'uid')},
        ),
        migrations.AlterUniqueTogether(
            name='code',
            unique_together={('email', 'code')},
        ),
        migrations.AlterUniqueTogether(
            name='nonce',
            unique_together={('server_url', 'timestamp', 'salt')},
        ),
    ]
