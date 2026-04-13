# Document Validator System

API para validação documental, aplicação de regras de negócio, trilha de auditoria e workflows operacionais, voltada a cenários de cartórios, legal ops, backoffice documental e ambientes regulados.

Este projeto integra um portfólio em legal tech e automação de fluxos documentais, demonstrando como estruturar uma solução capaz de receber documentos, validar campos obrigatórios, aplicar regras, gerar status operacionais e manter histórico auditável.

## Sobre o problema

Em operações cartorárias e jurídico-documentais, é comum haver:
- conferência manual de campos e requisitos;
- retrabalho em protocolos incompletos;
- dificuldade para padronizar validações;
- baixa rastreabilidade das correções e decisões;
- pouca visibilidade sobre o status das solicitações.

## Solução proposta

O **Document Validator System** resolve esse cenário por meio de uma API que permite:
- cadastrar templates de validação por tipo documental;
- definir campos obrigatórios e regras por template;
- registrar solicitações de validação;
- validar payloads automaticamente;
- gerar status como `validated` e `pending_correction`;
- registrar trilha de auditoria para acompanhamento operacional.

## Stack

- **FastAPI**
- **Python 3.12**
- **SQLAlchemy 2**
- **JWT Authentication**
- **SQLite** para execução local
- Estrutura preparada para adaptação para **PostgreSQL**

## Funcionalidades

- Autenticação JWT
- Usuários com perfil administrativo
- Cadastro de templates documentais
- Regras de validação por template
- Criação de solicitações de validação
- Retorno estruturado com campos ausentes e inválidos
- Histórico de auditoria por solicitação
- Endpoint de health check
- Seed automático com usuário administrador e template inicial

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
