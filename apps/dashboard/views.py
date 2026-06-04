from django.shortcuts import render
from django.utils import timezone
from django.db.models import Sum, Count, Q, F
from datetime import timedelta
from apps.accounts.decorators import seller_required
from apps.inventory.models import Product, Category
from apps.sales.models import Order, OrderItem

@seller_required
def dashboard(request):
    today = timezone.now().date()
    month_start = today.replace(day=1)

    total_products = Product.objects.count()
    out_of_stock = Product.objects.filter(stock=0).count()
    low_stock = Product.objects.filter(stock__gt=0, stock__lte=F('min_stock')).count()

    sales_today = Order.objects.filter(created_at__date=today).aggregate(total=Sum('total'))['total'] or 0
    sales_month = Order.objects.filter(created_at__date__gte=month_start).aggregate(total=Sum('total'))['total'] or 0
    orders_today = Order.objects.filter(created_at__date=today).count()

    monthly_sales = []
    for i in range(5, -1, -1):
        d = today - timedelta(days=30 * i)
        month_s = d.replace(day=1)
        month_e = (month_s.replace(month=month_s.month % 12 + 1, day=1) - timedelta(days=1)) if month_s.month < 12 else month_s.replace(month=12, day=31)
        total = Order.objects.filter(created_at__date__gte=month_s, created_at__date__lte=month_e).aggregate(t=Sum('total'))['t'] or 0
        monthly_sales.append({'month': month_s.strftime('%b %Y'), 'total': float(total)})

    top_products = OrderItem.objects.values('product__name').annotate(
        total_sold=Sum('quantity'), revenue=Sum(F('quantity') * F('unit_price'))
    ).order_by('-total_sold')[:5]

    categories = Category.objects.annotate(product_count=Count('products')).values('name', 'product_count')

    context = {
        'total_products': total_products,
        'out_of_stock': out_of_stock,
        'low_stock': low_stock,
        'sales_today': sales_today,
        'sales_month': sales_month,
        'orders_today': orders_today,
        'monthly_sales': monthly_sales,
        'top_products': list(top_products),
        'categories': list(categories),
        'recent_orders': Order.objects.select_related('user').order_by('-created_at')[:8],
        'low_stock_products': Product.objects.filter(stock__lte=F('min_stock'), is_active=True).select_related('category')[:5],
    }
    return render(request, 'dashboard/dashboard.html', context)
