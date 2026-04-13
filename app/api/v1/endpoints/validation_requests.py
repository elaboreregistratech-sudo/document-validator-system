import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models import AuditLog, DocumentTemplate, User, ValidationRequest
from app.schemas.audit import AuditLogResponse
from app.schemas.validation import (
    ValidationRequestCreate,
    ValidationRequestResponse,
    ValidationStatusUpdate,
)
from app.services.validator import run_validation

router = APIRouter(prefix="/validation-requests", tags=["validation_requests"])



def _serialize_request(item: ValidationRequest) -> ValidationRequestResponse:
    return ValidationRequestResponse(
        id=item.id,
        protocol_number=item.protocol_number,
        applicant_name=item.applicant_name,
        document_type=item.document_type,
        status=item.status,
        payload=json.loads(item.payload_json),
        result=json.loads(item.result_json) if item.result_json else None,
        notes=item.notes,
        template_id=item.template_id,
        created_by=item.created_by,
        created_at=item.created_at,
        updated_at=item.updated_at,
    )


@router.post("", response_model=ValidationRequestResponse)
def create_validation_request(
    data: ValidationRequestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    existing = db.query(ValidationRequest).filter(ValidationRequest.protocol_number == data.protocol_number).first()
    if existing:
        raise HTTPException(status_code=409, detail="Protocol number already exists")

    template = db.query(DocumentTemplate).filter(DocumentTemplate.id == data.template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")

    required_fields = json.loads(template.required_fields)
    rules = json.loads(template.validation_rules)
    result = run_validation(data.payload, required_fields, rules)
    status = "validated" if result["is_valid"] else "pending_correction"

    validation_request = ValidationRequest(
        protocol_number=data.protocol_number,
        applicant_name=data.applicant_name,
        document_type=data.document_type,
        payload_json=json.dumps(data.payload, ensure_ascii=False),
        result_json=json.dumps(result, ensure_ascii=False),
        status=status,
        notes=data.notes,
        template_id=data.template_id,
        created_by=current_user.id,
    )
    db.add(validation_request)
    db.commit()
    db.refresh(validation_request)

    audit_log = AuditLog(
        action="validation_request.created",
        details=f"Solicitação criada com status {status}",
        actor_id=current_user.id,
        validation_request_id=validation_request.id,
    )
    db.add(audit_log)
    db.commit()

    return _serialize_request(validation_request)


@router.get("", response_model=list[ValidationRequestResponse])
def list_validation_requests(
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    items = db.query(ValidationRequest).order_by(ValidationRequest.created_at.desc()).all()
    return [_serialize_request(item) for item in items]


@router.get("/{request_id}", response_model=ValidationRequestResponse)
def get_validation_request(
    request_id: int,
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    item = db.query(ValidationRequest).filter(ValidationRequest.id == request_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Validation request not found")
    return _serialize_request(item)


@router.patch("/{request_id}/status", response_model=ValidationRequestResponse)
def update_status(
    request_id: int,
    data: ValidationStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    item = db.query(ValidationRequest).filter(ValidationRequest.id == request_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Validation request not found")

    item.status = data.status
    item.notes = data.notes or item.notes
    db.commit()
    db.refresh(item)

    audit_log = AuditLog(
        action="validation_request.status_updated",
        details=f"Status alterado para {data.status}",
        actor_id=current_user.id,
        validation_request_id=item.id,
    )
    db.add(audit_log)
    db.commit()

    return _serialize_request(item)


@router.get("/{request_id}/audit", response_model=list[AuditLogResponse])
def get_audit_logs(
    request_id: int,
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    logs = (
        db.query(AuditLog)
        .filter(AuditLog.validation_request_id == request_id)
        .order_by(AuditLog.created_at.desc())
        .all()
    )
    return logs
