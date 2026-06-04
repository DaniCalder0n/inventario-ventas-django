from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def role_required(*roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            if request.user.role not in roles:
                messages.error(request, 'Acceso denegado.')
                return redirect('catalog')
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

admin_required = role_required('admin')
seller_required = role_required('admin', 'seller')
