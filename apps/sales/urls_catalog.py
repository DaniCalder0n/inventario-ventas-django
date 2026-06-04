from django.urls import path
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from apps.inventory.models import Product, Category

def catalog(request):
    products = Product.objects.filter(is_active=True, stock__gt=0).select_related('category')
    q = request.GET.get('q', '')
    cat_slug = request.GET.get('category', '')
    if q:
        products = products.filter(Q(name__icontains=q) | Q(description__icontains=q))
    if cat_slug:
        products = products.filter(category__slug=cat_slug)
    paginator = Paginator(products, 12)
    page_obj = paginator.get_page(request.GET.get('page'))
    featured = Product.objects.filter(is_active=True, is_featured=True, stock__gt=0)[:4]
    categories = Category.objects.all()
    return render(request, 'sales/catalog.html', {'page_obj': page_obj, 'featured': featured, 'categories': categories, 'q': q, 'cat_slug': cat_slug})

urlpatterns = [path('', catalog, name='catalog'), path('catalog/', catalog)]
