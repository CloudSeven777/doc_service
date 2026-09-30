from fastapi import FastAPI
from sqlalchemy.orm import Session
import models
from database import engine, SessionLocal
from schemas import DocumentCreate
from elasticsearch_client import es



models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Document Search Service is running"}


@app.post("/documents")
def create_document(document: DocumentCreate):
    db: Session = SessionLocal()

    try:
        db_document = models.Document(
            id=document.id,
            rubrics=",".join(document.rubrics),
            text=document.text,
            created_date=document.created_date,
        )

        db.add(db_document)
        db.commit()
        db.refresh(db_document)
        es.index(
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
    finally:
        db.close()



@app.get("/documents/search")
def search_documents(q: str):
    response = es.search(
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

    db: Session = SessionLocal()

    try:
        documents = (
            db.query(models.Document)
            .filter(models.Document.id.in_(document_ids))
            .order_by(models.Document.created_date.desc())
            .limit(20)
            .all()
        )

        return [
            {
                "id": document.id,
                "rubrics": document.rubrics.split(","),
                "text": document.text,
                "created_date": document.created_date,
            }
            for document in documents
        ]
    finally:
        db.close()