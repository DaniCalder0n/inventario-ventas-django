# InvStock — Guía de Instalación y Despliegue

## Requisitos previos
- Python 3.10+
- PostgreSQL 14+
- Docker & Docker Compose (para despliegue)
- Git

---

## 🖥️ Instalación Local (Desarrollo)

### 1. Clonar y configurar entorno

```bash
git clone <url-repositorio> inventario_ventas
cd inventario_ventas

python -m venv venv
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

pip install -r requirements.txt
```

### 2. Configurar variables de entorno

```bash
cp .env.example .env
```

Edita `.env` con tus datos:

```
SECRET_KEY=genera-una-clave-con: python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
DEBUG=True
DB_NAME=inventario_db
DB_USER=postgres
DB_PASSWORD=tu_password
DB_HOST=localhost
DB_PORT=5432
```

### 3. Crear base de datos PostgreSQL

```sql
CREATE DATABASE inventario_db;
```

### 4. Migraciones y datos iniciales

```bash
python manage.py makemigrations accounts inventory sales dashboard
python manage.py migrate
python manage.py shell < scripts/seed_data.py
python manage.py collectstatic --noinput
```

### 5. Ejecutar

```bash
python manage.py runserver
```

Accede en: **http://127.0.0.1:8000**

---

## 🐳 Despliegue con Docker Compose

### 1. Configurar .env para producción

```env
SECRET_KEY=clave-secreta-larga-aleatoria
DEBUG=False
ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com
DB_NAME=inventario_db
DB_USER=postgres
DB_PASSWORD=password_muy_seguro
DB_HOST=db
DB_PORT=5432
```

### 2. Construir y levantar servicios

```bash
docker-compose up --build -d
```

### 3. Inicializar base de datos en el contenedor

```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py shell < scripts/seed_data.py
```

### 4. Ver logs

```bash
docker-compose logs -f web
```

### 5. Detener servicios

```bash
docker-compose down
```

---

## 👥 Credenciales de prueba

| Usuario | Contraseña | Rol |
|---------|-----------|-----|
| `admin` | `Admin1234!` | Administrador |
| `vendedor1` | `Vendedor1234!` | Vendedor |
| `cliente1` | `Cliente1234!` | Cliente |

Admin de Django: http://localhost:8000/admin

---

## 📋 URLs principales

| URL | Descripción |
|-----|------------|
| `/` | Catálogo público |
| `/accounts/login/` | Inicio de sesión |
| `/accounts/register/` | Registro de cliente |
| `/dashboard/` | Dashboard (admin/vendedor) |
| `/inventory/` | Gestión de inventario |
| `/sales/cart/` | Carrito de compras |
| `/sales/orders/` | Mis pedidos |
| `/accounts/users/` | Gestión de usuarios (admin) |
| `/inventory/movements/` | Historial movimientos |
| `/admin/` | Admin Django |

---

## 🔒 Roles y permisos

| Acción | Admin | Vendedor | Cliente |
|--------|-------|----------|---------|
| Ver catálogo | ✅ | ✅ | ✅ |
| Agregar al carrito | — | — | ✅ |
| Ver inventario | ✅ | ✅ | ❌ |
| Crear productos | ✅ | ❌ | ❌ |
| Editar productos | ✅ | ❌ | ❌ |
| Actualizar stock | ✅ | ✅ | ❌ |
| Ver costos | ✅ | ❌ | ❌ |
| Dashboard | ✅ | ✅ | ❌ |
| Gestionar usuarios | ✅ | ❌ | ❌ |
| Ver pedidos propios | — | — | ✅ |
| Ver todos los pedidos | ✅ | ✅ | ❌ |

---

## 🏗️ Estructura del proyecto

```
inventario_ventas/
├── config/              # Configuración Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   ├── accounts/        # Usuarios, auth, roles
│   │   ├── models.py    # CustomUser
│   │   ├── views.py
│   │   ├── middleware.py
│   │   ├── decorators.py
│   │   └── forms.py
│   ├── inventory/       # Productos, stock
│   │   ├── models.py    # Product, Category, InventoryMovement
│   │   ├── views.py
│   │   ├── services.py
│   │   └── forms.py
│   ├── sales/           # Carrito, pedidos
│   │   ├── models.py    # Cart, Order, OrderItem
│   │   ├── views.py
│   │   └── services.py
│   └── dashboard/       # KPIs, reportes
├── templates/           # Templates HTML
├── static/css/          # Estilos Bootstrap+personalizados
├── media/products/      # Imágenes subidas
├── docker/              # Dockerfile + nginx.conf
├── scripts/             # seed_data.py, setup_local.sh
├── requirements.txt
├── docker-compose.yml
└── .env.example
```

---

## ⚙️ Comandos útiles

```bash
# Crear superusuario adicional
python manage.py createsuperuser

# Shell interactivo
python manage.py shell

# Ver migraciones pendientes
python manage.py showmigrations

# Backup de base de datos (con Docker)
docker-compose exec db pg_dump -U postgres inventario_db > backup.sql

# Restaurar backup
docker-compose exec -T db psql -U postgres inventario_db < backup.sql
```
