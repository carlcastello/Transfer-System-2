# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-18 03:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('TransferSystem', '0002_auto_20170511_0232'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='log',
            name='date',
        ),
        migrations.AddField(
            model_name='transfer',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='date-time transfered'),
            preserve_default=False,
        ),
    ]