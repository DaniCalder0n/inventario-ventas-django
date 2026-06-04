from django.db.models import F
from .models import Product

def low_stock_alerts(request):
    if request.user.is_authenticated and hasattr(request.user, 'role') and request.user.role in ('admin', 'seller'):
        count = Product.objects.filter(stock__lte=F('min_stock'), is_active=True).count()
        return {'low_stock_alert_count': count}
    return {'low_stock_alert_count': 0}
