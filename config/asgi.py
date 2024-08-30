# asgi.py
import os
from configurations.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")
os.environ.setdefault("DJANGO_CONFIGURATION", "Development")  # Set your configuration class name

application = get_asgi_application()