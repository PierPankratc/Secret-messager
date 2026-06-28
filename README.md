
```markdown
# Secret Messenger 🔐

**Сервис для отправки одноразовых зашифрованных сообщений.**  
Отправьте сообщение, получите ссылку — после первого прочтения оно самоуничтожится. Идеально для передачи конфиденциальной информации, паролей или ссылок, которые не должны храниться вечно.

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-D71F00?logo=sqlalchemy&logoColor=white)](https://sqlalchemy.org)
[![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?logo=docker&logoColor=white)](https://docker.com)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## ✨ Возможности

*   **🔐 Безопасность**: Сообщения шифруются с использованием Fernet (симметричное шифрование).
*   **👤 Регистрация и вход**: Простая аутентификация пользователей.
*   **🔗 Одноразовые ссылки**: После создания сообщения вы получаете уникальную ссылку.
*   **💥 Самоуничтожение**: Сообщение автоматически удаляется из базы данных после первого открытия.
*   **🐳 Docker и CI/CD**: Простой запуск в контейнере и готовый пайплайн для тестирования.
*   **🗄️ Миграции**: Управление схемой базы данных через Alembic.

## 🏗️ Архитектура проекта

Проект построен по модульному принципу. Вот его структура:

```
secrets-messager/
├── src/
│   ├── app/            # Главное FastAPI приложение и настройки
│   ├── db/             # Всё, что связано с базой данных
│   │   ├── models.py   # Модели (User, Message)
│   │   └── create_db.py# Логика подключения к БД и создания сессий
│   └── routers/        # Эндпоинты API (users, messages)
├── migrations/         # Скрипты миграций Alembic
├── tests/              # Автоматические тесты (pytest)
├── .github/workflows/  # Конфигурация GitHub Actions
├── .env                # Переменные окружения 
├── Dockerfile          # Инструкция для сборки Docker-образа
├── docker-compose.yml  # Для быстрого запуска всех сервисов
├── pyproject.toml      # Зависимости и настройки проекта
└── alembic.ini         # Конфигурация Alembic
```

## 📦 Установка и запуск

### Локальный запуск (для разработки)

1.  **Клонируйте репозиторий:**
    ```bash
    git clone https://github.com/PierPankratc/Secret-messager.git
    cd Secret-messager
    ```

2.  **Создайте и активируйте виртуальное окружение:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # для Linux/macOS
    # .venv\Scripts\activate   # для Windows
    ```

3.  **Установите зависимости:**
    ```bash
    pip install -e .
    ```

4.  **Настройте переменные окружения:**
    Создайте в корне проекта файл `.env` и укажите в нём:
    ```env
    DSN=sqlite:///./secrets.db
    FERNET_KEY=ваш_сгенерированный_ключ_fernet
    ```
    > Ключ Fernet можно сгенерировать, выполнив в Python: `from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())`.

5.  **Примените миграции:**
    ```bash
    alembic upgrade head
    ```

6.  **Запустите сервер:**
    ```bash
    uvicorn src.app.main:app --reload
    ```
    API будет доступно по адресу: [http://127.0.0.1:8000](http://127.0.0.1:8000). Интерактивная документация — [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

### 🐳 Запуск через Docker

Самый простой способ для быстрого старта или тестирования:

```bash
docker compose up --build
```

После сборки приложение будет доступно на том же адресе: [http://127.0.0.1:8000](http://127.0.0.1:8000).

## 🛠️ Основные команды

*   **Применить миграции:**
    ```bash
    alembic upgrade head
    ```
*   **Создать новую миграцию** (после изменения моделей):
    ```bash
    alembic revision --autogenerate -m "Описание изменений"
    ```
*   **Запустить тесты:**
    ```bash
    pytest -q
    ```

## 🚀 CI/CD

В проекте настроен GitHub Actions. При каждом пуше в репозиторий автоматически запускаются все тесты. Это гарантирует, что новый код не сломает существующую функциональность.

## 🛡️ Безопасность

*   Пароли пользователей хешируются с помощью **bcrypt** перед сохранением в базу данных.
*   Тело сообщения шифруется с использованием **Fernet**. Ключ для шифрования хранится в переменной окружения `FERNET_KEY`.
*   Сообщения хранятся в зашифрованном виде и удаляются при первом же прочтении.

## 🧪 Используемые технологии

*   **Backend-фреймворк:** [FastAPI](https://fastapi.tiangolo.com/)
*   **ORM:** [SQLAlchemy 2.0](https://www.sqlalchemy.org/)
*   **Миграции:** [Alembic](https://alembic.sqlalchemy.org/)
*   **База данных:** SQLite (для продакшена рекомендуется PostgreSQL)
*   **Хеширование:** [Bcrypt](https://github.com/pyca/bcrypt/)
*   **Шифрование:** [Cryptography (Fernet)](https://cryptography.io/)
*   **Тесты:** [Pytest](https://docs.pytest.org/)
*   **Контейнеризация:** Docker & Docker Compose

## 🤝 Как внести вклад

Если у вас есть идеи по улучшению проекта, вы всегда можете:

1.  Сделать форк репозитория.
2.  Создать ветку для вашей фичи (`git checkout -b feature/AmazingFeature`).
3.  Закоммитить изменения (`git commit -m 'Add some AmazingFeature'`).
4.  Отправить их в ваш форк (`git push origin feature/AmazingFeature`).
5.  Открыть Pull Request.

## 📄 Лицензия

Распространяется под лицензией MIT

---

**Автор:** [PierPankratc](https://github.com/PierPankratc)
