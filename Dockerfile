
# --- Этап 1: Сборщик (Builder) ---
# Этот этап используется для установки зависимостей.
# Артефакты этого этапа будут скопированы в финальный образ,
# а сам этап будет отброшен, что уменьшает размер итогового образа.

FROM python:3.11-slim as builder

# Устанавливаем переменные окружения
# PYTHONUNBUFFERED: обеспечивает немедленный вывод логов в stdout/stderr
# PYTHONDONTWRITEBYTECODE: предотвращает создание .pyc файлов
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Устанавливаем зависимости в отдельную директорию,
# чтобы потом скопировать только их в финальный образ.
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix="/install" -r requirements.txt


# --- Этап 2: Финальный образ ---
# Этот этап создает чистый образ только с необходимыми файлами.
FROM python:3.11-slim

# Повторяем установку переменных окружения
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Создаем непривилегированного пользователя для запуска приложения.
# Это лучшая практика с точки зрения безопасности.
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

# Устанавливаем рабочую директорию в домашней папке нового пользователя
WORKDIR /home/appuser/app

# Копируем установленные зависимости из этапа сборщика
COPY --from=builder /install /usr/local

# Копируем исходный код приложения и устанавливаем правильного владельца
COPY --chown=appuser:appgroup . .

# Устанавливаем права на выполнение для entrypoint скрипта
RUN chmod +x ./entrypoint.sh

# Переключаемся на непривилегированного пользователя
USER appuser

# # Команда для запуска приложения
# CMD ["python", "./lwt_app/main.py"]
