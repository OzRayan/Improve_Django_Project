# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-03-06 17:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0010_auto_20190306_1816'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='name',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='item',
            name='name',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='menu',
            name='season',
            field=models.CharField(max_length=20),
        ),
    ]