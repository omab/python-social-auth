# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import social.apps.django_app.default.fields
from django.conf import settings
import social.storage.django_orm


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Association',
            fields=[
                ('id', models.AutoField(
                    verbose_name='ID', serialize=False, auto_created=True,
                    primary_key=True)),
                ('server_url', models.CharField(max_length=255)),
                ('handle', models.CharField(max_length=255)),
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
                    primary_key=True)),
                ('server_url', models.CharField(max_length=255)),
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
                ('uid', models.CharField(max_length=255)),
                ('extra_data', social.apps.django_app.default.fields.JSONField(
                    default=b'{}')),
                ('user', models.ForeignKey(
                    related_name=b'social_auth', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'social_auth_usersocialauth',
            },
            bases=(models.Model, social.storage.django_orm.DjangoUserMixin),
        ),
        migrations.AlterUniqueTogether(
            name='usersocialauth',
            unique_together=set([('provider', 'uid')]),
        ),
        migrations.AlterUniqueTogether(
            name='code',
            unique_together=set([('email', 'code')]),
        ),
    ]
