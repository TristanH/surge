# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-27 11:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20160227_0908'),
    ]

    operations = [
        migrations.AddField(
            model_name='restuarant',
            name='name',
            field=models.CharField(default=None, max_length=255),
            preserve_default=False,
        ),
    ]
