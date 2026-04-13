# Document Validator System

API profissional para **validação documental, regras de negócio, trilha de auditoria e workflows operacionais**, pensada para cenários de **cartórios, legal ops, backoffice documental e ambientes regulados**.

Este projeto compõe um portfólio voltado a **legal tech e automação de fluxos documentais**, demonstrando como estruturar uma solução para receber documentos, validar campos obrigatórios, aplicar regras, gerar status operacionais e manter histórico auditável.

## Problema

Em operações cartorárias e jurídico-documentais, é comum haver:
- conferência manual de campos e requisitos;
- retrabalho em protocolos incompletos;
- dificuldade para padronizar validações;
- baixa rastreabilidade das correções e decisões;
- pouca visibilidade sobre o status das solicitações.

## Solução

O **Document Validator System** resolve esse cenário por meio de uma API que permite:
- cadastrar templates de validação por tipo documental;
- definir campos obrigatórios e regras por template;
- registrar solicitações de validação;
- validar payloads automaticamente;
- gerar status como `validated` ou `pending_correction`;
- registrar trilha de auditoria para acompanhamento operacional.

## Stack

- **FastAPI**
- **Python 3.12**
- **SQLAlchemy 2**
- **JWT Authentication**
- **SQLite** para execução rápida local
- Estrutura pronta para adaptação para PostgreSQL

## Funcionalidades

- Autenticação JWT
- Usuários com perfil administrativo
- Cadastro de templates documentais
- Regras de validação por template
- Criação de solicitações de validação
- Retorno estruturado com campos ausentes e inválidos
- Histórico de auditoria por solicitação
- Endpoint de health check
- Seed automático com usuário admin e template inicial

## Estrutura do projeto

```text
app/
  api/
  core/
  db/
  models/
  schemas/
  services/
  main.py
  seed.py
tests/
requirements.txt
README.md
```

## Regras suportadas no starter

No projeto inicial, o motor de validação suporta:
- `min_length`
- `allowed_values`
- `numeric_only`

Essas regras podem ser expandidas para:
- regex
- validação de CPF/CNPJ
- obrigatoriedade condicional
- datas válidas
- comparação entre campos
- validação por categoria documental

## Como executar localmente

### 1. Clonar o repositório

```bash
git clone <PRIVATE_URL>
cd document-validator-system
```

### 2. Criar e ativar ambiente virtual

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Criar arquivo `.env`

Copie o `.env.example` para `.env`.

### 5. Rodar a aplicação

```bash
uvicorn app.main:app --reload
```

A API ficará disponível em:
- `http://localhost:8000`
- Swagger: `http://localhost:8000/docs`

## Credenciais iniciais

O seed cria automaticamente:
- **email:** `admin@legaltech.local`
- **senha:** `Admin@123`

## Fluxo sugerido de uso

1. Fazer login em `/api/v1/auth/login`
2. Cadastrar ou listar templates em `/api/v1/templates`
3. Criar uma solicitação em `/api/v1/validation-requests`
4. Consultar resultado da validação
5. Consultar trilha em `/api/v1/validation-requests/{id}/audit`

## Exemplo de template

```json
{
  "code": "RG_STANDARD",
  "name": "Validação padrão de documento pessoal",
  "description": "Template base",
  "required_fields": ["full_name", "document_number", "issuer"],
  "validation_rules": [
    {"field": "full_name", "type": "min_length", "value": 5},
    {"field": "document_number", "type": "numeric_only"},
    {"field": "issuer", "type": "allowed_values", "values": ["SSP", "DETRAN", "POLICIA FEDERAL"]}
  ]
}
```

## Exemplo de solicitação de validação

```json
{
  "protocol_number": "VAL-2026-0001",
  "applicant_name": "Vitória Novais",
  "document_type": "RG",
  "template_id": 1,
  "payload": {
    "full_name": "Vitória Novais",
    "document_number": "123456789",
    "issuer": "SSP"
  },
  "notes": "Validação inicial do protocolo"
}
```

## Resultados esperados

### Caso válido

```json
{
  "is_valid": true,
  "missing_fields": [],
  "invalid_fields": [],
  "messages": []
}
```

### Caso com inconsistências

```json
{
  "is_valid": false,
  "missing_fields": ["cpf"],
  "invalid_fields": ["document_number"],
  "messages": [
    "Campo obrigatório ausente: cpf",
    "Campo document_number deve conter apenas números"
  ]
}
```

## Roadmap

- Integração com PostgreSQL
- Upload e análise de arquivos
- Validação por regex e regras compostas
- Dashboard com métricas operacionais
- Filas assíncronas para processamento em lote
- Versionamento de templates
- Logs estruturados e observabilidade

## Valor para o portfólio

Este projeto reforça competências em:
- modelagem de regras de negócio;
- construção de APIs para ambientes regulados;
- autenticação e controle de acesso;
- rastreabilidade e auditoria;
- automação aplicada a fluxos documentais;
- desenho de soluções aderentes ao contexto cartorário/legal.

## Licença

Uso educacional e demonstrativo para portfólio profissional.
