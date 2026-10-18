# -*- coding: utf-8 -*-
"""ASGI config for Pezeshkan Medical Ecosystem."""
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
application = get_asgi_application()
