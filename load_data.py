import ast
import csv
from datetime import datetime

import models
from database import SessionLocal, engine
from elasticsearch_client import es


models.Base.metadata.create_all(bind=engine)


def load_data():
    db = SessionLocal()

    try:
        with open("posts.csv", "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for document_id, row in enumerate(reader, start=1):
                rubrics = ast.literal_eval(row["rubrics"])
                created_date = datetime.strptime(
                    row["created_date"],
                    "%Y-%m-%d %H:%M:%S",
                )

                document = models.Document(
                    id=document_id,
                    rubrics=",".join(rubrics),
                    text=row["text"],
                    created_date=created_date,
                )

                db.add(document)

                es.index(
                    index="documents",
                    id=document_id,
                    document={
                        "id": document_id,
                        "text": row["text"],
                    },
                )

            db.commit()

    finally:
        db.close()


if __name__ == "__main__":
    load_data()