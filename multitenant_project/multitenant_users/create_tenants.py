# In a file named create_tenants.py inside one of your Django apps

from django.core.management.base import BaseCommand
from multitenant_users.models import Tenant

class Command(BaseCommand):
    help = 'Create tenants'

    def handle(self, *args, **options):
        # Create tenants here
        Tenant.objects.create(name='Tenant 1')
        Tenant.objects.create(name='Tenant 2')
        # Add more tenants as needed
