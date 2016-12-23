# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-22 19:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0037_auto_20161222_1915'),
    ]

    operations = [
        migrations.CreateModel(
            name='PageWithSiblings',
            fields=[
                ('genericpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='home.GenericPage')),
            ],
            options={
                'abstract': False,
            },
            bases=('home.genericpage',),
        ),
    ]
