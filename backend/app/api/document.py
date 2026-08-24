from pydantic import BaseModel, Field, field_validator
class DocumentCreate(BaseModel):
    title: str = Field(min_length=8, max_length=255)
    content: str = Field(min_length=1, max_length=255)
    @field_validator("title")
    def title_must_not_be_empty(cls, value):
        if not value.strip():
            raise ValueError("Title must not be shorter than 8 characters")
        return value
    def content_must_not_be_empty(cls, value):
        if not value.strip():
            raise ValueError("Content must not be shorter than 1 character")
        return value
    