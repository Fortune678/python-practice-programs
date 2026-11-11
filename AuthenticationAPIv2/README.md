# LiteAuth API

A lightweight authentication REST API built with [Litestar](https://litestar.dev/) and SQLAlchemy, backed by a **PostgreSQL** database.

---

## Project Structure

```
LiteAuthApi/
├── app.py                          # Application entry point
├── controllers/
│   ├── authenticationcontroller.py # Registration & login endpoints
│   ├── LogoutController.py         # Logout / token revocation endpoint
│   └── usermanagementcontroller.py # CRUD endpoints for users
├── data/
│   ├── databaseconnection.py       # SQLAlchemy engine & session management
│   └── data_access.py              # All DB read/write operations
├── models/
│   ├── models.py                   # SQLAlchemy ORM models (User, Token)
│   └── schemas.py                  # Request/response dataclasses & Pydantic models
├── services/
│   ├── AuthService.py              # Token issuance, verification, revocation
│   ├── jwt_config.py               # JWT settings (secret, algorithm, expiry)
│   ├── jwt_guard.py                # Litestar guard — enforces Bearer token auth
│   └── jwt_helper.py               # Low-level JWT encode/decode utilities
└── utils/
    └── healthcheck.py              # Startup health-check script
```

---

## API Endpoints

### Authentication — `/auth`

| Method | Path | Auth required | Description | Request Body |
|--------|------|:---:|-------------|--------------|
| `POST` | `/auth/register` | ✗ | Register a new user | `{ "username": "...", "email": "...", "password": "..." }` |
| `POST` | `/auth/login` | ✗ | Authenticate and receive a JWT | `{ "email": "...", "password": "..." }` |
| `POST` | `/auth/logout` | ✗ | Revoke the provided JWT | `{ "token": "<jwt>" }` |

### User Management — `/users`

> All routes require `Authorization: Bearer <token>` header.

| Method | Path | Description | Request Body |
|--------|------|-------------|------|
| `GET` | `/users/` | List all users | — |
| `GET` | `/users/{user_id}` | Get a user by ID | — |
| `PUT` | `/users/{user_id}` | Update username and email | `{ "username": "...", "email": "..." }` |
| `DELETE` | `/users/{user_id}` | Delete a user by ID | — |

---

## Configuration

All settings are controlled via environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `postgresql://postgres:password@localhost:5432/liteauth_db` | Full PostgreSQL connection string |
| `JWT_SECRET` | `change-me-in-production-super-secret-key` | Secret used to sign JWTs — **must be changed in production** |
| `JWT_ALGORITHM` | `HS256` | JWT signing algorithm |
| `JWT_EXPIRY_SECONDS` | `3600` | Token lifetime in seconds (default: 1 hour) |

---

## Running the API

```bash
# Install dependencies
pip install litestar sqlalchemy psycopg2-binary pyjwt bcrypt

# Set environment variables (example)
export DATABASE_URL="postgresql://postgres:secret@localhost:5432/liteauth_db"
export JWT_SECRET="my-production-secret"

# Start the server
uvicorn app:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

---

## File Descriptions

### `app.py`
Bootstraps the Litestar application, registers all route handler controllers (`AuthController`, `UserManagementController`, `LogoutController`), and runs the startup health check. Also exposes a root `GET /` welcome endpoint.

### `controllers/authenticationcontroller.py`
Handles registration and login under `/auth`.
- **`POST /auth/register`** — Checks for duplicate email, hashes the password with bcrypt, and creates the user.
- **`POST /auth/login`** — Looks up the user by email, verifies the password with `bcrypt.checkpw`, and returns a signed JWT on success.

### `controllers/LogoutController.py`
Handles logout under `/auth`.
- **`POST /auth/logout`** — Accepts `{ "token": "<jwt>" }` and revokes it by deleting it from the database. After this call the token is rejected by the JWT guard even if the signature is still technically valid.

### `controllers/usermanagementcontroller.py`
Provides JWT-protected CRUD operations for user records under `/users`. The `PUT /{user_id}` endpoint accepts a JSON body `{ "username": "...", "email": "..." }` via the `UpdateUserRequest` schema.

### `services/AuthService.py`
Static service class for authentication operations:
- `create_user_token(user_id, username)` — Encodes a signed JWT and persists it in the `tokens` table.
- `verify_token(token)` — Validates the JWT signature/expiry **and** checks the token still exists in the DB (not revoked).
- `revoke_token(token)` — Deletes the token from the DB (logout).
- `get_user_from_token(token)` — Returns the `User` object for a valid, non-revoked token.

### `services/jwt_helper.py`
Low-level PyJWT wrappers: `encode_token`, `decode_token`, `get_user_id_from_token`. All other code should go through `AuthService` rather than calling these directly.

### `services/jwt_guard.py`
Litestar guard function (`jwt_guard`) that enforces `Authorization: Bearer <token>` on protected routes. Raises HTTP 401 if the header is missing, malformed, or the token is invalid/revoked.

### `data/databaseconnection.py`
Wraps a SQLAlchemy engine and session factory for PostgreSQL. Reads `DATABASE_URL` from the environment. Logs the connection URL with the password masked (`user:***@host`).

### `data/data_access.py`
All database interactions. Methods are grouped into:
- **User methods**: `create_user`, `get_users`, `get_user_by_id`, `get_user_by_email`, `get_user_by_username`, `update_user`, `delete_user`
- **Token methods**: `create_token`, `get_token`, `get_token_by_user_id`, `delete_token`, `delete_all_tokens_by_user_id`, `get_tokens`

### `models/models.py`
SQLAlchemy ORM models:
- **`User`** — `id`, `username` (unique), `email` (unique), `password` (bcrypt hash), `created_at`
- **`Token`** — `id`, `token` (up to 1024 chars, unique), `user_id` (FK → users), `created_at`

### `models/schemas.py`
Request/response schemas used by route handlers:
- `RegisterRequest` — `username`, `email`, `password`
- `LoginRequest` — `email`, `password`
- `UpdateUserRequest` — `username`, `email`
- `LogoutRequest` — `token` (validated non-empty)
- `TokenResponse` — `token`

### `utils/healthcheck.py`
Run at startup (and standalone via `python healthcheck.py`). Checks imports, controller availability, database connectivity, and port 8000 availability. Writes a timestamped report to `reports/SUCCESS/` or `reports/FAILED/`.

---

## Security Notes

- Passwords are hashed with **bcrypt** before storage and never stored in plain text.
- JWTs are signed with `HS256` (configurable). Set a strong `JWT_SECRET` in production.
- The database password is **masked** in all log output.
- Tokens are stored in the database and deleted on logout, providing a server-side revocation mechanism.
