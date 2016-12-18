from django.conf import settings
from django.utils.html import format_html, format_html_join

from wagtail.wagtailcore import hooks
from wagtail.wagtailcore.whitelist import attribute_rule, check_url, allow_without_attributes

# https://jossingram.wordpress.com/2014/07/24/add-some-blockquote-buttons-to-wagtail-cms-wysiwyg-editor/
# http://docs.wagtail.io/en/v1.8/reference/hooks.html


# Allow target attribute on anchor elements, and blockquote and code elements
@hooks.register('construct_whitelister_element_rules')
def whitelister_element_rules():
    return {
        'a': attribute_rule({'href': check_url, 'target': True}),
        'blockquote': attribute_rule({'class': True}),
        'code': attribute_rule({'class': True}),
    }


# Add custom JS to editor so we can add blockquotes and code elements
@hooks.register('insert_editor_js')
def editor_js():
    js_files = [
        '/js/hallo-custom-buttons.js',
    ]
    js_includes = format_html_join('\n', '<script src="{0}{1}"></script>',
        ((settings.STATIC_URL, filename) for filename in js_files)
    )

    return js_includes + format_html(
        """
        <script>
            registerHalloPlugin('codebutton');
            //registerHalloPlugin('blockquotebutton');
            //registerHalloPlugin('blockquotebuttonwithclass');
        </script>
        """
    )


# Add fontawesome to editor's CSS
@hooks.register('insert_editor_css')
def editor_css():
    return format_html('<link rel="stylesheet" href="' + settings.STATIC_URL + '/css/font-awesome.min.css">')
