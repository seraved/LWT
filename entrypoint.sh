#!/bin/sh

# Выход из скрипта при любой ошибке
set -e

echo "Entrypoint script started"

# Запуск миграций Alembic
echo "Running database migrations..."
alembic upgrade head
echo "Migrations applied successfully"

# Запуск основной команды контейнера
echo "Run app"
python ./lwt_app/main.py