from django.apps import AppConfig


class MultitenantUsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'multitenant_users'
