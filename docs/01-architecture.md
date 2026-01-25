# Arquitetura do Sistema - TrazAí

Este documento descreve a arquitetura do projeto **TrazAí**, um Monolito Modular focado em simplicidade, performance e funcionalidades de IA.

## Visão Geral

O sistema segue o padrão **Monolito Modular**, onde o código é centralizado em um único repositório mas organizado em domínios de negócio claros (Django Apps). A comunicação com o cliente web é feita via **Django Templates + HTMX** (Server-Side Rendering com interatividade), enquanto a API para dispositivos móveis e Alexa é servida via **Django Ninja**.

## Componentes Principais

1.  **Django Web (Core)**:
    -   Responsável por servir o HTML inicial.
    -   Processa requisições HTMX para atualizações parciais de página (SPA-like feel).
    -   Gerencia autenticação e autorização.

2.  **API Gateway (Django Ninja)**:
    -   Expõe endpoints REST assíncronos.
    -   Ponto de entrada para a **Alexa Skill**.
    -   Utiliza Pydantic para validação rígida de dados.

3.  **Workers (Celery)**:
    -   Processamento de tarefas em segundo plano.
    -   Principal responsabilidade: Comunicação com APIs de IA (OpenAI/Gemini) para categorização de produtos.
    -   Evita bloqueio do loop de eventos principal do servidor web.

4.  **Message Broker (Redis)**:
    -   Fila de mensagens para o Celery.
    -   Cache de sessão e cache de respostas de API.

5.  **Banco de Dados (PostgreSQL)**:
    -   Armazenamento relacional persistente.
    -   Modelagem focada em integridade referencial (FamilyGroups, Lists, Items).

## Fluxos de Dados

### 1. Fluxo do Usuário (Web/HTMX)
1.  Usuário acessa a lista de compras no navegador.
2.  Django renderiza o template base (`base.html`).
3.  Usuário adiciona um item ("Leite").
4.  HTMX envia POST para `/lists/{id}/add`.
5.  Django salva o item e retorna um fragmento HTML (a linha da tabela atualizada).
6.  HTMX insere o HTML no DOM sem recarregar a página.

### 2. Fluxo de Integração com IA (Background)
1.  Quando um `Item` é salvo, um sinal (Django Signal) ou chamada direta dispara uma tarefa Celery.
2.  A tarefa `categorize_product_task` é enfileirada no Redis.
3.  O Worker consome a tarefa.
4.  O Worker verifica o `ProductCache` (DB) para ver se o termo já foi categorizado.
    -   **Cache Hit**: Usa a categoria existente.
    -   **Cache Miss**: Chama a API da LLM (OpenAI/Gemini).
5.  O Worker atualiza o `Item` com a `Category` correta.
6.  O Frontend é atualizado (via Polling HTMX ou WebSockets/SSE se implementado).

### 3. Fluxo Alexa
1.  Usuário diz: *"Alexa, adicione café na lista do TrazAí"*.
2.  Alexa Skill envia JSON para endpoint Django Ninja (`/api/alexa/webhook`).
3.  Django valida o request e identifica o `FamilyGroup` do usuário.
4.  Item é adicionado ao DB.
5.  Resposta de sucesso é enviada para a Alexa (TTS: *"Café adicionado"*).

## Diagrama de Arquitetura (Mermaid)

```mermaid
graph TD
    subgraph Clients
        Web[Web Browser (HTMX)]
        Alexa[Alexa Device]
    end

    subgraph Backend_Infrastructure
        LB[Reverse Proxy / Gunicorn]
        
        subgraph Django_App
            Ninja[API (Django Ninja)]
            Views[Django Views]
            Models[ORM]
        end
        
        subgraph Async_Workers
            Celery[Celery Workers]
        end
    end

    subgraph Data_Layer
        Postgres[(PostgreSQL)]
        Redis[(Redis - Broker/Cache)]
        LLM[External AI API]
    end

    %% Interactions
    Web -- HTTP/HTMX --> Views
    Alexa -- JSON/HTTPS --> Ninja
    
    Views --> Models
    Ninja --> Models
    
    Models -- Read/Write --> Postgres
    
    %% Async Flow
    Models -- "Trigger Task" --> Redis
    Redis -- "Consume Task" --> Celery
    Celery -- "API Call" --> LLM
    Celery -- "Update Item" --> Postgres
    Celery -- "Check Cache" --> Postgres

    classDef db fill:#e1f5fe,stroke:#01579b,stroke-width:2px;
    classDef ext fill:#fff3e0,stroke:#e65100,stroke-width:2px,stroke-dasharray: 5 5;
    
    class Postgres,Redis db;
    class LLM,Alexa ext;
```
