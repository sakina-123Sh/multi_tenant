from django.db import connection
from django.db.utils import DEFAULT_DB_ALIAS

class MultiTenancyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Logic to determine the tenant
        # For simplicity, let's assume the tenant is identified by a request header 'Tenant-ID'
        tenant_id = request.headers.get('Tenant-ID', None)

        # Set up the database connection for the current tenant
        if tenant_id:
            self.set_tenant_connection(tenant_id)

        response = self.get_response(request)

        # Reset the database connection after the request is processed
        self.reset_connection()

        return response

    def set_tenant_connection(self, tenant_id):
        tenant_database_mapping = {
            'tenant1': 'tenant1_db',
            'tenant2': 'tenant2_db',
            # Add more mappings as needed
        }

        # Get the database name for the given tenant ID
        database_name = tenant_database_mapping.get(tenant_id)

        # Configure the database connection
        if database_name:
            connection.settings_dict[DEFAULT_DB_ALIAS]['NAME'] = database_name

    def reset_connection(self):

        connection.close()
