"""
Script de datos de prueba.
Ejecutar: python manage.py shell < scripts/seed_data.py
"""
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.inventory.models import Category, Product
from django.utils.text import slugify

User = get_user_model()

# Crear superusuario admin
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@invstock.co', 'Admin1234!', role='admin', first_name='Admin', last_name='Sistema')
    print("✓ Admin creado: admin / Admin1234!")

# Crear vendedor de prueba
if not User.objects.filter(username='vendedor1').exists():
    User.objects.create_user('vendedor1', 'vendedor@invstock.co', 'Vendedor1234!', role='seller', first_name='Carlos', last_name='Martínez')
    print("✓ Vendedor creado: vendedor1 / Vendedor1234!")

# Crear cliente de prueba
if not User.objects.filter(username='cliente1').exists():
    User.objects.create_user('cliente1', 'cliente@invstock.co', 'Cliente1234!', role='client', first_name='María', last_name='González')
    print("✓ Cliente creado: cliente1 / Cliente1234!")

# Categorías
cats = ['Electrónica', 'Alimentos', 'Bebidas', 'Papelería', 'Aseo', 'Repuestos']
cat_objs = {}
for name in cats:
    c, _ = Category.objects.get_or_create(name=name, defaults={'slug': slugify(name), 'description': f'Productos de {name}'})
    cat_objs[name] = c

# Productos de ejemplo
products = [
    ('Portátil HP 15', 'Electronica', 1500000, 1800000, 10, 2),
    ('Mouse Inalámbrico', 'Electrónica', 25000, 45000, 50, 10),
    ('Teclado Mecánico', 'Electrónica', 80000, 130000, 30, 5),
    ('Arroz Diana 500g', 'Alimentos', 1800, 2500, 200, 30),
    ('Aceite Vegetal 1L', 'Alimentos', 8000, 11000, 150, 20),
    ('Coca-Cola 1.5L', 'Bebidas', 3500, 5500, 100, 15),
    ('Agua Cristal 500ml', 'Bebidas', 800, 1500, 300, 50),
    ('Resma Papel A4', 'Papelería', 12000, 18000, 80, 15),
    ('Bolígrafos (x10)', 'Papelería', 5000, 9000, 60, 10),
    ('Jabón Líquido 500ml', 'Aseo', 7000, 12000, 90, 20),
]

for name, cat_name, cost, price, stock, min_stock in products:
    cat_key = cat_name if cat_name in cat_objs else 'Electrónica'
    if cat_key == 'Electronica':
        cat_key = 'Electrónica'
    Product.objects.get_or_create(
        name=name,
        defaults={'category': cat_objs.get(cat_key, cat_objs['Electrónica']), 'cost_price': cost, 'sale_price': price, 'stock': stock, 'min_stock': min_stock}
    )
    print(f"  ✓ {name}")

print("\n¡Datos de prueba cargados exitosamente!")
