# TaskFlow API

Этот проект представляет собой API для онлайн диспетчера задач. 
API разработано с использованием FastAPI и предназначено для управления задачами для пользователей.

## Настройка окружения

Перед запуском проекта необходимо установить зависимости `pip install -r requirements.txt`,
настроить переменные окружения в файле `.env`. Пример файла находится в .env.example

## Создание базы данных
### Обычная база данных

Для создания основной базы данных и настройки пользователей выполните следующие шаги:
```bash
# Подключение к PostgreSQL:
psql -U postgres

CREATE DATABASE your_db_name; # Создание базы данных
CREATE USER your_user WITH PASSWORD 'your_password'; # Создание пользователя с паролем
GRANT ALL PRIVILEGES ON DATABASE your_db_name TO your_user; # Предоставление привилегий пользователю
    
# Подключение к созданной базе данных:
\c your_db_name

# Предоставление прав на схему public:
GRANT USAGE ON SCHEMA public TO your_user;
GRANT CREATE ON SCHEMA public TO your_user;
```
### Тестовая база данных

Для создания тестовой базы данных выполните аналогичные шаги:

```bash
# Подключение к PostgreSQL:
psql -U postgres

CREATE DATABASE your_db_name_test; # Создание базы данных
CREATE USER your_user_test WITH PASSWORD 'your_password_test'; # Создание пользователя с паролем
GRANT ALL PRIVILEGES ON DATABASE your_db_name_test TO your_user_test; # Предоставление привилегий пользователю
    
# Подключение к созданной базе данных:
\c your_db_name_test

# Предоставление прав на схему public:
GRANT USAGE ON SCHEMA public TO your_user_test;
GRANT CREATE ON SCHEMA public TO your_user_test;
```
## Настройка Alembic

1. Инициализируйте Alembic, чтобы создать структуру для миграций:

   ```bash
   alembic init migrations
   ```
2. Настройте файл alembic.ini:

    Откройте файл alembic.ini и найдите строку, где указывается sqlalchemy.url.
    Замените её на строку подключения к вашей базе данных:
   ```
    sqlalchemy.url = postgresql://your_user:your_password@localhost/task_manager
   ```
3. Также установите шаблон для имен файлов миграций, добавив следующую строку:
    ```
    file_template = %%(year)d_%%(month).2d_%%(day).2d_%%(hour).2d%%(minute).2d-%%(rev)s_%%(slug)s
   ```
4. Настройте файл migrations/env.py:

    Откройте файл migrations/env.py и добавьте импорт метаданных вашей базы данных:
    ```
    from app.db.models import Base
    target_metadata = Base.metadata
   ```
   
5. Для применения миграции к базе данных выполните команду:
    ```
    alembic upgrade head
   ```
   
6.  Для создания миграции выполните команду:
    ```
    alembic revision --autogenerate -m "Initial migration"
    ```

## Форматирование кода

Перед использованием `black .` и `isort .`, рекомендуется сначала проверить изменения с помощью:

```
black --diff . 
isort --diff .
```


