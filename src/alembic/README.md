Инициализировать Alembic в проекте (должен использоваться асинхронный шаблон)
```bash
poetry run alembic init --template async alembic 
```

При первом запуске указать нулевое состояние базы
```bash
poetry run alembic stamp head
```

Создать миграции, если внесены изменения в ``/orm``
```bash
poetry run alembic revision --autogenerate -m "Your commit"
``` 

Применить миграции
```bash
poetry run alembic upgrade head
```
