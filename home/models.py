from __future__ import absolute_import, unicode_literals

from django.db import models

from modelcluster.fields import ParentalKey

from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel, InlinePanel
from wagtail.wagtailimages.blocks import ImageChooserBlock


# A section of content, such as Tutorials to show on the home page
class HomePageSection(models.Model):
    title = models.CharField(max_length=255)
    body = RichTextField(blank=True)

    panels = [
        FieldPanel('title'),
        FieldPanel('body'),
    ]

    class Meta:
        abstract = True


# Sections for the home page collected together in an orderable way
class HomePageSections(Orderable, HomePageSection):
    page = ParentalKey('HomePage', related_name='sections')


class HomePage(Page):
    introduction = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('introduction', classname="full"),
        InlinePanel('sections', label="Sections"),
    ]


# A relative link path (used for CSS and JS)
class LinkFragment(models.Model):
    path = models.CharField(max_length=255, help_text="Relative URL")
    panels = [FieldPanel('path')]

    class Meta:
        abstract = True


class CSSLinkFragments(Orderable, LinkFragment):
    page = ParentalKey('GenericPage', related_name='css_links')


class JSLinkFragments(Orderable, LinkFragment):
    page = ParentalKey('GenericPage', related_name='js_links')


# A generic page which uses a Stream field with a raw HTML block so is relatively flexible
class GenericPage(Page):
    date = models.DateField("Post date")

    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('html', blocks.RawHTMLBlock()),
        ('image', ImageChooserBlock()),
    ])

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        InlinePanel('css_links', label="CSS links"),
        InlinePanel('js_links', label="JS links"),
        StreamFieldPanel('body'),
    ]
