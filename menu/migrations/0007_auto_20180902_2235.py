# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2018-09-02 21:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0006_auto_20180901_1822'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='expiration_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]