# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-20 18:13
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0032_contactpage_formfield'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='featuredcontent',
            name='link_page',
        ),
        migrations.RemoveField(
            model_name='featuredcontentset',
            name='featuredcontent_ptr',
        ),
        migrations.RemoveField(
            model_name='featuredcontentset',
            name='page',
        ),
        migrations.DeleteModel(
            name='FeaturedContent',
        ),
        migrations.DeleteModel(
            name='FeaturedContentSet',
        ),
    ]