from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, F
from .models import Product, Category, InventoryMovement
from .forms import ProductForm, StockUpdateForm, ProductSearchForm
from .services import update_stock
from apps.accounts.decorators import admin_required, seller_required

@seller_required
def inventory_list(request):
    form = ProductSearchForm(request.GET)
    products = Product.objects.select_related('category').all()
    if form.is_valid():
        q = form.cleaned_data.get('q')
        category = form.cleaned_data.get('category')
        status = form.cleaned_data.get('status')
        if q:
            products = products.filter(Q(name__icontains=q) | Q(description__icontains=q))
        if category:
            products = products.filter(category=category)
        if status == 'low':
            products = products.filter(stock__gt=0, stock__lte=F('min_stock'))
        elif status == 'out':
            products = products.filter(stock=0)
        elif status == 'active':
            products = products.filter(stock__gt=F('min_stock'), is_active=True)
    paginator = Paginator(products, 20)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'inventory/inventory_list.html', {'page_obj': page_obj, 'form': form})

@admin_required
def product_create(request):
    form = ProductForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        product = form.save()
        InventoryMovement.objects.create(
            product=product, user=request.user, movement_type='in',
            quantity=product.stock, previous_stock=0, new_stock=product.stock, notes='Creación inicial'
        )
        messages.success(request, f'Producto "{product.name}" creado.')
        return redirect('inventory_list')
    return render(request, 'inventory/product_form.html', {'form': form, 'title': 'Nuevo Producto'})

@admin_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = ProductForm(request.POST or None, request.FILES or None, instance=product)
    if form.is_valid():
        form.save()
        messages.success(request, 'Producto actualizado.')
        return redirect('inventory_list')
    return render(request, 'inventory/product_form.html', {'form': form, 'title': 'Editar Producto', 'product': product})

@admin_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Producto eliminado.')
        return redirect('inventory_list')
    return render(request, 'inventory/product_confirm_delete.html', {'product': product})

@seller_required
def stock_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = StockUpdateForm(request.POST or None)
    if form.is_valid():
        try:
            update_stock(product, form.cleaned_data['quantity'], form.cleaned_data['movement_type'], request.user, form.cleaned_data.get('notes', ''))
            messages.success(request, 'Stock actualizado.')
            return redirect('inventory_list')
        except ValueError as e:
            messages.error(request, str(e))
    return render(request, 'inventory/stock_update.html', {'form': form, 'product': product})

@seller_required
def movement_history(request):
    movements = InventoryMovement.objects.select_related('product', 'user').all()
    paginator = Paginator(movements, 30)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'inventory/movement_history.html', {'page_obj': page_obj})
