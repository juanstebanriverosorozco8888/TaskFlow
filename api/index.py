import os

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings"
)

from django.core.management import execute_from_command_line

try:
    execute_from_command_line(
        ["manage.py", "migrate", "--noinput"]
    )
except Exception as e:
    print("ERROR MIGRATE:", e)

from django.core.wsgi import get_wsgi_application

app = get_wsgi_application()