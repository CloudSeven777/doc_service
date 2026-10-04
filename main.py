from fastapi import FastAPI
from sqlalchemy import select

import models
from database import engine, SessionLocal
from schemas import DocumentCreate
from elasticsearch_client import es


app = FastAPI()


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


@app.get("/")
async def root():
    return {"message": "Document Search Service is running"}


@app.post("/documents")
async def create_document(document: DocumentCreate):
    async with SessionLocal() as db:
        db_document = models.Document(
            id=document.id,
            rubrics=",".join(document.rubrics),
            text=document.text,
            created_date=document.created_date,
        )

        db.add(db_document)
        await db.commit()
        await db.refresh(db_document)

        await es.index(
            index="documents",
            id=db_document.id,
            document={
                "id": db_document.id,
                "text": db_document.text,
            },
        )

        return {
            "id": db_document.id,
            "rubrics": db_document.rubrics.split(","),
            "text": db_document.text,
            "created_date": db_document.created_date,
        }


@app.get("/documents/search")
async def search_documents(q: str):
    response = await es.search(
        index="documents",
        query={
            "match": {
                "text": q
            }
        },
        size=20,
    )

    document_ids = [
        int(hit["_id"])
        for hit in response["hits"]["hits"]
    ]

    if not document_ids:
        return []

    async with SessionLocal() as db:
        result = await db.execute(
            select(models.Document)
            .where(models.Document.id.in_(document_ids))
            .order_by(models.Document.created_date.desc())
            .limit(20)
        )

        documents = result.scalars().all()

        return [
            {
                "id": document.id,
                "rubrics": document.rubrics.split(","),
                "text": document.text,
                "created_date": document.created_date,
            }
            for document in documents
        ]


@app.delete("/documents/{document_id}")
async def delete_document(document_id: int):
    async with SessionLocal() as db:
        result = await db.execute(
            select(models.Document).where(
                models.Document.id == document_id
            )
        )
        document = result.scalar_one_or_none()

        if document is None:
            return {"message": "Document not found"}

        await db.delete(document)
        await db.commit()

        if await es.exists(index="documents", id=document_id):
            await es.delete(index="documents", id=document_id)

        return {"message": "Document deleted successfully"}