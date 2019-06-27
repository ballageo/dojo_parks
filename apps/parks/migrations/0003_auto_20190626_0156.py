# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-06-26 01:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parks', '0002_auto_20190626_0138'),
    ]

    operations = [
        migrations.AddField(
            model_name='park',
            name='review',
            field=models.TextField(default='no reviews'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='park',
            name='rating',
            field=models.IntegerField(default=None),
        ),
    ]