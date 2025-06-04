# 🔗 YADRO URL Alias Service

**YADRO\_url\_alias\_service** — это микросервис для сокращения ссылок, созданный на базе **FastAPI**, с использованием **PostgreSQL**, **SQLAlchemy**, **Alembic**, **Uvicorn**, и системой планирования задач на **APScheduler**. Поддерживает JWT-аутентификацию, сбор статистики переходов и авто-деактивацию ссылок по времени.

---

## 🚀 Функциональность

* ✅ Генерация коротких ссылок
* 🔐 JWT-аутентификация
* 📊 Подсчёт кликов ( за час/день )
* 🗓️ Плановая деактивация просроченных ссылок
* 🧠 Асинхронный стек (FastAPI + Async SQLAlchemy)
* 🫐 Поддержка тестирования через HTTP-клиенты (Insomnia/Postman)

---

## 🎞️ Стек технологий

| Компонент         | Технология             |
| ----------------- | ---------------------- |
| Язык              | Python 3.10+           |
| Web Framework     | FastAPI                |
| БД                | PostgreSQL             |
| ORM               | SQLAlchemy             |
| Аутентификация    | JWT (OAuth2)           |
| Планировщик задач | APScheduler            |
| Логирование       | Loguru                 |
| Валидация         | Pydantic               |
| Докеризация       | Docker                 |

---

## 🛠️ Установка и запуск

### 🔧 Клонирование проекта

```bash
git clone git@github.com:Rxyalxrd/YADRO_url_alias_service.git
cd YADRO_url_alias_service
```

### 💣 Запуск через Docker

```bash
docker-compose up --build
```

### 🫐 Локальный запуск
  1. Установить [uv](https://docs.astral.sh/uv/getting-started/installation)
  2. Установить зависимости
        ```bash
        cd src
        make install-dev
        make migrate
        ```
  3. Запустить приложение
     ```bash
     make run
     ```

---

## 🗂️ Структура проекта

```
app/
├── infra
└── src
    ├── alembic
    │   └── versions
    └── app
        ├── api                        # API приложения
        │   └── v1
        ├── auth                       # Регистрация, логин, токены
        │   ├── dependencies
        │   └── security
        ├── core                       # Настройки приложения, общие зависимости
        ├── dao                        # Взаимодействие с БД
        ├── models                     # SQLAlchemy ORM модели
        ├── schemas                    # Pydantic-схемы для валидации
        ├── tasks                      # Плановая задача деактивации ссылок
        └── url                        # Получение статистики, деактивация ссылок
```

---

## 📘 Автор

* GitHub: [Rxyalxrd](https://github.com/Rxyalxrd)

---
