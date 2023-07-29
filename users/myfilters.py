from django import template
from sorl.thumbnail import get_thumbnail

register = template.Library()


@register.filter
def thumbnail_url(image_url, size):
    """
    Generates a URL for a thumbnail of the given image.

    """
    return get_thumbnail(image_url, size).url
