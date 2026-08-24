from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.api.document import DocumentCreate

app = FastAPI(
    title="Mesh API",
    version="0.0.0",
)

@app.get("/")
async def root():
    return {"message": "Mesh API is running"}

@app.post("/documents/")
async def create_document(document: DocumentCreate,
    db: Session = Depends(get_db),
):
    db_document = Document(
        title=document.title,
        content=document.content,
        user_id=document.user_id,
    )
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return {
        "title": document.title,
        "content": document.content,
    }