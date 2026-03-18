import markdown as md
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def markdown(value):
    """Render a markdown string as safe HTML."""
    return mark_safe(md.markdown(value, extensions=['extra', 'codehilite', 'toc']))
