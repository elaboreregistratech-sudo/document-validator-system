import json
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.security import get_password_hash
from app.db.base import Base
from app.db.session import engine, SessionLocal
from app.models import DocumentTemplate, User


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
    settings = get_settings()
    db: Session = SessionLocal()
    try:
        admin = db.query(User).filter(User.email == settings.default_admin_email).first()
        if not admin:
            admin = User(
                full_name="System Administrator",
                email=settings.default_admin_email,
                hashed_password=get_password_hash(settings.default_admin_password),
                role="admin",
                is_active=True,
            )
            db.add(admin)
            db.commit()

        template = db.query(DocumentTemplate).filter(DocumentTemplate.code == "RG_STANDARD").first()
        if not template:
            template = DocumentTemplate(
                code="RG_STANDARD",
                name="Validação padrão de documento pessoal",
                description="Template base para validar nome, número e órgão emissor.",
                required_fields=json.dumps(["full_name", "document_number", "issuer"]),
                validation_rules=json.dumps(
                    [
                        {"field": "full_name", "type": "min_length", "value": 5},
                        {"field": "document_number", "type": "numeric_only"},
                        {
                            "field": "issuer",
                            "type": "allowed_values",
                            "values": ["SSP", "DETRAN", "POLICIA FEDERAL"],
                        },
                    ]
                ),
            )
            db.add(template)
            db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
