# Document Search Service

Сервис для хранения и полнотекстового поиска документов.

## Стек

- Python 3.13
- FastAPI
- SQLite
- SQLAlchemy
- Elasticsearch
- Docker

## Возможности

- создание документа;
- полнотекстовый поиск документов через Elasticsearch;
- получение данных документов из SQLite;
- удаление документов из SQLite и Elasticsearch;
- загрузка документов из `posts.csv`.

## Установка

Создайте виртуальное окружение:

```bash
python -m venv .venv
```

Активируйте его на Windows:

```bash
.venv\Scripts\activate
```

Установите зависимости:

```bash
pip install -r requirements.txt
```

## Запуск Elasticsearch

Elasticsearch запускается в Docker:

```bash
docker run -d --name elasticsearch -p 9200:9200 -e "discovery.type=single-node" -e "xpack.security.enabled=false" docker.elastic.co/elasticsearch/elasticsearch:9.1.4
```

Проверить работу контейнера:

```bash
docker ps
```

Elasticsearch должен быть доступен на `localhost:9200`.

## Загрузка данных

Для загрузки документов из `posts.csv` в SQLite и Elasticsearch выполните:

```bash
python load_data.py
```

## Запуск приложения

```bash
uvicorn main:app --reload
```

После запуска Swagger UI доступен по адресу:

`http://127.0.0.1:8000/docs`

## API

### Создание документа

`POST /documents`

Создаёт документ в SQLite и индексирует его текст в Elasticsearch.

### Поиск документов

`GET /documents/search?q=...`

Выполняет полнотекстовый поиск через Elasticsearch, получает найденные документы из SQLite, сортирует их по `created_date` и возвращает до 20 результатов.

### Удаление документа

`DELETE /documents/{id}`

Удаляет документ из SQLite и Elasticsearch.


## Запуск через Docker Compose

Проект можно полностью запустить с помощью Docker Compose.

```bash
docker compose up --build
```

После запуска загрузите данные:

```bash
docker compose exec app python load_data.py
```

Swagger UI будет доступен по адресу:

`http://localhost:8000/docs`

Для остановки контейнеров:

```bash docker compose down```

