# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2018-09-03 06:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0012_auto_20180903_0728'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='expiration_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]