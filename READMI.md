# 🦊 Лисья школа

**Лисья школа** — это Telegram-бот, который помогает учителю геймифицировать учебный процесс.  
Ученики регистрируются в боте, выбирают персонажа и взаимодействуют с учителем, получая или теряя внутриигровую валюту и прокачивая уровень.

## 📋 Возможности

- **Регистрация учеников** — каждый ученик создает профиль и выбирает персонажа.
- **Система уровней** — учитель может повышать уровень учеников.
- **Внутриигровая валюта** — начисление и списание монет учителем.
- **Прозрачность действий** — ученики видят изменения, внесённые учителем.
- **Геймификация обучения** — превращение урока в увлекательную игру.

## 🛠️ Технологии

- **Python** 3.12
- **Redis** — хранение состояний.
- **aiogram_dialog** — построение интерактивных диалогов в Telegram.
- **SQLAlchemy** + **alembic** — ORM и миграции базы данных.
- **aiosqlite** — асинхронная работа с SQLite.


## 🎯 Целевая аудитория

Учителя средних и старших классов, которые хотят сделать уроки более увлекательными и мотивировать учеников через игровой процесс.


## Установка и запуск через docker compose

Требования:
- docker 24+ и docker compose v2+
- токен телеграм-бота

## 🚀 Установка и запуск

1. **Клонировать репозиторий**
   ```bash
   git clone https://github.com/morarsv/school-bot.git
   cd school-bot

2. **Собрать образ на сервере**
    ```bash
    docker build . -t school-bot:latest
    ```
2. **Создайте docker-compose.yaml**
    ```
    services:
    
      bot:
        image: school-bot:latest
        container_name: bot_school
        restart: unless-stopped
        env_file: ".env"
        volumes:
          - /home/service/bot/logs:/app/src/logs # логи
          - /home/service/bot/data/db:/app/data # директория бд
        depends_on:
          redis-school:
            condition: service_started
        networks:
          - schoolnet
    
      redis-school:
          image: "redis:7-alpine"
          container_name: redis-school
          restart: unless-stopped
          healthcheck:
              test: [ "CMD", "redis-cli","ping" ]
          networks:
           - schoolnet
    
    
    networks:
      schoolnet:
    ```
3. **Создать и заполнить файл .env**
    ```
    BOT_TOKEN= #Токен вашего бота
    URL_SQLITE=sqlite+aiosqlite:///data/iq_game.db
    HOST_REDIS=redis-school
    PORT_REDIS=6379
    ADMIN_ID=123456,654789,147258 #Telegram ID администратора(-ов)
    ```
4. **Запуск**
    ```bash
    docker compose up -d
    ```
   **Остановка**
    ```bash
    docker compose stop
    ```