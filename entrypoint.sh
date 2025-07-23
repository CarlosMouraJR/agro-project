#!/bin/sh
set -e

echo "⏳ Aguardando o banco ficar disponível em db:5432..."
while ! nc -z db 5432; do
  echo "🔄 Esperando PostgreSQL subir..."
  sleep 1
done

echo "✅ Banco disponível, aplicando migrations..."
python manage.py migrate --noinput

echo "🚀 Iniciando servidor Django..."
exec "$@"
