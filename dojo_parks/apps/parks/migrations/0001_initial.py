# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-06-27 17:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Park',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('review', models.TextField()),
                ('rating', models.DecimalField(decimal_places=1, max_digits=2)),
                ('longitude', models.DecimalField(decimal_places=4, max_digits=8)),
                ('latitude', models.DecimalField(decimal_places=4, max_digits=8)),
                ('operating_hours', models.TextField(blank=True)),
                ('website', models.CharField(default='Sorry, no website found', max_length=255)),
                ('phone_number', models.CharField(default='Sorry, no phone number found', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parks_created', to='login.User')),
            ],
        ),
    ]
