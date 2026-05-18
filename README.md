# User-Friendly System Call Interface for Enhanced Security

[![GitHub stars](https://img.shields.io/github/stars/sushantranjan912/User-Friendly-System-Call-Interface-for-Enhanced-Security.svg?style=social)](https://github.com/sushantranjan912/User-Friendly-System-Call-Interface-for-Enhanced-Security/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A web platform that exposes **controlled, auditable** system operations—file management and whitelisted shell commands—through a Flask API with authentication, logging, and role-based access.

---

## Table of contents

1. [Overview](#1-overview)
2. [Quick reference](#2-quick-reference)
3. [Technology stack](#3-technology-stack)
4. [Repository layout](#4-repository-layout)
5. [Getting started](#5-getting-started)
6. [Configuration](#6-configuration)
7. [Database](#7-database)
8. [Running the application](#8-running-the-application)
9. [Frontend and API](#9-frontend-and-api)
10. [Using the application](#10-using-the-application)
11. [Troubleshooting](#11-troubleshooting)
12. [Contributing](#12-contributing)
13. [License and authors](#13-license-and-authors)

---

## 1. Overview

**Secure System Call Interface** lets authorized users perform OS-level tasks through a validated gateway instead of direct shell access. The backend enforces permissions, sanitizes input, and records activity for review.

| Capability | Description |
|------------|-------------|
| Authentication | JWT sessions; roles: `admin`, `user`, `viewer` |
| File manager | Sandboxed storage with optional encryption and passcode locks |
| System calls | Whitelisted commands only; full execution logging |
| Audit trail | Action logs, system-call history, recycle bin |
| Dashboard | Activity and stats (broader access for `admin`) |

---

## 2. Quick reference

| Item | Value |
|------|--------|
| Application URL | http://localhost:5000 |
| API base URL | http://localhost:5000/api |
| Health check | http://localhost:5000/api/test |
| Entry point | `backend/app.py` |
| Default port | `5000` |
| Run from | `backend/` directory |
| Dependencies | `requirements.txt` (repo root) |
| Config file | `backend/.env` (optional) |
| SQLite database | `backend/database/database.db` (default) |

---

## 3. Technology stack

| Layer | Stack |
|-------|--------|
| Frontend | HTML, CSS, JavaScript — `frontend/` |
| Backend | Python 3, Flask — `backend/app.py` |
| Database | SQLite — `backend/database/` |
| Security | PyJWT, bcrypt, Fernet (`cryptography`) |
| Config | `python-dotenv` — `backend/config.py` |

**Python packages** (`requirements.txt`):

| Package | Role |
|---------|------|
| Flask | HTTP server and REST API |
| Flask-CORS | CORS for `/api/*` routes |
| PyJWT | Access tokens |
| bcrypt | Password hashing |
| python-dotenv | Environment variable loading |
| cryptography | Fernet encryption for sensitive data |

---

## 4. Repository layout

```
/
├── backend/                    # Flask API and runtime data
│   ├── app.py                  # Start here: python app.py
│   ├── config.py               # Settings and env vars
│   ├── database/
│   │   ├── db_connection.py    # SQLite + auto schema init
│   │   └── schema.sql
│   ├── routes/                 # API blueprints
│   ├── utils/                  # Auth, validation, secure ops
│   ├── ssci_files/             # User file sandbox
│   ├── recycle_bin/
│   └── file_permissions.json
├── frontend/                   # UI (served by Flask)
│   ├── index.html
│   ├── pages/
│   ├── css/
│   └── js/
├── docs/                       # Optional reference copies (not required to run)
├── requirements.txt
└── README.md
```

> **Note:** There is no `database/` folder at the repo root. The SQLite file is created under `backend/database/` at runtime.

---

## 5. Getting started

### 5.1 Prerequisites

- Python 3 with `pip`
- A terminal (PowerShell, Command Prompt, or bash)
- Windows is supported; several allowed commands are Windows-specific (`ipconfig`, `tasklist`, etc.)

### 5.2 Installation

```bash
# Clone the repository
git clone https://github.com/sushantranjan912/User-Friendly-System-Call-Interface-for-Enhanced-Security.git
cd User-Friendly-System-Call-Interface-for-Enhanced-Security

# Virtual environment (recommended)
python -m venv venv

# Activate — Windows (PowerShell)
venv\Scripts\activate

# Activate — Linux / macOS
# source venv/bin/activate

# Install dependencies (from repo root)
pip install -r requirements.txt
```

An identical `requirements.txt` exists in `backend/`; either location lists the same packages.

### 5.3 First run

```bash
cd backend
python app.py
```

Then open http://localhost:5000, register an account, and sign in.

Optional: configure `backend/.env` before the first run (see [Configuration](#6-configuration)).

---

## 6. Configuration

Settings are defined in `backend/config.py` and loaded with `python-dotenv`. Create **`backend/.env`** in the same directory where you run `python app.py`.

| Variable | Default | Purpose |
|----------|---------|---------|
| `SECRET_KEY` | `dev-secret-key` | Flask session secret |
| `JWT_SECRET_KEY` | `dev-jwt-secret` | JWT signing key |
| `DATABASE_PATH` | `database/database.db` | SQLite path (relative to `backend/`) |
| `ENCRYPTION_KEY` | *(see config.py)* | Fernet key for encrypted log details |

**Example `backend/.env`:**

```env
SECRET_KEY=your-flask-secret
JWT_SECRET_KEY=your-jwt-secret
DATABASE_PATH=database/database.db
ENCRYPTION_KEY=your-fernet-key-here
```

`ENCRYPTION_KEY` must be a valid Fernet key. If it is invalid, the app generates a new key at startup and prints a warning; previously encrypted data may not decrypt.

Generate a key (requires `cryptography` installed):

```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

Use strong, unique values in production. Defaults are suitable for local development only.

---

## 7. Database

Setup is **automatic**—no manual migration commands.

1. `backend/database/db_connection.py` creates the database directory when needed.
2. On first run, if the database file is missing, `backend/database/schema.sql` is applied.

| Detail | Value |
|--------|--------|
| Default file | `backend/database/database.db` |
| Tables | `users`, `system_calls`, `logs`, `login_attempts` |
| Default accounts | None — register via the UI or `POST /api/auth/register` |

**Registration rules** (from `backend/utils/validators.py`):

- **Username:** 3–20 characters; letters, numbers, underscore
- **Password:** minimum 8 characters; at least one letter and one number
- **Role:** `admin`, `user`, or `viewer`

---

## 8. Running the application

| Setting | Value |
|---------|--------|
| Command | `python app.py` |
| Working directory | `backend/` |
| Host | `0.0.0.0` |
| Port | `5000` |
| Debug mode | Enabled when using `app.py` |

**Stop the server:** `Ctrl+C`

**Verify it is running:**

```bash
curl http://localhost:5000/api/test
```

Expected response includes `"ok": true`.

Console output should include:

```
>>> Server running at: http://localhost:5000
>>> Test endpoint: http://localhost:5000/api/test
```

---

## 9. Frontend and API

### 9.1 How frontend and backend work together

- The UI is **static HTML/CSS/JS** in `frontend/`.
- Flask **serves the frontend and API** on one port—there is no separate Node.js server or build step.
- Access the app at **http://localhost:5000**, not by opening `frontend/index.html` directly (`file://` URLs will break API calls).

If you change the server host or port in `backend/app.py`, update `API_BASE_URL` in `frontend/js/modules/api.js` (default: `http://localhost:5000/api`).

### 9.2 UI routes

| URL | Page |
|-----|------|
| `/` | Landing, login, register |
| `/pages/dashboard.html` | Dashboard |
| `/pages/file_manager.html` | File manager |
| `/pages/logs.html` | Logs |
| `/pages/recycle_bin.html` | Recycle bin |
| `/pages/editor.html` | File editor |
| `/pages/viewer.html` | File viewer |

The `docs/` folder mirrors similar assets for reference only.

### 9.3 API endpoints

| Prefix | Purpose |
|--------|---------|
| `/api/auth` | Register, login, logout |
| `/api/system` | Whitelisted system commands |
| `/api` | Audit logs |
| `/api/files` | File manager |
| `/api/recycle-bin` | Recycle bin |
| `/api/test` | Health check |

### 9.4 Allowed system commands

Defined in `backend/config.py`:

`ls` · `dir` · `pwd` · `whoami` · `date` · `echo` · `ipconfig` · `hostname` · `systeminfo` · `tasklist`

Commands outside this list, or containing characters such as `;`, `&`, `|`, are rejected.

---

## 10. Using the application

1. Start the server (`cd backend` → `python app.py`).
2. Open http://localhost:5000.
3. **Register** — use role `admin` for full log access and file permission bypass.
4. **Log in** and navigate to the dashboard, file manager, or system-call tools.
5. Perform actions allowed for your role; all significant operations are logged.

Admin-only example: `GET /api/logs/stats` requires the `admin` role.

---

## 11. Troubleshooting

| Symptom | Solution |
|---------|----------|
| `ModuleNotFoundError` for Flask or other packages | Activate the venv; run `pip install -r requirements.txt` |
| Wrong database or file paths | Run `python app.py` from **`backend/`**, not the repo root |
| Port 5000 in use | Free the port, or change `port=5000` in `app.py` and `API_BASE_URL` in `frontend/js/modules/api.js` |
| `WARNING: Generated new encryption key` | Set a valid `ENCRYPTION_KEY` in `backend/.env` |
| UI loads but API calls fail | Use http://localhost:5000 via Flask, not `file://` on `index.html` |
| Registration rejected | Check username/password rules; email and username must be unique |
| System command rejected | Use only allowed commands; avoid shell metacharacters |
| `401` on protected routes | Log in again; JWT is stored in browser `localStorage` |

---

## 12. Contributing

1. Fork the repository.
2. Create a branch: `git checkout -b feature/my-feature`
3. Implement and test locally: `cd backend && python app.py`
4. Open a pull request with a clear description of your changes.

---

## 13. License and authors

**License:** MIT — see [LICENSE](LICENSE).

**Maintainers:** rajaman85, sushantranjan912, bittusingh14

### Planned enhancements

- Multi-factor authentication (MFA)
- Anomaly detection and alerting
- Real-time security notifications
- File version history
- Enhanced rate limiting and firewall rules
- Additional OS-level operations (network, process management)
