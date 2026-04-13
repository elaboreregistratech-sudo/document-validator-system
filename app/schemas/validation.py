from datetime import datetime
from pydantic import BaseModel


class ValidationRequestCreate(BaseModel):
    protocol_number: str
    applicant_name: str
    document_type: str
    template_id: int
    payload: dict
    notes: str | None = None


class ValidationResultResponse(BaseModel):
    is_valid: bool
    missing_fields: list[str]
    invalid_fields: list[str]
    messages: list[str]


class ValidationRequestResponse(BaseModel):
    id: int
    protocol_number: str
    applicant_name: str
    document_type: str
    status: str
    payload: dict
    result: dict | None
    notes: str | None
    template_id: int
    created_by: int
    created_at: datetime
    updated_at: datetime


class ValidationStatusUpdate(BaseModel):
    status: str
    notes: str | None = None
