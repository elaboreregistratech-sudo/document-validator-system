from datetime import datetime
from pydantic import BaseModel


class DocumentTemplateCreate(BaseModel):
    code: str
    name: str
    description: str | None = None
    required_fields: list[str]
    validation_rules: list[dict]


class DocumentTemplateResponse(BaseModel):
    id: int
    code: str
    name: str
    description: str | None
    required_fields: list[str]
    validation_rules: list[dict]
    created_at: datetime

    class Config:
        from_attributes = True
