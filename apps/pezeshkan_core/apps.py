# -*- coding: utf-8 -*-
from django.apps import AppConfig
from django.db.backends.signals import connection_created

def configure_sqlite_concurrency(sender, connection, **kwargs):
    """
    Ensures SQLite connections use WAL mode, 30s busy timeout, and memory cache
    to eliminate 'database is locked' errors under thousands of concurrent users.
    """
    if connection.vendor == 'sqlite':
        try:
            cursor = connection.cursor()
            cursor.execute("PRAGMA journal_mode=WAL;")
            cursor.execute("PRAGMA synchronous=NORMAL;")
            cursor.execute("PRAGMA busy_timeout=30000;")
            cursor.execute("PRAGMA cache_size=-64000;")
            cursor.execute("PRAGMA temp_store=MEMORY;")
        except Exception:
            pass

class PezeshkanCoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.pezeshkan_core'
    verbose_name = 'Pezeshkan Medical Core'

    def ready(self):
        connection_created.connect(configure_sqlite_concurrency)
