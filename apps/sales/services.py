from django.db import transaction
from .models import Cart, CartItem, Order, OrderItem
from apps.inventory.services import update_stock

def get_or_create_cart(user):
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart

def add_to_cart(user, product, quantity=1):
    cart = get_or_create_cart(user)
    if product.stock < quantity:
        raise ValueError(f'Stock insuficiente. Solo quedan {product.stock} unidades.')
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        new_qty = item.quantity + quantity
        if product.stock < new_qty:
            raise ValueError(f'Stock insuficiente.')
        item.quantity = new_qty
    else:
        item.quantity = quantity
    item.save()
    return item

@transaction.atomic
def checkout(user, notes=''):
    cart = get_or_create_cart(user)
    if not cart.items.exists():
        raise ValueError('El carrito está vacío.')
    for item in cart.items.select_related('product').all():
        if item.product.stock < item.quantity:
            raise ValueError(f'Stock insuficiente para "{item.product.name}".')
    order = Order.objects.create(
        user=user, subtotal=cart.subtotal, tax=cart.tax, total=cart.total, notes=notes
    )
    for item in cart.items.select_related('product').all():
        OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity, unit_price=item.product.sale_price)
        update_stock(item.product, item.quantity, 'sale', user, f'Venta {order.invoice_number}')
    cart.items.all().delete()
    return order
