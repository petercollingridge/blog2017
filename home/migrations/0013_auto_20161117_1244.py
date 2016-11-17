# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-17 12:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0030_index_on_pagerevision_created_at'),
        ('home', '0012_auto_20161117_1242'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeaturedContent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='FeaturedContentX',
            fields=[
                ('featuredcontent_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='home.FeaturedContent')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='featured_content', to='home.IndexPage')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
            bases=('home.featuredcontent', models.Model),
        ),
        migrations.AddField(
            model_name='featuredcontent',
            name='link_page',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wagtailcore.Page'),
        ),
    ]
