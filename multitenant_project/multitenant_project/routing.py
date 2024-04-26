from django.db import connections
from django.conf import settings

def set_tenant_database(tenant_id):
    # Logic to set the database connection based on the tenant ID
    tenant_database_mapping = getattr(settings, 'TENANT_DATABASE_MAPPING', {})
    database_name = tenant_database_mapping.get(tenant_id)
    connection = connections['default']
    connection.settings_dict['NAME'] = database_name

def unset_tenant_database():
    # Reset the database connection after the request
    connection = connections['default']
    connection.settings_dict['NAME'] = 'default_db_name'

class MultiTenancyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Logic to determine the tenant for the current request
        # For example, get the tenant ID from request headers
        tenant_id = request.headers.get('Tenant-ID')

        if tenant_id:
            set_tenant_database(tenant_id)

        response = self.get_response(request)

        unset_tenant_database()

        return response
