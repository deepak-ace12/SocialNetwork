# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-13 06:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_friend_current_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post',
            field=models.CharField(max_length=160),
        ),
    ]
