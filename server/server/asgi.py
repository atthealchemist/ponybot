"""
ASGI config for server project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
os.environ.setdefault('DJANGO_CONFIGURATION', 'Dev')

import configurations
configurations.setup()
from django.core.asgi import get_asgi_application

application = get_asgi_application()
