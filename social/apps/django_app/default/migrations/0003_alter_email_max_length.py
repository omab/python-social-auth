# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models, migrations

from social.utils import setting_name

EMAIL_LENGTH = getattr(settings, setting_name('EMAIL_LENGTH'), 254)


class Migration(migrations.Migration):
    dependencies = [
        ('default', '0002_add_related_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='code',
            name='email',
            field=models.EmailField(max_length=EMAIL_LENGTH),
        ),
    ]
