# TrazAí 🛒

TrazAí is a shared shopping list Progressive Web App (PWA) designed for families. It features AI-powered automatic product categorization, real-time updates using HTMX, and voice integration via Amazon Alexa.

## 🚀 Features

- **AI-Powered Categorization:** Automatically categorizes products as they are added (e.g., adding "Detergent" automatically assigns it to the "Cleaning" category) using LLMs (OpenAI/Gemini).
- **Real-Time Shared Lists:** Collaborate with your family in real-time with a fast, SPA-like experience powered by HTMX.
- **Voice Integration:** Add items to your shopping list using Amazon Alexa ("Alexa, add bread to TrazAí").
- **Family Group Management:** Easily manage your family members and shared lists.

## 🛠️ Tech Stack

- **Backend:** Python 3.12+, Django 5.x
- **API Framework:** Django Ninja (Async, Pydantic)
- **Frontend:** Server-Side Rendering (Django Templates) + HTMX + Tailwind CSS
- **Database:** PostgreSQL 16
- **Background Tasks:** Celery + Redis 7
- **AI Integration:** OpenAI API (`gpt-4o-mini`) / Gemini API
- **Infrastructure:** Docker & Docker Compose, Traefik (Coolify), Cloudflare R2 (Storage)

## 🏗️ Architecture

TrazAí is built as a **Modular Monolith**. It uses a single repository organized into specific Django apps (`core`, `accounts`, `lists`). 

- The **Web Interface** is served using server-side rendered Django Templates enriched with HTMX for dynamic, partial page reloads.
- The **Mobile/Voice API** is exposed via Django Ninja using async endpoints.
- **AI Processing** is offloaded to background workers using Celery and Redis to ensure the web interface remains fast and responsive.

*For more details, check the `docs/` folder.*

## ⚙️ Prerequisites

- Docker
- Docker Compose

## 💻 Local Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd trazai
   ```

2. **Environment Variables:**
   Create a `.env` file in the root directory and configure the necessary variables (Database, Redis, AI API keys, etc.).

3. **Start the containers:**
   ```bash
   docker-compose up -d --build
   ```
   This will start the Django Web server, Celery worker, PostgreSQL database, and Redis.

4. **Run Migrations:**
   ```bash
   docker-compose exec web python backend/manage.py migrate
   ```

5. **Create a Superuser:**
   ```bash
   docker-compose exec web python backend/manage.py createsuperuser
   ```

6. **Access the application:**
   Open your browser and navigate to `http://localhost:8000` (or the port specified in your docker-compose).

## 📂 Project Structure

- `backend/`: Contains the core Django application, settings, and apps.
- `docs/`: Architectural documentation, setup guides, schema designs, and MVP roadmap.
- `docker-compose.yml`: Services configuration for local development.
