# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2018-09-03 08:49
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0014_auto_20180903_0947'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='expiration_date',
            field=models.DateField(default=datetime.datetime(2018, 9, 3, 8, 49, 15, 924874, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
