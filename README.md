# Highload

Тестовый сервис для работы с высокими нагрузками.

## Требования

- Docker
- Docker Compose
- Make

## Установка и запуск

1. Склонируйте репозиторий в пустую директорию:

```bash
git clone https://github.com/Jeishod/highload.git .
```


2. Создайте файл `.env` на основе `.env.example`:

```bash
cp .env.example .env
```

3. Скорректируйте параметры в файле `.env` под ваш конфиг. Например:

```bash
POSTGRES_HOST=localhost # для локального запуска
POSTGRES_HOST=highload-postgres # для запуска через docker compose
```

4. Запустите PostgreSQL:

```bash
make up-postgres
```

5. Запустить сервис:

```bash
make up
```


6. Создать таблицы

```bash
make create-tables
```

7. Загрузить фикстуры

```bash
make load-fixtures
```

## Доступные ендпоинты

- `GET  /api/v1/shared/healthcheck` - проверка доступности сервиса
- `POST /api/v1/auth/register` - регистрация пользователя
- `POST /api/v1/auth/login` - авторизация пользователя
- `GET  /api/v1/users/me` - получить текущего пользователя (защищенный ендпоинт)
- `GET  /api/v1/users/get/{user_id}` - получить пользователя по id
