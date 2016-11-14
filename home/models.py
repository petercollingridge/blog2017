from __future__ import absolute_import, unicode_literals

from django.db import models

from modelcluster.fields import ParentalKey

from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel


class BlogSection(models.Model):
    title = models.CharField(max_length=255)
    body = RichTextField(blank=True)

    panels = [
        FieldPanel('title'),
        FieldPanel('body'),
    ]

    class Meta:
        abstract = True


class HomePageSection(Orderable, BlogSection):
    page = ParentalKey('HomePage', related_name='sections')


class HomePage(Page):
    introduction = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('introduction', classname="full"),
        InlinePanel('sections', label="Sections"),
    ]
