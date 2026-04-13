from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    action: Mapped[str] = mapped_column(String(80), nullable=False)
    details: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    actor_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    validation_request_id: Mapped[int | None] = mapped_column(ForeignKey("validation_requests.id"), nullable=True)

    actor = relationship("User", back_populates="audit_logs")
    validation_request = relationship("ValidationRequest", back_populates="audit_logs")
