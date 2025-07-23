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

echo "⏳ Verificando se banco precisa ser populado..."

TABLE_NAME="agronegocio_producer"

TABLE_EXISTS=$(python -c "from django.db import connection; cursor=connection.cursor(); cursor.execute(\"SELECT to_regclass('public.${TABLE_NAME}')\"); print(cursor.fetchone()[0])")

if [ "$TABLE_EXISTS" = "$TABLE_NAME" ]; then
  ROW_COUNT=$(python -c "from django.db import connection; cursor=connection.cursor(); cursor.execute(\"SELECT COUNT(*) FROM ${TABLE_NAME}\"); print(cursor.fetchone()[0])")
  if [ "$ROW_COUNT" -eq 0 ]; then
    echo "🚀 Banco vazio, rodando seed..."
    python manage.py seed
  else
    echo "✅ Banco já populado, pulando seed."
  fi
else
  echo "❌ Tabela ${TABLE_NAME} não encontrada."
fi

echo "🚀 Iniciando servidor Django..."
exec "$@"
