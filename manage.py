# manage.py
import os
import sys
from configurations.management import execute_from_command_line


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")
    os.environ.setdefault("DJANGO_CONFIGURATION", "Development")  # Set your configuration class name

    try:
        execute_from_command_line(sys.argv)
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc


if __name__ == "__main__":
    main()