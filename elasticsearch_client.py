import os

from elasticsearch import Elasticsearch


ELASTICSEARCH_URL = os.getenv(
    "ELASTICSEARCH_URL",
    "http://localhost:9200"
)

es = Elasticsearch(ELASTICSEARCH_URL)