FROM python:3.12-alpine

# Установка менеджера зависимостей uv
RUN pip install --no-cache-dir uv

# Установка рабочей директории
WORKDIR /app

# Копирование зависимостей
COPY pyproject.toml uv.lock* ./

# Установка зависимостей приложения
RUN uv pip install --system --no-cache


# Копирование исходного кода
COPY . .

# Команда запуска Uvicorn-сервера
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
