from django import template
from hurry.filesize import size


register = template.Library()


@register.filter
def convert(value):
    return size(value)