# Project Context: TrazAí

## 1. Project Overview

**Name:** TrazAí
**Description:** A shared shopping list PWA (Progressive Web App) for families.
**Key Features:**

- AI-powered automatic categorization of products (e.g., User inputs "Detergent", App categorizes as "Cleaning").
- Real-time shared lists via HTMX.
- Voice integration via Amazon Alexa ("Alexa, add bread to TrazAí").
- Family group management.

## 2. Tech Stack & Infrastructure

- **OS/Environment:** Linux (Fedora/Zorin), Docker & Docker Compose.
- **Language:** Python 3.12+.
- **Backend Framework:** Django 5.x.
- **API Framework:** **Django Ninja** (Strictly prefer over DRF). Use `Schema` (Pydantic) and `async` endpoints.
- **Frontend:** Django Templates (Serverside Rendering) + **HTMX** (Dynamic interactions) + **Tailwind CSS**.
- **Database:** PostgreSQL 16.
- **Async/Background Tasks:** Celery + Redis 7. (Used for AI API calls).
- **AI Provider:** OpenAI API (`gpt-4o-mini`) or Gemini API.

## 3. Architecture & Data Flow

- **Monolith Modular:** All code in one repo, organized by Django apps (`core`, `shopping_list`, `accounts`).
- **AI Flow:**
  1. User adds Item (Text).
  2. Item saved to DB (Category: NULL).
  3. Celery Task dispatched asynchronously.
  4. Task calls LLM -> Returns Category.
  5. Task updates Item in DB.
  6. Frontend updates via HTMX polling or SSE.

## 4. Database Schema (Draft)

### Apps Structure

- `accounts`: User and FamilyGroup logic.
- `lists`: Shopping lists, Items, Categories.

### Core Models

- **FamilyGroup**: `name`, `invite_code`.
- **CustomUser**: Extends AbstractUser, linked to `FamilyGroup`.
- **ShoppingList**: `name`, `family_group` (FK).
- **Category**: `name`, `color_hex`, `icon_slug`.
- **Item**: `name` (raw), `clean_name`, `category` (FK, nullable), `is_checked` (bool), `shopping_list` (FK).
- **ProductCache**: `term` (unique index), `predicted_category` (FK). Used to reduce API costs.

## 5. Development Rules (For AI Assistant)

1.  **Async First:** When writing API endpoints or I/O bound tasks, use `async def`.
2.  **Type Hinting:** Strictly use Python type hints and Pydantic schemas.
3.  **Config:** Use `python-decouple` (`config('VAR')`) to read from `.env`.
4.  **No React/Vue:** Keep the frontend simple with Django Templates + HTMX.
5.  **Docker:** Paths and connection strings must respect the Docker Compose service names (`db`, `redis`, etc.).

## 6. Current Status (As of Jan 2026)

- Infrastructure defined (`docker-compose.yml` created).
- Project initiated (`django-admin startproject core`).
- **PENDING:**
  - Configuration of `settings.py` for Database and Redis.
  - Creation of `celery.py` configuration.
  - Creation of the first app (`lists`).
