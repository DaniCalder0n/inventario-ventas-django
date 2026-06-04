from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from apps.inventory.models import Product, Category
from .models import Cart, CartItem, Order
from .services import add_to_cart, checkout, get_or_create_cart
from apps.accounts.decorators import seller_required

@login_required
def cart_view(request):
    cart = get_or_create_cart(request.user)
    return render(request, 'sales/cart.html', {'cart': cart})

@login_required
def cart_add(request, pk):
    product = get_object_or_404(Product, pk=pk, is_active=True)
    try:
        add_to_cart(request.user, product)
        messages.success(request, f'"{product.name}" añadido al carrito.')
    except ValueError as e:
        messages.error(request, str(e))
    return redirect(request.META.get('HTTP_REFERER', 'catalog'))

@login_required
def cart_update(request, pk):
    item = get_object_or_404(CartItem, pk=pk, cart__user=request.user)
    quantity = int(request.POST.get('quantity', 1))
    if quantity <= 0:
        item.delete()
        messages.info(request, 'Producto eliminado del carrito.')
    elif quantity > item.product.stock:
        messages.error(request, f'Solo hay {item.product.stock} unidades disponibles.')
    else:
        item.quantity = quantity
        item.save()
    return redirect('cart')

@login_required
def cart_remove(request, pk):
    item = get_object_or_404(CartItem, pk=pk, cart__user=request.user)
    item.delete()
    messages.info(request, 'Producto eliminado.')
    return redirect('cart')

@login_required
def checkout_view(request):
    if request.method == 'POST':
        try:
            order = checkout(request.user, request.POST.get('notes', ''))
            messages.success(request, f'¡Pedido {order.invoice_number} creado exitosamente!')
            return redirect('order_detail', pk=order.pk)
        except ValueError as e:
            messages.error(request, str(e))
            return redirect('cart')
    return redirect('cart')

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'sales/order_list.html', {'orders': orders})

@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, 'sales/order_detail.html', {'order': order})

@seller_required
def all_orders(request):
    orders = Order.objects.select_related('user').all()
    paginator = Paginator(orders, 30)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'sales/all_orders.html', {'page_obj': page_obj})
