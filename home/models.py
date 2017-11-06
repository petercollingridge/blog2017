from __future__ import absolute_import, unicode_literals

from itertools import chain

from django.db import models
from django.shortcuts import render

from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager

from taggit.models import TaggedItemBase
from taggit.models import Tag

from fluent_comments.moderation import moderate_model

from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField, StreamField

from wagtail.wagtailsearch import index

from wagtail.wagtailadmin.edit_handlers import FieldPanel, FieldRowPanel, StreamFieldPanel, InlinePanel, PageChooserPanel, MultiFieldPanel

from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

from wagtail.wagtailforms.models import AbstractEmailForm, AbstractFormField
from wagtail.wagtailforms.edit_handlers import FormSubmissionsPanel


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


class CodeBlock(blocks.StructBlock):
    code = blocks.TextBlock(required=True)
    language = blocks.CharBlock(required=False)
    line_number = blocks.IntegerBlock(required=False)

    class Meta:
        icon = 'code'
        label = 'Code'
        template = 'home/blocks/code_block.html'


# https://jossingram.wordpress.com/2015/07/30/some-wagtail-v1-streamfield-examples/
class TwoColumnBlock(blocks.StructBlock):
    left_column = blocks.StreamBlock([
        ('paragraph', blocks.RichTextBlock()),
        ('html', blocks.RawHTMLBlock()),
        ('image', ImageChooserBlock()),
        ('code', CodeBlock()),
    ], icon='arrow-left', label='Left column content')

    right_column = blocks.StreamBlock([
        ('paragraph', blocks.RichTextBlock()),
        ('html', blocks.RawHTMLBlock()),
        ('image', ImageChooserBlock()),
        ('code', CodeBlock()),
    ], icon='arrow-right', label='Right column content')

    class Meta:
        icon = 'placeholder'
        label = 'Two Columns'
        template = 'home/blocks/two_column_block.html'


class GenericPageTag(TaggedItemBase):
    content_object = ParentalKey('GenericPage', related_name='tagged_items')


class GenericPage(Page):
    """
    GenericPage uses a Streamfield with a raw HTML block so is flexible.
    Used for leaf nodes where we don't want to show links to siblings,
    such as tool pages and standalone articles.
    """

    date = models.DateField("Post date", blank=True)
    short_description = RichTextField(blank=True)
    github_link = models.URLField("Github link", blank=True)
    tags = ClusterTaggableManager(through=GenericPageTag, blank=True)

    featured_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('html', blocks.RawHTMLBlock()),
        ('image', ImageChooserBlock()),
        ('code_block', CodeBlock()),
        ('two_columns', TwoColumnBlock()),
    ])

    # Inherit search_fields from Page and add more
    search_fields = Page.search_fields + [
        index.SearchField('short_description', boost="1.5"),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        MultiFieldPanel(
            [
                FieldPanel('github_link'),
                InlinePanel('css_links', label="CSS links"),
                InlinePanel('js_links', label="JS links"),
            ],
            heading="Additional resources",
            classname="collapsible collapsed"
        ),
        MultiFieldPanel(
            [
                ImageChooserPanel('featured_image'),
                FieldPanel('short_description'),
            ],
            heading="Featured content information",
            classname="collapsible collapsed"
        ),
        StreamFieldPanel('body'),
    ]

    promote_panels = Page.promote_panels + [FieldPanel('tags')]


# A GenericPage with links to previous and next pages
class PageWithSiblings(GenericPage):
    def get_context(self, request):
        context = super(GenericPage, self).get_context(request)
        context["previous_page"] = self.get_prev_siblings().live().first()
        context["next_page"] = self.get_next_siblings().live().first()
        return context


# Generic page, but showing list of child pages
# Used as the first page for tutorials and articles
class IntroductionPage(GenericPage):
    def get_context(self, request):
        context = super(IntroductionPage, self).get_context(request)
        context['children'] = GenericPage.objects.child_of(self).live()
        context['introduction'] = context['children'].first()
        return context


# A page containing links to child pages.
class IndexPage(Page):
    introduction = RichTextField(blank=True)
    short_description = RichTextField(blank=True)

    featured_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        FieldPanel('introduction', classname="full"),
        MultiFieldPanel(
            [
                ImageChooserPanel('featured_image'),
                FieldPanel('short_description'),
            ],
            heading="Featured content information",
            classname="collapsible collapsed"
        ),
    ]

    def get_context(self, request):
        context = super(IndexPage, self).get_context(request)

        # Get children with different model types
        generic_children = GenericPage.objects.child_of(self).live()
        index_children = IndexPage.objects.child_of(self).live()

        # Combine children of different types
        all_children = list(chain(generic_children, index_children))

        # Split into those with short descriptions
        featured = []
        not_featured = []

        for child in all_children:
            if child.short_description:
                featured.append(child)
            else:
                not_featured.append(child)

        #context['children'] = sorted(not_featured, key=attrgetter('date'))
        #context['featured'] = sorted(featured, key=attrgetter('date'))
        context['children'] = not_featured
        context['featured'] = featured

        return context


class HomePage(Page):
    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('html', blocks.RawHTMLBlock()),
        ('image', ImageChooserBlock()),
        ('featured_pages', blocks.ListBlock(blocks.PageChooserBlock(label="featured_page")))
    ])

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]


# SVG icon from font-awesome or elsewhere
class IconBlock(blocks.StructBlock):
    name = blocks.CharBlock(max_length=255, required=True)
    font_awesome_class = blocks.CharBlock(max_length=255, required=False)
    svg = blocks.TextBlock(required=False)
    url = blocks.URLBlock(required=False)

    class Meta:
        icon = 'list-ul'
        label = 'Icon'
        template = 'home/blocks/icon_block.html'


class AboutPage(Page):
    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('icon_block', IconBlock()),
    ])

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]


class FormField(AbstractFormField):
    page = ParentalKey('ContactPage', related_name='form_fields')


class ContactPage(AbstractEmailForm):
    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)

    content_panels = AbstractEmailForm.content_panels + [
        FormSubmissionsPanel(),
        FieldPanel('intro', classname="full"),
        InlinePanel('form_fields', label="Form fields"),
        FieldPanel('thank_you_text', classname="full"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject')
        ], "Email")
    ]


class TagPage(Page):
    def serve(self, request):
        # Filter by tag
        tag = request.GET.get('tag')
        data = {}

        if tag:
            data['tag'] = tag
            data['pages'] = GenericPage.objects.live().filter(tags__name=tag)
        else:
            data['tags'] = Tag.objects.all

        return render(request, self.template, data)


moderate_model(
    GenericPage,
    publication_date_field='date'
)
