from __future__ import absolute_import, unicode_literals

from django.db import models

from modelcluster.fields import ParentalKey

from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField, StreamField

from wagtail.wagtailadmin.edit_handlers import FieldPanel, FieldRowPanel, StreamFieldPanel, InlinePanel, PageChooserPanel, MultiFieldPanel

from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

from wagtail.wagtailforms.models import AbstractEmailForm, AbstractFormField
from wagtail.wagtailforms.edit_handlers import FormSubmissionsPanel


# A section of content, such as Tutorials to show on the home page
class HomePageSection(models.Model):
    title = models.CharField(max_length=255)
    link_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        related_name='+'
    )
    body = RichTextField(blank=True)

    panels = [
        FieldPanel('title'),
        PageChooserPanel('link_page'),
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

    # Return sections to show on front page
    def get_sections(self):
        return IndexPage.objects.filter(path__startswith=self.path).order_by('path')

    # Get a list of child pages which will be the main sections of the site
    def get_context(self, request):
        context = super(HomePage, self).get_context(request)
        # Add extra variables and return the updated context
        context['children'] = IndexPage.objects.child_of(self).live()
        return context


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


# GenericPage uses a Streamfield with a raw HTML block so is relatively flexible
# Used for all leave nodes (tools, tutorial pages, blog posts) other than special pages
class GenericPage(Page):
    date = models.DateField("Post date")
    show_siblings = models.BooleanField()

    main_image = models.ForeignKey(
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
        ('code', CodeBlock()),
        ('two_columns', TwoColumnBlock()),
    ])

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('show_siblings'),
        InlinePanel('css_links', label="CSS links"),
        InlinePanel('js_links', label="JS links"),
        ImageChooserPanel('main_image'),
        StreamFieldPanel('body'),
    ]

    def get_context(self, request):
        context = super(GenericPage, self).get_context(request)
        # Add extra variables and return the updated context
        #context['children'] = IndexPage.objects.live().descendant_of(self)
        context["previous_page"] = self.get_prev_siblings().live().first()
        context["next_page"] = self.get_next_siblings().live().first()
        return context


# A page containing a list of child pages.
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
        # Add extra variables and return the updated context
        #context['children'] = IndexPage.objects.live().descendant_of(self)
        context['children'] = GenericPage.objects.child_of(self).live()
        context['index_children'] = IndexPage.objects.child_of(self).live()
        return context


# An index page for a section with links to the child pages
class SectionPage(Page):
    introduction = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('introduction', classname="full"),
    ]

    def get_context(self, request):
        context = super(SectionPage, self).get_context(request)

        # Add extra variables and return the updated context
        context['children'] = GenericPage.objects.child_of(self).live()
        context['index_children'] = IndexPage.objects.child_of(self).live()
        return context


# Page for prototyping the homepage
class HomePageTest(Page):
    pass
