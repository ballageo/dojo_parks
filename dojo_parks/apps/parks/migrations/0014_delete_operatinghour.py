# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-06-27 17:35
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parks', '0013_auto_20190627_1535'),
    ]

    operations = [
        migrations.DeleteModel(
            name='OperatingHour',
        ),
    ]
