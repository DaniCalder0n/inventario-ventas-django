def cart_count(request):
    if request.user.is_authenticated and hasattr(request.user, 'role') and request.user.role == 'client':
        try:
            return {'cart_count': request.user.cart.total_items}
        except Exception:
            pass
    return {'cart_count': 0}
