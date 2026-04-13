from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class ValidationRequest(Base):
    __tablename__ = "validation_requests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    protocol_number: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    applicant_name: Mapped[str] = mapped_column(String(120), nullable=False)
    document_type: Mapped[str] = mapped_column(String(80), nullable=False)
    payload_json: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="pending", nullable=False)
    result_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    template_id: Mapped[int] = mapped_column(ForeignKey("document_templates.id"), nullable=False)
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    template = relationship("DocumentTemplate", back_populates="validation_requests")
    created_by_user = relationship("User", back_populates="validation_requests")
    audit_logs = relationship("AuditLog", back_populates="validation_request")
