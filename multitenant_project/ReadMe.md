
Documentation

```bash
# Make sure you have git installed
git clone https://github.com/sakina-123Sh/multi_tenant.git

```

-> Create Virtual environment

```bash
# Windows
py -3 -m venv env
# Linux and Mac
python3 -m venv env
```

-> Activate environment

```bash
# Windows
.\env\Scripts\activate
# Linux and Mac
source env/bin/activate
```

-> Install Requirements

```bash
pip install -r requirements.txt
```

-> Make sure project is running

```bash
python manage.py runserver
```

-> Install django tenants


-> Setup Middleware and Database. First create a PostgreSQL database and
note the user and password

```py

MIDDLEWARE = [
    # add this at the top
    # django tenant middleware
    'django_tenants.middleware.main.TenantMainMiddleware',

    #........
]


# Setup Postgres database in settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django_tenants.postgresql_backend',
        'NAME': 'samtadb',
        'USER': 'usersamta',
        'PASSWORD': 'samta',
        'HOST': 'localhost',  # Or the host where your PostgreSQL server is running
        'PORT': '5432',       # Default PostgreSQL port
    }
}

# DATABASE ROUTER
DATABASE_ROUTERS = (
    'django_tenants.routers.TenantSyncRouter',
)

```

-> Configure TENANT_MODEL and TENANT_DOMAIN_MODEL

```py
TENANT_MODEL = 'multitenant_users.Tenant'  # Define the tenant model
TENANT_DOMAIN_MODEL = 'multitenant_users.Domain'

```

-> Setup SHARED_APPS and TENANT_APPS

```py
# Application definition
"""
    These app's data are stored on the public schema
"""
SHARED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_tenants',
    'multitenant_users',
]
"""
    These app's data are stored on their specific schemas
"""
TENANT_APPS = [
    # The following Django contrib apps must be in TENANT_APPS
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.sessions',
    'django.contrib.messages',
    # tenant-specific apps
    'multitenant_users',
]


INSTALLED_APPS = list(SHARED_APPS) + [
    app for app in TENANT_APPS if app not in SHARED_APPS
]

```

-> Make migrations and Apply to database

```bash
# create migrations files
python manage.py makemigrations
# You may need to run migrations for specific app
python manage.py makemigrations user_app
# Apply migrations
python manage.py migrate_schemas
```

-> Setup Initial User, Tenant and Admin

```bash
# create first user
python manage.py createsuperuser
# Create the Public Schema
python manage.py create_tenant
# Create the Administrator
python manage.py create_tenant_superuser
python manage.py runserve
```
