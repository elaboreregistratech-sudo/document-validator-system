from datetime import datetime
from pydantic import BaseModel


class AuditLogResponse(BaseModel):
    id: int
    action: str
    details: str | None
    created_at: datetime
    actor_id: int | None
    validation_request_id: int | None

    class Config:
        from_attributes = True
