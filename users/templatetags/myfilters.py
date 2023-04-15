from django import template
from sorl.thumbnail import get_thumbnail

register = template.Library()


@register.filter
def thumbnail_url(image_url, size):
    """
    Generates a URL for a thumbnail of the given image.

    :param image_url: the URL of the original image
    :param size: the size of the thumbnail in the format "WxH", e.g. "100x100"
    :return: the URL of the thumbnail
    """
    return get_thumbnail(image_url, size).url
