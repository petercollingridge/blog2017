from django.utils.html import format_html, format_html_join

import django_comments

from wagtail.core import hooks
from wagtail.admin.rich_text.converters.html_to_contentstate import BlockElementHandler
from wagtail.admin.rich_text.converters.html_to_contentstate import InlineStyleElementHandler
import wagtail.admin.rich_text.editors.draftail.features as draftail_features

from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register


@hooks.register('register_rich_text_features')
def register_blockquote_feature(features):
    """
    Registering the `blockquote` feature, which uses the `blockquote` Draft.js block type,
    and is stored as HTML with a `<blockquote>` tag.
    """
    feature_name = 'blockquote'
    type_ = 'blockquote'
    tag = 'blockquote'

    control = {
        'type': type_,
        'label': '❝',
        'description': 'Blockquote',
        # Optionally, we can tell Draftail what element to use when displaying those blocks in the editor.
        'element': 'blockquote',
    }

    features.register_editor_plugin(
        'draftail', feature_name, draftail_features.BlockFeature(control)
    )

    features.register_converter_rule('contentstate', feature_name, {
        'from_database_format': {tag: BlockElementHandler(type_)},
        'to_database_format': {'block_map': {type_: tag}},
    })


class CommentAdmin(ModelAdmin):
    model = django_comments.models.Comment

    menu_label = 'Comments'
    menu_icon = 'list-ul'
    menu_order = 200
    add_to_settings_menu = False
    list_display = ('user_name', 'submit_date', 'show_page_link', 'comment')

    def show_page_link(self, obj):
        return format_html("<a href='{url}'>{name}</a>", url=obj.content_object.url, name=obj.content_object)

    show_page_link.short_description = "Page"


modeladmin_register(CommentAdmin)
