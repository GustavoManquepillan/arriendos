"""
WSGI config for arriendos project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

# Establece la configuración de DJANGO_SETTINGS_MODULE
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'arriendos.settings')

# Obtiene la aplicación WSGI para este proyecto Django
application = get_wsgi_application()
