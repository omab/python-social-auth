# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import social.apps.django_app.default.fields
from django.conf import settings
import social.storage.django_orm


class Migration(migrations.Migration):

    dependencies = [
        ('default', '0001_initial'),
    ]

    operations = [
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
        migrations.AlterUniqueTogether(
            name='code',
            unique_together=set([('email', 'code')]),
        ),
        migrations.AlterField(
            model_name='usersocialauth',
            name='user',
            field=models.ForeignKey(related_name='social_auth', to=settings.AUTH_USER_MODEL)
        ),
    ]
