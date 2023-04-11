from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.si_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            return view_func(request, *args, **kwargs)
        
    return wrapper_func

'''def allowed_user(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorized to view this page')
        return wrapper_func
    return decorator
'''

def allowed_user(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group=None
            if request.user.groups.exists():
                group=request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorised to view this page')
            
        return wrapper_func
    return decorator


def staff_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group=None
        
        if request.user.groups.exists():
            group=request.user.groups.all()[0].name

        if group=='nanny' or 'employer':
            return redirect('home')
        
        if group=='admin':
            return view_func(request, *args, **kwargs)
    return wrapper_function