from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages

PROTECTED_PATHS = {
    '/inventory/': ['admin', 'seller'],
    '/dashboard/': ['admin', 'seller'],
}

class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        if request.user.is_authenticated:
            for prefix, roles in PROTECTED_PATHS.items():
                if path.startswith(prefix):
                    if not hasattr(request.user, 'role') or request.user.role not in roles:
                        messages.error(request, 'No tienes permiso para acceder a esta sección.')
                        return redirect('catalog')
        return self.get_response(request)
