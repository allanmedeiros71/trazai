# Guia de Configuração (Setup Guide)

Este guia descreve os passos para rodar o projeto **TrazAí** localmente a partir do zero.

## Pré-requisitos

Certifique-se de ter instalado em sua máquina:

1.  **Docker Engine** (versão 24+ recomendada).
2.  **Docker Compose** (Plugin V2).
3.  **Git**.
4.  **(Opcional)** `Make` (para facilitar comandos, se houver Makefile).

## Configuração do Ambiente

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/seu-usuario/trazai.git
    cd trazai
    ```

2.  **Crie o arquivo `.env`:**
    Copie o exemplo (se houver) ou crie um arquivo `.env` na raiz do projeto com as seguintes variáveis. Estas chaves são essenciais para conectar o Django ao PostgreSQL e Redis definidos no `docker-compose.yml`.

    ```ini
    # Django Core
    SECRET_KEY=sua-chave-secreta-desenvolvimento-insegura
    DEBUG=True
    ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

    # Banco de Dados (Deve bater com o docker-compose.yml)
    # No docker-compose, o host do banco é o nome do serviço: 'db'
    DB_NAME=trazai_db
    DB_USER=trazai_user
    DB_PASSWORD=trazai_pass
    DB_HOST=db
    DB_PORT=5432

    # Redis & Celery
    # Host 'redis' é o nome do serviço no docker-compose
    CELERY_BROKER_URL=redis://redis:6379/0
    CELERY_RESULT_BACKEND=redis://redis:6379/0

    # AI Configuration (Futuro)
    OPENAI_API_KEY=sk-proj-...
    ```

    > **Nota:** As credenciais de banco de dados (`DB_NAME`, `DB_USER`, `DB_PASSWORD`) devem corresponder exatamente às variáveis de ambiente `POSTGRES_...` definidas no serviço `db` do arquivo `docker-compose.yml`.

## Executando o Projeto

Utilizamos o Docker Compose para orquestrar todos os serviços (App, Worker, DB, Redis).

1.  **Subir os containers (Build + Up):**
    ```bash
    docker compose up --build
    ```
    *A primeira execução pode demorar alguns minutos para baixar as imagens e instalar as dependências Python.*

2.  **Rodar Migrações:**
    Com os containers rodando (em outro terminal):
    ```bash
    docker compose exec web python manage.py migrate
    ```

3.  **Criar Superusuário (Admin):**
    ```bash
    docker compose exec web python manage.py createsuperuser
    ```

4.  **Acessar a Aplicação:**
    -   **Web App:** [http://localhost:8000](http://localhost:8000)
    -   **Admin Panel:** [http://localhost:8000/admin](http://localhost:8000/admin)
    -   **API Docs (Swagger):** [http://localhost:8000/api/docs](http://localhost:8000/api/docs)

## Comandos Úteis

-   **Parar containers:** `docker compose down`
-   **Ver logs:** `docker compose logs -f`
-   **Criar novas migrações (após editar models):**
    ```bash
    docker compose exec web python manage.py makemigrations
    ```
-   **Recriar containers (se mudar dependências):**
    ```bash
    docker compose up --build -d
    ```

## Solução de Problemas Comuns

-   **Erro de conexão com DB:** Verifique se o container `db` está "healthy" ou "running". O Django pode tentar conectar antes do Postgres estar pronto na primeira vez. O Docker Compose deve lidar com isso, mas um restart pode ser necessário.
-   **Erro de permissão no Linux:** Se tiver problemas com volumes docker, verifique as permissões da pasta local ou rode com `sudo` (não recomendado para dev, melhor adicionar seu usuário ao grupo docker).
