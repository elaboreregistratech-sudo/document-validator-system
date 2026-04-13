import json
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_admin
from app.db.session import get_db
from app.models import DocumentTemplate, User
from app.schemas.template import DocumentTemplateCreate, DocumentTemplateResponse

router = APIRouter(prefix="/templates", tags=["templates"])


def _serialize_template(template: DocumentTemplate) -> DocumentTemplateResponse:
    return DocumentTemplateResponse(
        id=template.id,
        code=template.code,
        name=template.name,
        description=template.description,
        required_fields=json.loads(template.required_fields),
        validation_rules=json.loads(template.validation_rules),
        created_at=template.created_at,
    )


@router.post("", response_model=DocumentTemplateResponse)
def create_template(
    data: DocumentTemplateCreate,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    existing = db.query(DocumentTemplate).filter(DocumentTemplate.code == data.code).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Template code already exists")

    template = DocumentTemplate(
        code=data.code,
        name=data.name,
        description=data.description,
        required_fields=json.dumps(data.required_fields, ensure_ascii=False),
        validation_rules=json.dumps(data.validation_rules, ensure_ascii=False),
    )
    db.add(template)
    db.commit()
    db.refresh(template)
    return _serialize_template(template)


@router.get("", response_model=list[DocumentTemplateResponse])
def list_templates(
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    templates = db.query(DocumentTemplate).order_by(DocumentTemplate.created_at.desc()).all()
    return [_serialize_template(item) for item in templates]
