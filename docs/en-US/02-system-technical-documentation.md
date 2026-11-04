# OMNILOG HUB — System Technical Documentation & API Reference

## 1. Purpose and scope
OMNILOG HUB is a logistics management learning project. The repository contains a Python/FastAPI service and browser interface, a Java domain module for object-oriented coursework, a JavaFX desktop proof of concept, and a Node.js/Express API module for the web-backend coursework. These are parallel coursework deliverables; they are not yet a single production deployment.

## 2. Architecture
- **Web UI:** semantic HTML, CSS and JavaScript in `frontend/`.
- **Existing service:** FastAPI application in `backend/`, connected to MySQL through SQLAlchemy.
- **Domain layer:** Java 21 classes in `uc4-java/`; abstract `Veiculo`, concrete vehicle types, payment interface and FIFO/LIFO structures.
- **Desktop proof of concept:** JavaFX MVC separation in `uc8-desktop/`; DAO uses prepared JDBC statements.
- **Node API:** Express routes/controllers/models in `uc13-node/`; parameterized SQL through mysql2.
- **Database:** MySQL 8 schema in `database/`.

## 3. Installation
### Existing Python service
1. Install Python 3.12 and MySQL 8.
2. Create the `omnilog_hub` schema with `database/01_create_database.sql`.
3. Create a local `.env` from `.env.example` (do not commit it) and set database credentials.
4. Install `backend/requirements.txt` in a virtual environment.
5. Run `python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000`.
6. Open `http://127.0.0.1:8000/docs`.

### Node API
1. Install Node.js 20+ and run `cd uc13-node && npm install`.
2. Copy `.env.example` to `.env`, set DB credentials and a long random `SESSION_SECRET`.
3. Run `npm test`, then `npm start`; API listens on port 3001 by default.
4. `GET /api/health` is public. Customer routes require a valid session: `POST /api/auth/login`, `POST /api/auth/logout`, `GET /api/customers?search=&limit=&offset=`, `GET /api/customers/{id}`, `POST /api/customers`.
5. Seed user password hashes securely; never store plaintext passwords.

### Java modules
- `cd uc4-java && mvn test` runs domain tests.
- `cd uc8-desktop && mvn javafx:run` launches the desktop proof of concept after setting DB environment variables.

## 4. API contracts (Node.js)
- `POST /api/auth/login`: JSON `{ "email": "...", "password": "..." }`; returns authenticated session or 401.
- `POST /api/auth/logout`: destroys the session.
- `GET /api/customers`: session required; returns `{ "items": [...] }`; supports bounded `limit`, `offset`, and `search`.
- `GET /api/customers/:id`: returns one customer or 404.
- `POST /api/customers`: session required; JSON requires `full_name` and valid `email`; returns 201 or 409 for duplicate e-mail.

All SQL values are parameterized. Error responses avoid exposing database details. Session storage is Express's development default and must be replaced with a persistent store before production.

## 5. Security and deployment notes
Use HTTPS, a persistent session store, a strong secret from a secret manager, secure cookies, restricted CORS, least-privilege DB credentials, backups, monitoring and dependency updates in deployment. The included Node service is a coursework baseline, not a production-certified system. Payment operations are simulations and must not be treated as real authorizations.

## 6. English presentation outline
“Good morning. OMNILOG HUB is a logistics management platform designed to organize customers, products, warehouse inventory, orders and deliveries. Its architecture separates the user interface, application services, domain logic and relational persistence. We use parameterized SQL, input validation and session-based authentication in the Node API sample. The Java domain module demonstrates polymorphic vehicle calculations, payment contracts, a stack for operator history and a queue for dispatch. The next steps before production are end-to-end integration, persistent session storage, security testing, deployment validation and operational monitoring. Thank you. I will be happy to answer your questions.”
