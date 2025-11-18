#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cras360.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Django não está instalado; ative o venv e instale as dependências."
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
