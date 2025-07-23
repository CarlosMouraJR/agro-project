FROM python:3.13-slim

# Ensure all system packages are up-to-date to reduce vulnerabilities
RUN apt-get update && apt-get upgrade -y && apt-get clean && rm -rf /var/lib/apt/lists/*

# Impede a criação de arquivos .pyc e mantém logs no stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Cria o diretório de trabalho
WORKDIR /code

# Instala dependências
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia o restante do projeto
COPY . .

# Dá permissão de execução ao entrypoint
RUN chmod +x /code/entrypoint.sh

# Instala netcat para o script de espera do banco
RUN apt-get update && apt-get install -y netcat-openbsd && apt-get upgrade -y && apt-get clean && rm -rf /var/lib/apt/lists/*

# Usa o entrypoint para controlar startup
ENTRYPOINT ["/code/entrypoint.sh"]

CMD ["gunicorn", "agronegocio.wsgi:application", "--bind", "0.0.0.0:8000"]
