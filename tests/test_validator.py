from app.services.validator import run_validation


def test_run_validation_success():
    payload = {"full_name": "Vitória Novais", "document_number": "123456", "issuer": "SSP"}
    required_fields = ["full_name", "document_number", "issuer"]
    rules = [
        {"field": "full_name", "type": "min_length", "value": 5},
        {"field": "document_number", "type": "numeric_only"},
        {"field": "issuer", "type": "allowed_values", "values": ["SSP", "DETRAN"]},
    ]

    result = run_validation(payload, required_fields, rules)
    assert result["is_valid"] is True
    assert result["missing_fields"] == []
    assert result["invalid_fields"] == []


def test_run_validation_failure():
    payload = {"full_name": "Ana", "document_number": "12A3", "issuer": "OUTRO"}
    required_fields = ["full_name", "document_number", "issuer", "cpf"]
    rules = [
        {"field": "full_name", "type": "min_length", "value": 5},
        {"field": "document_number", "type": "numeric_only"},
        {"field": "issuer", "type": "allowed_values", "values": ["SSP", "DETRAN"]},
    ]

    result = run_validation(payload, required_fields, rules)
    assert result["is_valid"] is False
    assert "cpf" in result["missing_fields"]
    assert "full_name" in result["invalid_fields"]
