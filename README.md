# 🔗 YADRO URL Alias Service

**YADRO\_url\_alias\_service** — это микросервис для сокращения ссылок, созданный на базе **FastAPI**, с использованием **PostgreSQL**, **SQLAlchemy**, **Alembic**, **Uvicorn**, и системой планирования задач на **APScheduler**. Поддерживает JWT-аутентификацию, сбор статистики переходов и авто-деактивацию ссылок по времени.

---

## 🚀 Функциональность

* ✅ Генерация коротких ссылок
* 🔐 JWT-аутентификация
* 📊 Подсчёт кликов ( за час/день )
* 🗓️ Плановая деактивация просроченных ссылок и обнуление кликов
* 🧠 Асинхронный стек (FastAPI + Async SQLAlchemy)
* ✨ Поддержка тестирования через HTTP-клиенты (Insomnia/Postman)

---

## 🎞️ Стек технологий

| Компонент         | Технология   |
| ----------------- | ------------ |
| Язык              | Python 3.10+ |
| Web Framework     | FastAPI      |
| БД                | PostgreSQL   |
| ORM               | SQLAlchemy   |
| Аутентификация    | JWT (OAuth2) |
| Планировщик задач | APScheduler  |
| Логирование       | Loguru       |
| Валидация         | Pydantic     |
| Докеризация       | Docker       |

---

## 🛠️ Установка и запуск

### 🔧 Клонирование проекта

```bash
git clone git@github.com:Rxyalxrd/YADRO_url_alias_service.git
cd YADRO_url_alias_service
```

### ⚙️ .env

Создать в `src` `.env` и заполнить его по примеру `.env.example`:

```bash
################
# App Settings #
################

APP_HOST=127.0.0.1                                                     # Хост, на котором запускается приложение
APP_PORT=8000                                                          # Порт, на котором запускается приложение
APP_TITLE=FastAPI URL Shortener                                        # Название вашего приложения
APP_DESCRIPTION=Сервис для сокращения URL с авторизацией пользователей # Описание приложения

##############
# PostgreSQL #
##############

POSTGRES_USER=postgres                                                 # Имя пользователя базы данных
POSTGRES_PASSWORD=password                                             # Пароль пользователя базы данных
POSTGRES_HOST=localhost                                                # Хост базы данных (например, db или localhost)
POSTGRES_DB=shortener_db                                               # Название базы данных
POSTGRES_PORT=5432                                                     # Порт базы данных PostgreSQL

########
# HASH #
########

HASH_SECRET_KEY=supersecretkey                                         # Секретный ключ для генерации токенов
ALGORITHM=HS256                                                        # Алгоритм шифрования JWT
ACCESS_TOKEN_EXPIRE_MINUTES=30                                         # Время жизни токена в минутах
```

---

### 💣 Запуск через Docker

#### 1. Собрать и запустить контейнеры

Перейти в корень проекта (где `docker-compose.yml`) и выполнить:

```bash
docker-compose up --build
```

#### 2. Проверка доступа

После запуска приложение будет доступно по адресу:

```
http://localhost:8000/docs
```

---

### 💻 Локальный запуск

1. Установить`Poetry`
2. Подключиться к БД
3. Установить зависимости
   ```bash
   cd src
   make install
   make migrate
   ```
4. Запустить приложение

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
