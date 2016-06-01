# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import social.apps.django_app.default.fields


class Migration(migrations.Migration):

    dependencies = [
        ('default', '0003_alter_email_max_length'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersocialauth',
            name='extra_data',
            field=social.apps.django_app.default.fields.JSONField(default={}),
        ),
    ]
