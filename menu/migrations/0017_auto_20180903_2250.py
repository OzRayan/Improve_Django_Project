# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2018-09-03 21:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0016_auto_20180903_0957'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='expiration_date',
            field=models.DateField(blank=True, help_text='MM/DD/YYYY', null=True),
        ),
    ]
