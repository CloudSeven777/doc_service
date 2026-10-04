import asyncio
import csv
from datetime import datetime

import models
from database import SessionLocal, engine
from elasticsearch_client import es


async def load_data():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

    async with SessionLocal() as db:
        with open("posts.csv", "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                document_id = int(row["id"])
                created_date = datetime.fromisoformat(row["created_date"])

                document = models.Document(
                    id=document_id,
                    rubrics=row["rubrics"],
                    text=row["text"],
                    created_date=created_date,
                )

                db.add(document)

                await es.index(
                    index="documents",
                    id=document_id,
                    document={
                        "id": document_id,
                        "text": row["text"],
                    },
                )

            await db.commit()

    await es.close()


if __name__ == "__main__":
    asyncio.run(load_data())