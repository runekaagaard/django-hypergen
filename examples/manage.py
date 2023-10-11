#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

# Backport and monkeypatch urls.path function for Django 1.11.29.
# Great job, chatgpt! <3
if django.VERSION < (2, 0):
    try:
        from django.conf.urls import url as re_path_, path as path_
    except ImportError:
        try:
            from django.urls import re_path as re_path_, path as path_
        except ImportError:
            from django.conf.urls import url as re_path_

    import django
    import django.urls

    def simple_path(route, *args, **kwargs):
        converters = {
            '<int:': r'(?P<{}>[0-9]+)',
            '<slug:': r'(?P<{}>[-\w]+)',
            '<str:': r'(?P<{}>[^/]+)',}

        pattern = route
        for key, value in converters.items():
            start_pos = 0
            while key in pattern[start_pos:]:
                param_start = pattern.find(key, start_pos)
                param_end = pattern.find('>', param_start)
                param_name = pattern[param_start + len(key):param_end]

                pattern = pattern[:param_start] + value.format(param_name) + pattern[param_end + 1:]
                start_pos = param_start + len(value.format(param_name))

        return re_path_(pattern, *args, **kwargs)

    django.urls.path = simple_path
    django.urls.re_path = re_path_

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError("Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?") from exc

    import websockets.routing
    import features.routing

    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
