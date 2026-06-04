from django.contrib import admin
from .models import Order, OrderItem, Cart, CartItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'user', 'total', 'status', 'created_at')
    inlines = [OrderItemInline]
    readonly_fields = ('invoice_number',)
