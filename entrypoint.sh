#!/bin/sh
set -e

mkdir -p logs

MAX_ATTEMPTS=30
ATTEMPT=1

echo "⏳ Aguardando o banco ficar disponível em $DB_HOST:$DB_PORT..."

while ! nc -z $DB_HOST $DB_PORT; do
  if [ $ATTEMPT -ge $MAX_ATTEMPTS ]; then
    echo "❌ Timeout: banco não ficou disponível após $MAX_ATTEMPTS tentativas."
    exit 1
  fi
  echo "🔄 Esperando PostgreSQL subir... (tentativa $ATTEMPT/$MAX_ATTEMPTS)"
  ATTEMPT=$((ATTEMPT + 1))
  sleep 1
done

echo "✅ Banco disponível, aplicando migrations..."
python manage.py migrate --noinput

echo "🚀 Iniciando servidor Django..."
exec "$@"
