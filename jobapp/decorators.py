from django.contrib.auth.decorators import user_passes_test


def is_nanny(user):
    return user.groups.filter(name='nanny').exists()


def is_employer(user):
    return user.groups.filter(name='employer').exists()
