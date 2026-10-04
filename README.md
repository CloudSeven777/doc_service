# Document Search Service

Асинхронный REST API-сервис для хранения, поиска и удаления документов.

Данные документов хранятся в SQLite, а полнотекстовый поиск выполняется с помощью Elasticsearch.

## Возможности

- создание документов;
- хранение документов в SQLite;
- индексация документов в Elasticsearch;
- полнотекстовый поиск;
- получение полных данных найденных документов из SQLite;
- сортировка результатов по дате создания;
- возврат до 20 результатов поиска;
- удаление документов из SQLite и Elasticsearch;
- импорт документов из CSV;
- автоматические API-тесты;
- запуск приложения через Docker Compose.

## Технологии

- Python 3.13
- FastAPI
- SQLAlchemy (async)
- SQLite
- aiosqlite
- Elasticsearch
- AsyncElasticsearch
- Pydantic
- Uvicorn
- pytest
- pytest-asyncio
- httpx
- Docker
- Docker Compose

## Асинхронность

API реализован с использованием `async/await`.

Для асинхронной работы с базой данных используется SQLAlchemy `AsyncSession`
и драйвер `aiosqlite`.

Взаимодействие с Elasticsearch выполняется через `AsyncElasticsearch`.

## API

### Создание документа

```text
POST /documents
```

Создаёт документ в SQLite и индексирует его в Elasticsearch.

Пример тела запроса:

```json
{
  "id": 1,
  "rubrics": ["python", "backend"],
  "text": "Example document",
  "created_date": "2026-10-04"
}
```

### Поиск документов

```text
GET /documents/search?q=...
```

Поиск выполняется по полю `text` с помощью Elasticsearch.

После поиска идентификаторы найденных документов используются для получения
полных записей из SQLite.

Результаты сортируются по `created_date`. Возвращается до 20 документов.

Пример:

```text
GET /documents/search?q=Россия
```

### Удаление документа

```text
DELETE /documents/{document_id}
```

Удаляет документ из SQLite и Elasticsearch.

## Локальный запуск

### 1. Создание виртуального окружения

```bash
python -m venv .venv
```

### 2. Активация виртуального окружения

Windows:

```bash
.venv\Scripts\activate
```

### 3. Установка зависимостей

```bash
python -m pip install -r requirements.txt
```

### 4. Запуск Elasticsearch

Elasticsearch можно запустить с помощью Docker:

```bash
docker run -d --name elasticsearch -p 9200:9200 -e "discovery.type=single-node" -e "xpack.security.enabled=false" docker.elastic.co/elasticsearch/elasticsearch:9.1.4
```

Проверить состояние контейнера:

```bash
docker ps
```

### 5. Загрузка данных

```bash
python load_data.py
```

Скрипт загружает документы из `posts.csv` в SQLite и индексирует их
в Elasticsearch.

### 6. Запуск FastAPI

```bash
uvicorn main:app --reload
```

После запуска Swagger UI доступен по адресу:

```text
http://localhost:8000/docs
```

## Запуск через Docker Compose

Проект можно полностью запустить с помощью Docker Compose.

### 1. Сборка и запуск контейнеров

```bash
docker compose up --build
```

Будут запущены два сервиса:

- FastAPI;
- Elasticsearch.

### 2. Загрузка данных

В отдельном терминале:

```bash
docker compose exec app python load_data.py
```

### 3. Swagger UI

После запуска:

```text
http://localhost:8000/docs
```

### 4. Остановка контейнеров

```bash
docker compose down
```

## Тестирование

Для запуска автоматических тестов:

```bash
python -m pytest -v
```

Тесты проверяют:

- доступность OpenAPI;
- поиск документов;
- создание документа;
- удаление тестового документа.

Тестирование асинхронного API выполняется с помощью `pytest-asyncio`
и `httpx.AsyncClient`.

## OpenAPI

OpenAPI-схема проекта сохранена в:

```text
docs.json
```

Интерактивная документация FastAPI доступна через Swagger UI:

```text
http://localhost:8000/docs
```

## Структура проекта

```text
doc_service/
├── tests/
│   └── test_api.py
├── database.py
├── elasticsearch_client.py
├── load_data.py
├── main.py
├── models.py
├── schemas.py
├── posts.csv
├── docs.json
├── requirements.txt
├── pytest.ini
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .gitignore
└── README.md
```