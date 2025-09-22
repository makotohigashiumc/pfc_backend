# Copilot Instructions for AI Coding Agents

## Project Overview
This workspace is a full-stack scheduling and account management system for massotherapists and clients, split into:
- **Back_end/**: Python (Flask) REST API, JWT authentication, PostgreSQL (Supabase)
- **Front_end/**: React + Vite SPA, communicates via HTTP to Back_end

## Architecture & Data Flow
- **Back_end** exposes endpoints for:
	- Client and massotherapist registration, login, account management
	- Scheduling (agendamentos) and history
	- JWT-protected routes (see `rota_clientes.py`, `rota_massoterapeuta.py`)
	- Database access via `database.py` (Supabase/PostgreSQL)
- **Front_end** uses `src/services/Api.js` and direct fetch calls in components to interact with API endpoints
- Data flows: User actions in React components → API calls → Flask routes → DB

## Developer Workflows
- **Back_end**:
	- Install: `pip install -r requirements.txt` (in `Back_end/`)
	- Run: `python app.py` (Flask dev server, port 5000)
	- DB connection string in `.env` as `DATABASE_URL`
	- Offline massotherapist registration: `python cadastrar_massoterapeuta_offline.py`
- **Front_end**:
	- Install: `npm install` (in `Front_end/`)
	- Dev server: `npm run dev` (port 5173)
	- Build: `npm run build`

## Conventions & Patterns
- **Back_end**:
	- Route files (`rota_*.py`) group related endpoints using Flask Blueprints
	- JWT required for most account and scheduling actions
	- Error handling via Flask error handlers (see `app.py`)
	- DB access via helper functions in `cliente.py`, `massoterapeuta.py`
	- Passwords hashed with Werkzeug
- **Front_end**:
	- Components organized by feature (e.g., `Conta/`, `Perfil/`, `Agendamentos/`)
	- API calls centralized in `services/Api.js` and also directly in components
	- Auth tokens stored in `localStorage`, sent as `Authorization: Bearer <token>`
	- Form validation and error display in components

## Integration Points
- **API Contract**: Endpoints in Back_end must match usage in Front_end (see `Api.js` and fetch calls in components)
- **Authentication**: JWT tokens required for most API calls; login endpoints return token
- **Database**: Model changes in Back_end require updates to forms and API usage in Front_end

## Examples
- To add a new scheduling feature:
	1. Update Back_end route and DB logic (`rota_clientes.py`, `cliente.py`)
	2. Update Front_end component (e.g., `AgendamentosCliente.jsx`)
	3. Update API call in `Api.js` or component

## External Dependencies
- Back_end: Flask, Flask-JWT-Extended, Flask-CORS, python-dotenv, psycopg2, Werkzeug
- Front_end: React, Vite, jwt-decode, react-datepicker

## Key Files & Directories
- `Back_end/app.py`, `Back_end/database.py`, `Back_end/rota_clientes.py`, `Back_end/rota_massoterapeuta.py`, `Back_end/cliente.py`, `Back_end/massoterapeuta.py`
- `Front_end/src/components/`, `Front_end/src/services/Api.js`, `Front_end/package.json`, `Front_end/vite.config.js`

---
**Feedback:** If any section is unclear or missing, specify which workflows, conventions, or integration details need further documentation.
