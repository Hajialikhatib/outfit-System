#!/usr/bin/env python
"""
SQLite → MySQL Data Migration Script
====================================
This script exports data from a SQLite database and imports it into MySQL using
Django's serializers. It preserves relationships for all project apps.

Usage:
  1) Ensure MySQL is configured in .env and migrations have been applied:
       python manage.py migrate
  2) Run the migration:
       python migrate_sqlite_to_mysql.py

Optional environment variables:
  SQLITE_DB_PATH=/path/to/db.sqlite3
  MIGRATION_APPS=accounts,styles,orders,feedback
"""

import os
import sys
from io import StringIO

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nguoSystem.settings')
django.setup()

from django.conf import settings
from django.apps import apps
from django.core.management import call_command
from django.db import connections, transaction


def parse_apps(value: str) -> list[str]:
    return [app.strip() for app in value.split(',') if app.strip()]


def configure_sqlite_alias(sqlite_path: str) -> None:
    settings.DATABASES['sqlite'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': sqlite_path,
    }
    connections.databases = settings.DATABASES


def dump_sqlite_data(app_labels: list[str]) -> str:
    out = StringIO()
    call_command(
        'dumpdata',
        *app_labels,
        database='sqlite',
        format='json',
        natural_foreign=True,
        natural_primary=True,
        verbosity=1,
        stdout=out,
    )
    return out.getvalue()


def load_mysql_data(payload: str) -> None:
    call_command(
        'loaddata',
        '-',
        database='default',
        format='json',
        verbosity=1,
        stdin=StringIO(payload),
    )


def validate_counts(app_labels: list[str]) -> tuple[list[str], list[str]]:
    matches = []
    mismatches = []
    for model in apps.get_models():
        if model._meta.app_label not in app_labels:
            continue
        sqlite_count = model.objects.using('sqlite').count()
        mysql_count = model.objects.using('default').count()
        label = f"{model._meta.label}: sqlite={sqlite_count}, mysql={mysql_count}"
        if sqlite_count == mysql_count:
            matches.append(label)
        else:
            mismatches.append(label)
    return matches, mismatches


def main() -> int:
    sqlite_path = os.environ.get('SQLITE_DB_PATH', os.path.join(settings.BASE_DIR, 'db.sqlite3'))
    if not os.path.exists(sqlite_path):
        print(f"SQLite database not found: {sqlite_path}")
        return 1

    app_labels = parse_apps(os.environ.get('MIGRATION_APPS', 'accounts,styles,orders,feedback'))

    print("Configuring SQLite connection...")
    configure_sqlite_alias(sqlite_path)

    print("Exporting data from SQLite...")
    payload = dump_sqlite_data(app_labels)
    if not payload.strip():
        print("No data found in SQLite. Nothing to migrate.")
        return 0

    print("Importing data into MySQL...")
    with transaction.atomic(using='default'):
        load_mysql_data(payload)

    print("Validating row counts...")
    matches, mismatches = validate_counts(app_labels)
    for line in matches:
        print(f"✓ {line}")
    for line in mismatches:
        print(f"✗ {line}")

    if mismatches:
        print("Migration completed with count mismatches.")
        return 2

    print("Migration completed successfully.")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())