from django import template
from home.models import Icon

register = template.Library()


@register.inclusion_tag('home/tags/icons.html', takes_context=True)
def icon(context):
    return {
        'icons': Icon.objects.all(),
        'request': context['request']
    }
