# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-06-26 02:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parks', '0004_auto_20190626_0200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='park',
            name='operating_hours',
            field=models.TextField(blank=True),
        ),
    ]
