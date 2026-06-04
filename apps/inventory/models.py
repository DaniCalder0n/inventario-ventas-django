from django.db import models
from django.utils import timezone
from datetime import timedelta

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['name']

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    stock = models.IntegerField(default=0)
    min_stock = models.IntegerField(default=5, help_text='Alerta cuando el stock baje de este valor')
    expiry_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    cost_price = models.DecimalField(max_digits=12, decimal_places=2)
    sale_price = models.DecimalField(max_digits=12, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['name']
        indexes = [
            models.Index(fields=['category', 'is_active']),
            models.Index(fields=['stock', 'min_stock']),
        ]

    @property
    def profit_margin(self):
        if self.cost_price and self.cost_price > 0:
            return round(((self.sale_price - self.cost_price) / self.cost_price) * 100, 2)
        return 0

    @property
    def is_low_stock(self):
        return self.stock <= self.min_stock and self.stock > 0

    @property
    def is_out_of_stock(self):
        return self.stock == 0

    @property
    def is_expiring_soon(self):
        if self.expiry_date:
            return self.expiry_date <= (timezone.now().date() + timedelta(days=30))
        return False

    @property
    def status_display(self):
        if self.is_out_of_stock:
            return ('Agotado', 'danger')
        if self.is_low_stock:
            return ('Stock bajo', 'warning')
        return ('Activo', 'success')

    def __str__(self):
        return self.name

class InventoryMovement(models.Model):
    MOVEMENT_TYPES = [
        ('in', 'Entrada'),
        ('out', 'Salida'),
        ('sale', 'Venta'),
        ('adjustment', 'Ajuste'),
        ('return', 'Devolución'),
    ]
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='movements')
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.SET_NULL, null=True)
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPES)
    quantity = models.IntegerField()
    previous_stock = models.IntegerField()
    new_stock = models.IntegerField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Movimiento de inventario'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_movement_type_display()} - {self.product.name} ({self.quantity})"
