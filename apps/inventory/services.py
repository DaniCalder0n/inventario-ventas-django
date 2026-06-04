from .models import Product, InventoryMovement

def update_stock(product, quantity, movement_type, user, notes=''):
    """Actualiza el stock y registra el movimiento."""
    previous_stock = product.stock
    if movement_type == 'in':
        product.stock += quantity
    elif movement_type in ('out', 'sale'):
        if product.stock < quantity:
            raise ValueError(f'Stock insuficiente. Disponible: {product.stock}')
        product.stock -= quantity
    elif movement_type == 'adjustment':
        product.stock = quantity
    product.save()
    InventoryMovement.objects.create(
        product=product, user=user, movement_type=movement_type,
        quantity=quantity, previous_stock=previous_stock, new_stock=product.stock, notes=notes
    )
    return product

def get_low_stock_products():
    return Product.objects.filter(stock__lte=models.F('min_stock'), is_active=True)

def get_alerts():
    from django.db.models import F
    low_stock = Product.objects.filter(stock__gt=0, stock__lte=F('min_stock'), is_active=True)
    out_of_stock = Product.objects.filter(stock=0, is_active=True)
    return {'low_stock': low_stock, 'out_of_stock': out_of_stock}
