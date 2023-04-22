from django import template

register = template.Library()


@register.filter(name='has_group')
def has_group(user, group_name):
    """
    Returns True if the user belongs to a given group.
    Usage: {{ user|has_group:"employer" }}
    """
    return user.groups.filter(name=group_name).exists()
