from django.contrib import admin
from .models import Category, Product, InventoryMovement

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'stock', 'sale_price', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('name',)

@admin.register(InventoryMovement)
class MovementAdmin(admin.ModelAdmin):
    list_display = ('product', 'movement_type', 'quantity', 'user', 'created_at')
    readonly_fields = ('created_at',)
