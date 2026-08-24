from fastapi import FastAPI, Depends, Response, Request
from sqlalchemy.orm import Session
from fastapi.exceptions import RequestValidationError
from app.database import get_db
from app.api.document import DocumentCreate
from app.models.models import Document

app = FastAPI(
    title="Mesh API",
    version="0.0.0",
)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
):
    return Response(
        content=f"Validation error: {exc}", status_code=400
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
    )
    try:
        db.add(db_document)
        db.commit()
        db.refresh(db_document)
    except Exception as e:
        db.rollback()
        return Response(
            content=f"Error creating document: {str(e)}", status_code=400)
    return {
        "title": document.title,
        "content": document.content,
    }