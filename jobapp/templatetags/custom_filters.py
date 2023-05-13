from django import template

register = template.Library()


@register.filter
def range_filter(value):
    return range(value)


@register.filter(name='int')
def convert_to_int(value):
    return int(value)
