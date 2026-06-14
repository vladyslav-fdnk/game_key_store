# Используем официальный образ uv от Astral в качестве источника бинарников
FROM ghcr.io/astral-sh/uv:latest AS uv_bin

FROM python:3.11-slim

# Копируем бинарники uv в финальный контейнер
COPY --from=uv_bin /uv /uvx /bin/

# Отключаем буферизацию логов и генерацию pyc-файлов
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Установка системных зависимостей для сборки (необходимо для psycopg2)
RUN apt-get update && apt-get install -y --no-install-recommends     build-essential     libpq-dev     && rm -rf /var/lib/apt/lists/*

# Копируем требования для установки
COPY requirements.txt /app/

# Сверхбыстрая установка зависимостей напрямую в систему (благодаря --system) с помощью uv!
RUN uv pip install --system --no-cache -r requirements.txt

# Копируем остальной код бота в контейнер
COPY . /app/