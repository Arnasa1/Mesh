from pydantic import BaseModel, Field
class DocumentCreate(BaseModel):
    title: str = Field(..., max_length=255)
    content: str = Field(..., max_length=255)
    user_id: int = Field