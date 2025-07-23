#!/bin/sh
set -e

echo "⏳ Aguardando o banco ficar disponível em $DB_HOST:$DB_PORT..."
while ! nc -z $DB_HOST $DB_PORT; do
  echo "🔄 Esperando PostgreSQL subir..."
  sleep 1
done

echo "✅ Banco disponível, aplicando migrations..."
python manage.py migrate --noinput

echo "🚀 Iniciando servidor Django..."
exec "$@"
