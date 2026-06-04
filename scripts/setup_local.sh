#!/bin/bash
echo "=== Configuración InvStock Local ==="

# Copiar .env
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✓ .env creado — edita las variables antes de continuar"
fi

# Virtualenv
python -m venv venv
source venv/bin/activate || source venv/Scripts/activate
pip install -r requirements.txt

# Migraciones
python manage.py makemigrations accounts inventory sales dashboard
python manage.py migrate

# Datos de prueba
python manage.py shell < scripts/seed_data.py

echo ""
echo "=== ✅ Proyecto listo ==="
echo "Ejecuta: python manage.py runserver"
echo "URL: http://127.0.0.1:8000"
echo "Admin Django: http://127.0.0.1:8000/admin  (admin / Admin1234!)"
