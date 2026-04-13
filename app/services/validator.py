from typing import Any


def run_validation(payload: dict[str, Any], required_fields: list[str], rules: list[dict[str, Any]]) -> dict[str, Any]:
    missing_fields: list[str] = []
    invalid_fields: list[str] = []
    messages: list[str] = []

    for field in required_fields:
        value = payload.get(field)
        if value is None or value == "":
            missing_fields.append(field)
            messages.append(f"Campo obrigatório ausente: {field}")

    for rule in rules:
        field = rule.get("field")
        rule_type = rule.get("type")
        value = payload.get(field)

        if value is None:
            continue

        if rule_type == "min_length":
            minimum = int(rule.get("value", 0))
            if len(str(value).strip()) < minimum:
                invalid_fields.append(field)
                messages.append(f"Campo {field} possui tamanho inferior ao mínimo de {minimum} caracteres")

        if rule_type == "allowed_values":
            allowed = rule.get("values", [])
            if value not in allowed:
                invalid_fields.append(field)
                messages.append(f"Campo {field} possui valor inválido")

        if rule_type == "numeric_only":
            if not str(value).isdigit():
                invalid_fields.append(field)
                messages.append(f"Campo {field} deve conter apenas números")

    return {
        "is_valid": not missing_fields and not invalid_fields,
        "missing_fields": missing_fields,
        "invalid_fields": invalid_fields,
        "messages": messages,
    }
