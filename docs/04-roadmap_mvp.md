# Roadmap MVP - TrazAí

Este documento define o plano de execução para o Produto Mínimo Viável (MVP) do TrazAí.

## Fase 1: Configuração e Fundação 🛠️
*Objetivo: Ter o ambiente de desenvolvimento rodando e a estrutura básica do projeto pronta.*

- [x] Inicializar repositório Git.
- [x] Configurar `docker-compose.yml` (Django, Postgres, Redis).
- [x] Criar projeto Django (`core`).
- [x] **Configurar `settings.py` com variáveis de ambiente (Decouple).**
- [x] Configurar conexão com Banco de Dados e testar migrações iniciais.
- [x] Configurar Celery e conexão com Redis.
- [x] Configurar estrutura de logs básica.

## Fase 2: Core Backend (Domínio) 🧱
*Objetivo: Implementar a lógica de negócios principal (Listas e Itens).*

- [x] Criar app `accounts`:
    - [x] Model `FamilyGroup`.
    - [x] Model `CustomUser` estendendo AbstractUser.
- [x] Criar app `lists`:
    - [x] Models `ShoppingList`, `Category`, `Item`.
    - [x] Migrations e Admin do Django para testar modelos.
- [x] Criar API com **Django Ninja** (v1):
    - [x] Endpoint `GET /lists`: Listar listas do grupo.
    - [x] Endpoint `POST /lists/{id}/items`: Adicionar item.
    - [x] Endpoint `PATCH /items/{id}`: Marcar check/uncheck.

## Fase 3: Integração IA (Background Tasks) 🤖
*Objetivo: Categorizar produtos automaticamente sem travar a UI.*

- [x] Model `ProductCache` no app `lists`.
- [x] Implementar Task Celery `categorize_item_task`:
    - [x] Lógica de verificação no Cache (DB).
    - [x] Integração com OpenAI/Gemini API (Prompt Engineering básico).
    - [x] Atualização do registro `Item` no banco.
- [x] Testar fluxo assíncrono (Adicionar item -> Task roda -> Item atualiza categoria).

## Fase 4: Frontend Básico (HTMX) 🖥️
*Objetivo: Interface funcional para uso familiar.*

- [ ] Configurar Templates Django Base + Tailwind CSS (via CDN ou build).
- [ ] Tela de Login/Cadastro (Simples).
- [ ] Dashboard (Listagem de Listas de Compras).
- [ ] Detalhe da Lista:
    - [ ] Input para adicionar item.
    - [ ] Listagem de itens agrupados por Categoria.
    - [ ] Implementar **HTMX** para:
        - [ ] Adicionar item sem reload.
        - [ ] Checkbox de item (Request PATCH).
        - [ ] Polling simples (a cada 5s) para atualizar categorias vindas da IA.

## Fase 5: Alexa Skill & Polimento 🗣️
*Objetivo: Adicionar itens por voz.*

- [ ] Endpoint Específico para Alexa (`/api/alexa/webhook`).
- [ ] Lógica de mapeamento de usuário (Vincular conta Alexa com conta TrazAí - *Account Linking* ou código simples).
- [ ] Comando "Adicionar {item} na lista".
- [ ] Deploy em ambiente de Staging (ex: Render, Railway ou VPS) para teste real com Alexa.

## Fase 6: Testes e Documentação ✅
- [ ] Testes Unitários para Models e Views principais.
- [ ] Documentação de API (Swagger gerado pelo Ninja).
- [ ] Preencher README final.
