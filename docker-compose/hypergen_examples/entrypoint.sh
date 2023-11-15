#!/bin/bash

set -euo pipefail

python manage.py collectstatic --no-input
exec daphne --bind 0.0.0.0 -p 8000 --access-log - --verbosity 1 asgi:application
