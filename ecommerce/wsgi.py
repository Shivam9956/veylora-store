import os
import sys
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()

# Auto-migrate database and seed initial data on server launch
try:
    from django.core.management import call_command
    call_command('migrate', interactive=False)
    call_command('seed_data')
except Exception as e:
    print(f"[WSGI Startup Notice] Migration/Seed status: {e}", file=sys.stderr)

